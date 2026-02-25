from langchain_core.runnables import RunnableLambda

paso_1 = RunnableLambda(lambda x: f"Numero {x}")

def duplicar_text(texto):
    return [texto] * 2

paso_2 = RunnableLambda(duplicar_text)


# primero recibe un valor, en el paso 1 se convierte a texto, y luego pasa al segundo donde se duplica
chain = paso_1 | paso_2


result = chain.invoke("ariku")

print(result)