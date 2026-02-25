from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

import random
import json


# class
class Curso:
    def __init__(self, area, cursos, nota_promedio):
        self.area = area
        self.cursos = cursos
        self.nota_promedio = nota_promedio

    def __str__(self):
        return f"area={self.area}, cursos={self.cursos}, nota_promedio={self.nota_promedio}"


# globals
list_areas_user = []
history_messages = []
system_prompts = []

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# templates

prompt_template_area = PromptTemplate(
    template="""
        Eres un director de una escuela, y estás asignado a seleccionar temas de estudis segun la categoria de cursos.

        Se necesita cursos de esta area: {area}.

    {{
    "cursos": ["curso1", "curso2", "curso3"]
    }}

    No agregues texto adicional.
    """,
    input_variables=["area"],
)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un instructor de varias profesiones, y tienes el trabajo de poder ayudar a los estudiantes segun el area que necesitan apoyo",
        ),
        (
            "human",
            "Historial de conversación: {historial}.\\nPregunta actual: {pregunta}",
        ),
    ]
)


# chains
chain_area = prompt_template_area | llm
chain_chat = chat_prompt_template | llm


# AI functions
def generar_temas(area: str):
    # sin chain:
    # format_prompt = prompt_template_area.format(area=area)
    # return llm.invoke(format_prompt).content

    # con chain
    response = chain_area.invoke({"area": area})
    data = json.loads(response.content)
    return data["cursos"]


# helpers
def user_options(key_exit: int | None) -> int:
    key_result = int(input("Selección: "))
    if key_result != key_exit:
        return key_result
    return 0


def print_list_enumerable(list):
    for i, element in enumerate(list):
        print(f"{i + 1}: {element}")


def init():
    title = f"{'=' * 10} CHAT BOX {'=' * 10}"
    print(title)

    track_state = True
    operation_task = ["Agregar tarea", "Ver tareas", "Generar plan con IA", "Salir"]

    while track_state:
        print_list_enumerable(operation_task)

        val = user_options(key_exit=len(operation_task))

        if val == 0:
            track_state = False

        print(operation_task[val - 1])

        match val:
            case 1:
                task_input = input("task: ")
                temas_area = generar_temas(task_input)
                rng_nota = random.randint(0, 10)
                curso_body = Curso(
                    area=task_input, cursos=temas_area, nota_promedio=rng_nota
                )

                print("Curso generado por IA: ", curso_body)

                list_areas_user.append(curso_body)
                pass
            case 2:
                for item in list_areas_user:
                    print(f"Area: {item.area}")
                    print(f"Cursos: {item.cursos}")
                    print(f"Nota Promedio: {item.nota_promedio}")

                pass
            case 3:

                for i, item in enumerate(list_areas_user):
                    print(f"{'='*5} {i + 1} {item.area} {'='*5} ")
                    print(f"Cursos: {item.cursos}")
                    print(f"Nota Promedio: {item.nota_promedio}")

                user_seleccion = int(input("Selecciona un curso: ")) - 1
                print(list_areas_user[user_seleccion])

                print("Generando resumen del curso seleccionado..")
                question = f"Quiero que me recomiendes como poder mejorar mi nota de este curso:\n{list_areas_user[user_seleccion]}"
                print("User: ", question)
                response = chain_chat.invoke(
                    {"historial": history_messages, "pregunta": question}
                ).content

                history_messages.append(response)
                print("Instructor: ", response)

                pass


if __name__ == "__main__":
    init()
