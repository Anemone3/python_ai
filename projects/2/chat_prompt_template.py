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
# esto es para ver el type y el contenido de nuestro mensajes estructurados



# sin chain, doble invoke ->

my_origin_text = "Soy ariku, el viernes ire de paseo."

# 1️⃣ Construimos los mensajes
mensajes = chat_prompt.invoke({"texto_input": my_origin_text})

# Puedes ver qué tipo devuelve:
# for m in mensajes:
#     print(f"{type(m)}: {m.content}")

# 2️⃣ Enviamos los mensajes al modelo
response_manual = llm.invoke(mensajes)

print("=== DOBLE PASO ===")
print("origin:", my_origin_text)
print("translate:", response_manual.content)


#  con chain ->

chain = chat_prompt | llm

response = chain.invoke({"texto_input": my_origin_text})

print("\n=== CON CHAIN ===")
print("origin:", my_origin_text)
print("translate:", response.content)
