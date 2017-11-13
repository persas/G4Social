def calcula_gastos(ingreso, gasto, reto):
    sobra = ingreso - gasto - reto
    if sobra < 400:
        return -1
    else:
        gastos = []
        comida = 300 + sobra * 0.2
        casa = 60 + sobra * 0.2
        ocio = 39 + sobra * 0.60
        gastos.append(gasto, comida, casa, ocio)

        return gastos

def nuevo_ingreso(gastos, income):

    gastos[1] += income*0.2
    gastos[2] += income*0.2
    gastos[3] += income*0.6
    return gastos



