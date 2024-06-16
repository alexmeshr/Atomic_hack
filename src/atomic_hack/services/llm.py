import json
import logging
from typing import NewType

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from atomic_hack.entities.llm import MessageRole
from atomic_hack.settings import settings

logger = logging.getLogger(__name__)

LLMMessage = NewType('Message', dict[str, str])

SYSTEM_SUMMARIZATION_PROMPT: str = '''Тебе на вход будут приходить жалобы пользователей.
Ты умеешь отбрасывать всё лишнее - знаки вопроса / вводные слова / эмоции / ..., выделять корень проблемы и отдавать их в формате json. В поле "problems" должен быть список проблем.
Одна проблема - одна строка. Если в сообщении не сформулировано проблемы  возникшей у пользователя то массив поля "problems" должен быть пустой.
Не используй форматирование или стили кода, нужен только текст.

Пример:
- ввод: У меня нихрена не работает! Я нажимаю на кнопку войти и оно не входит! Вы там совсем уже!??
  вывод: {"problems": ["не работает кнопка войти"]}
- ввод: Добрый день! Не хочу вас отвлекать, но, если не сложно, подскажите пожалуйста, как сформировать отчет?
  вывод: {"problems": ["не получается сформировать отчет"]}
- ввод: Здравствуйте! Помогите пожалуйста, не получается актуализировать распределение на основании данного изменения, т.к. компьютер его не видит при выборе по кнопке
  вывод: {"problems": ["не получается актуализировать распределение", "компьютер не видит изменения"]}

Если жалоба пользователя не содержит конкретных проблем - верни пустой список проблем
Пример:
- ввод: Какой чудесный день! Пошли пить пиво вечером?
  вывод: {"problems": []}

Делай так на каждый ввод пользователя. Твой вывод должен быть валидным json-файлом.
'''

ASSISTANT_ADDITIONAL_SUMMARIZATION_PROMPT: str = (
    'выдай ответ в нужном формате, там не должно быть лишних слов, не должно быть форматирования, не должно быть ```'
)

SYSTEM_COMBINE_RESPONSE_PROMBP: str = '''Тебе даны инструкции. Ты можешь на них ссылаться.
С помощью этих инструкций ты помогаешь пользователям решать их проблемы.

В начале тебе будут отправлены инструкции, потом история общения с пользоваетелм.
Этот пользователь столкнулся с проблемой. Твоя задача - ему помочь. Прочитав твой ответ пользователь должен понять,
как ему решить свою проблему.

Твои ответы должны быть развернутыми, но не избыточными.
'''


class SaigaLLM:
    __slots__ = ['_model', '_tokenizer', '_generation_config']

    _model: AutoModelForCausalLM | None
    _tokenizer: AutoTokenizer | None
    _generation_config: GenerationConfig | None

    def __init__(self):
        self._model = None

    def setup(self):
        self._model = AutoModelForCausalLM.from_pretrained(
            settings.saiga_model_name,
            load_in_8bit=True,
            token=settings.huggingface_token,
            torch_dtype=torch.bfloat16,
            device_map='auto',
        )
        self._model.eval()
        self._tokenizer = AutoTokenizer.from_pretrained(settings.saiga_model_name)
        self._generation_config = GenerationConfig.from_pretrained(settings.saiga_model_name)

    def get_model_output(self, msgs: list[LLMMessage]) -> str:
        assert self._model is not None
        assert self._tokenizer is not None
        assert self._generation_config is not None

        # да снизойдет на авторов библиотек машинного обучения благословение бога типизации!
        # (но видимо не сейчас)
        prompt = self._tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        data = self._tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(self._model.device) for k, v in data.items()}
        output_ids = self._model.generate(**data, generation_config=self._generation_config)[0]
        output_ids = output_ids[len(data["input_ids"][0]):]
        return self._tokenizer.decode(output_ids, skip_special_tokens=True).strip()

    def summarize_user_input(self, user_input: str) -> list[str]:
        def _fetch_problems_from_user_input(msgs: list[LLMMessage]) -> list[str] | None:
            model_output = self.get_model_output(msgs)
            print(model_output)
            return _try_get_problems(model_output)

        msgs = [
            create_message(content=SYSTEM_SUMMARIZATION_PROMPT, role=MessageRole.system),
            create_message(content=user_input)
        ]

        user_problems = _fetch_problems_from_user_input(msgs)

        if user_problems is not None:
            return user_problems

        logger.warning('первый вывод суммаризатора неудачный на входе: `%s`', user_input)

        msgs.extend(
            [
                create_message(content=ASSISTANT_ADDITIONAL_SUMMARIZATION_PROMPT, role=MessageRole.assistant),
                create_message(content=user_input)
            ],
        )

        user_problems = _fetch_problems_from_user_input(msgs)
        if user_problems is not None:
            return user_problems

        logger.error('моделька облажалась дважды на входе: `%s`', user_input)
        return []

    def construct_user_response(self, history: list[str], instructions: list[str]):
        msgs = [
            create_message(content=SYSTEM_COMBINE_RESPONSE_PROMBP, role=MessageRole.system),
            create_message(content='ИНСТРУКЦИИ:\n' + '\n'.join(instructions), role=MessageRole.assistant),
            create_message(content='\nИСТОРИЯ ПОЛЬЗОВАТЕЛЯ\n' + '\n'.join(history), role=MessageRole.user),
        ]
        return self.get_model_output(msgs)


def create_message(content: str, role: MessageRole = MessageRole.user) -> LLMMessage:
    return LLMMessage({'role': role, 'content': content})


def _try_get_problems(text: str, problems_key: str = 'problems') -> list[str] | None:
    try:
        problems_list = json.loads(text).get(problems_key)
        assert isinstance(problems_list, list)
        for problem in problems_list:
            assert isinstance(problem, str)
    except Exception:
        return None

    return problems_list
