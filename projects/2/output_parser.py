# from pydantic import BaseModel, Field
# from langchain_openai import ChatOpenAI


# class AnalisisTexto(BaseModel):
#     resumen: str = Field(description="Resumen breve del texto")
#     sentimiento: str = Field(
#         description="Sentimiento del texto (Positivo, neutro o negativo)"
#     )


# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

# structured_llm = llm.with_structured_output(AnalisisTexto)

# test_prompt = "Me encantó la pelicula de zootopia y me parecio graciosa la parte final, estuvo decente creo yo"

# resultado = structured_llm.invoke(f"Analiza el siguiente texto: {test_prompt}")

# print(resultado)

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(
        description="Sentimiento del texto (Positivo, neutro o negativo)"
    )


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

parser = PydanticOutputParser(pydantic_object=AnalisisTexto)

prompt = PromptTemplate(
    template="Analiza el siguiente texto:\n{texto}\n{format_instructions}",
    input_variables=["texto"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

resultado = chain.invoke(
    {
        "texto": "Me encantó la pelicula de zootopia y me parecio graciosa la parte final, estuvo decente creo yo"
    }
)

print(resultado)
