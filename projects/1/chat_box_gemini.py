from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

pregunta = "¿Cuál es el roadmap 2026 para ser ai enginer?"

print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)

print("Response: ", respuesta.content)
