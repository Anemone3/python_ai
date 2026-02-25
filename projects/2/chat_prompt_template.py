from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un traductor del español al japones muy preciso."),
        ("human", "{texto_input}"),
    ]
)

# mensajes = chat_prompt.format_messages(
#     texto_input="Soy ariku, el viernes ire de paseo."
# )

# for m in mensajes:
#     print(f"{type(m)}: {m.content}")


chain = chat_prompt | llm


my_origin_text = "Soy ariku, el viernes ire de paseo."
response = chain.invoke({"texto_input": my_origin_text})

print("origin:", my_origin_text)
print("translate:",response.content)