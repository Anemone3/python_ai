from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# pregunta = "¿Cuál es el roadmap 2026 para ser ai enginer?"

# print("Pregunta: ", pregunta)

# respuesta = llm.invoke(pregunta)

# print("Response: ", respuesta.content)

"""
-- from langchain.prompts import PromptTemplate
Plantilla Prompt:
Componente reutilizable, se podria usar de manera dinamica en tiempo de ejecución
"""

plantilla = PromptTemplate(
    input_variables=["nombre","pregunta"],
    template="""
        Saluda al usuario con su nombre:
        Nombre del usuario: {nombre}
        Asistente:
        Responde la siguiente pregunta {pregunta}
    """,
)

# encadenamos el objeto template con el chat (llm), el pipeline | <- tambien se conoce como LCEL
chain = plantilla | llm

# un detalle importante es que si agregas al pipe este parser = StrOutputParser(), supuestamente te responde en texto
# y no en AIMessage(content="Hola Ariku 👋"), aunque en este caso no lo veo necesario porque me responde en texto

# se insertaria el objeto en el template

pregunta = input("Pregunta: ")

full_content = ""

for chunk in chain.stream({"nombre":"Ariku", "pregunta": pregunta}):
    res = chunk.content
    print(res)
    full_content += res 

print("Asistente: " , full_content)