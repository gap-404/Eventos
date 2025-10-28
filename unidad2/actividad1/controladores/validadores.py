import re
class Validaciones():
    
    def __init__(self):
        pass

    def validarLetras(self, valor: str):
        patron = re.compile(r"^[A-Za-z ]*$")
        resultado = patron.match(valor.get())is not None
        if not resultado:
            return False
        return True
