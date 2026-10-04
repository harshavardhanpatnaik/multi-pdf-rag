from langchain_core.prompts import ChatPromptTemplate


def prompt():
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """
            Take the context and give answers from it only 
            
            if answers are not found from the context simplfiy give i dont know lanjakodaka
            
            """,
            ),
            (
                "user",
                """
            context:{context}
            question : {question}
            """,
            ),
        ]
    )

    return prompt
