class ParImpar:
    """Clase encargada del ejercicio 1."""

    def __init__(self, numero):
        self.numero = numero

    def resolver(self):
        if self.numero % 2 == 0:
            return "El número es par"
        else:
            return "El número es impar"


class TablaMultiplicar:
    """Clase encargada del ejercicio 2."""

    def __init__(self, numero):
        self.numero = numero

    def resolver(self):
        tabla = []

        for i in range(1, 11):
            resultado = self.numero * i
            tabla.append(f"{self.numero} x {i} = {resultado}")

        return tabla


class AdivinaNumero:
    """Clase encargada del ejercicio 3."""

    def __init__(self, numero_secreto):
        self.numero_secreto = numero_secreto
        self.acertado = False

    def comprobar(self, intento):
        while True:
            if intento < self.numero_secreto:
                return "El número secreto es mayor"

            elif intento > self.numero_secreto:
                return "El número secreto es menor"

            else:
                self.acertado = True
                return "¡Correcto! Adivinaste el número"
