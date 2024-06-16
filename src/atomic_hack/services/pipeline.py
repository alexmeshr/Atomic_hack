from time import sleep

from atomic_hack.entities import chat
from atomic_hack.repositories import pg_chat
from atomic_hack.services import embeddings, llm
from atomic_hack.settings import settings


def summarization_example():
    saiga = llm.SaigaLLM()
    inputs = [
        "У меня стучит подвеска на машине, что делать?",
        "Непонятный стук в двигателе, а еще дверь плохо закрывается",
        "Хорошая погода на улице, не правда ли?",
        "Долбанный голубь насрал на крышу!!1! как я зол",
    ]
    saiga.setup()
    for user_input in inputs:
        print(
            user_input,
            saiga.summarize_user_input(user_input),
            sep='\n',
            end='\n\n',
        )


def _fetch_summarized_problems(user_input: str) -> list[str]:
    saiga = llm.SaigaLLM()
    saiga.setup()
    out = saiga.summarize_user_input(user_input)
    del saiga
    return out


def _get_k_closest(problem: str, k: int) -> list[str]:
    pgv = embeddings.PGVectorStorage()
    pgv.setup()

    closest_docs = pgv.get_k_closest(problem, k=k)
    del pgv
    return [doc.page_content + f" на странице {doc.metadata['page']} в инструкции {doc.metadata['source']}" for doc in closest_docs]


def _construct_response(history: list[str], instructions: list[str]) -> str:
    saiga = llm.SaigaLLM()
    saiga.setup()
    out = saiga.construct_user_response(history=history, instructions=instructions)
    del saiga
    return out


def process_single_user_input(session: list[str]) -> str:
    last_user_msg = session[-1]

    user_problems = _fetch_summarized_problems(last_user_msg)
    if not user_problems:
        return (
            'Извините, мы не смогли понять проблему. '
            'Попробуйте написать подробнее или обратиться к живому человеку.'
        )

    K = 3
    instructions: list[str] = [
        instruction
        for problem in user_problems
        for instruction in _get_k_closest(problem, k=K)
    ]

    return _construct_response(history=session, instructions=instructions)


def main_pipeline():
    while True:
        oldest_session = pg_chat.get_oldest_unprocessed_session()
        if oldest_session is None:
            print('no task found --> sleep')
            sleep(settings.llm_worker_delay_seconds)
            continue

        print(f'found message({oldest_session[0].message_id}) in session({oldest_session[0].session_id})')

        history = [msg_obj.message for msg_obj in oldest_session if msg_obj.sender == chat.MessageSender.from_user]

        response = process_single_user_input(history)

        session_id = oldest_session[0].session_id
        pg_chat.insert_message(response, session_id, chat.MessageSender.from_support)
