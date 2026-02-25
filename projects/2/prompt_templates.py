from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"

prompt = PromptTemplate(template=template, input_variables=["producto"])

# #  Formatear el prompt
# prompt_formateado = prompt.invoke({"producto": "café orgánico"})

# # Enviar al modelo
# respuesta = llm.invoke(prompt_formateado)

#print(respuesta.content)


# con langchain ->
chain = prompt | llm

# Ejecutamos todo en un solo paso
respuesta = chain.invoke({"producto": "café orgánico"})

print(respuesta.content)
