from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
import json

# Configuración del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class Sentimiento(BaseModel):
    sentimiento: Literal["positivo", "negativo", "neutro"]
    razon: str
    anime: str


"""
La temperatura controla qué tan “aleatoria” es la respuesta del modelo:

Temperatura alta (ej. 0.7 - 1.0) → más creatividad, más variedad.

Temperatura baja (ej. 0 - 0.2) → más precisión, menos variación.

Temperatura = 0 → el modelo siempre elige la opción más probable.
"""


def generate_summary(text):
    """
    Genera un resumen del anime o manga que será pasado por parametro
    """
    prompt = f"""
    Resume el siguiente texto en máximo 5 líneas.
    No identifiques la obra, solo resume el contenido proporcionado.

    Texto:
    {text}
    """
    return llm.invoke(prompt).content


def preprocess(text: str):
    """Limpia el texto eliminando espaciados extra, y limitando la longitud"""
    return text.strip()[:500]


def analizar_sentimientos(text):
    response = llm.invoke(
        f"""
        Analiza el sentimiento general del texto.

        Devuelve estrictamente este JSON:
        {{
          "sentimiento": "positivo | negativo | neutro",
          "razon": "explicacion",
          "anime": "el anime que esta describiendo el texto"
        }}

        Texto:
        {text}
        """
    )

    data = json.loads(response.content)
    return Sentimiento(**data)


def merge_result(data):
    summary = data["resumen"]
    sentiment = data["sentimiento_data"]
    return {
        "resumen": summary,
        "anime": sentiment.anime,
        "sentimiento": sentiment.sentimiento,
        "razon": sentiment.razon,
    }




# def process_one(texto):
#     # ya que esto se puede ejecutar secuencialmente, podemos usar RunnableParallel
#     # resumen = generate_summary(texto)  # llama llm 1
#     # sentimiento_obj = analizar_sentimientos(texto) # llama llm 2

#     return merge_result(resumen,sentimento_objet)
# aqui se genera el resumen, sentimiento segun el texto ya formateado con el antiguo proceso
#process = RunnableLambda(process_one)

## usando RunnableParallel ->

summary_branch = RunnableLambda(generate_summary)
sentiment_branch = RunnableLambda(analizar_sentimientos)
merger_result = RunnableLambda(merge_result)

parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

# Runnables
# Aqui solo limpia el texto enviado si es mas de 500 lo limita
preprocesador = RunnableLambda(preprocess)



chain = preprocesador | parallel_analysis | merger_result

textos_prueba = [
    "Un joven aspirante a pirata obtiene un poder elástico tras comer una fruta misteriosa. Con el sueño de encontrar el tesoro más grande del mundo, reúne una tripulación diversa y navega por mares peligrosos enfrentando gobiernos corruptos, piratas legendarios y secretos del pasado.",
    "Un chico sin habilidades especiales nace en un mundo donde casi todos poseen superpoderes. A pesar de las dificultades, logra ingresar a una academia de héroes para demostrar que el esfuerzo y la determinación pueden competir contra talentos extraordinarios.",
    "Un espadachín errante marcado por un pasado sangriento intenta vivir sin volver a matar. Sin embargo, antiguos enemigos y nuevas amenazas lo obligan a enfrentar su historia mientras protege a quienes le ofrecen una segunda oportunidad.",
    "Un grupo de estudiantes es transportado a un mundo de fantasía donde deben superar pruebas mortales impuestas por una entidad desconocida. Las alianzas, traiciones y sacrificios se vuelven inevitables mientras luchan por regresar a casa.",
    "En una sociedad donde ciertos individuos pueden manipular la energía espiritual para combatir maldiciones, un estudiante termina compartiendo su cuerpo con una poderosa entidad ancestral. Mientras aprende a controlar esa fuerza, se ve envuelto en conflictos cada vez más peligrosos.",
    "Un universitario tímido sobrevive a un encuentro mortal tras recibir un trasplante que lo transforma en un híbrido entre humano y depredador. Incapaz de alimentarse como antes y rechazado por ambos mundos, debe aprender a sobrevivir en una sociedad secreta donde criaturas ocultas cazan para vivir. Mientras intenta proteger a sus amigos humanos, se enfrenta a organizaciones que exterminan a los de su especie y a su propia naturaleza cada vez más violenta.",
]

# for text in textos_prueba:
#     print(f"Anime: {text}")
#     result = chain.invoke(text)
#     print(f"Result: {result}")
#     print("=" * 73)

# -> batch usando RunnableParallel
result_batch = chain.batch(textos_prueba)

print(result_batch)

# Casos de usos mas reales, se puede sacar para saber la reseña de los usuarios de tipos de productos
# para hacer analisis o mas cosas.