from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Response de manera {tono}"
)

plantilla_human = HumanMessagePromptTemplate.from_template(
    " Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([plantilla_sistema, plantilla_human])


messages_prompt = chat_prompt.format_messages(
    rol="nutricionista",
    especialidad="dietas veganas",
    tono="profesional pero accesible",
    tema="proteinas vegetales",
    pregunta="¿Cuáles son las mejores fuentes de proteina vegana para un atetla profesional?",
)

for m in messages_prompt:
    print(m.content)
