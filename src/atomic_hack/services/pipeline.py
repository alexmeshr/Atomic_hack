from atomic_hack.services import llm


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
