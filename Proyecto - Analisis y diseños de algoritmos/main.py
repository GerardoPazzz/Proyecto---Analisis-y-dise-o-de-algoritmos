print("Hola soy Gerardo")
print("hola soy sebastian")
print("HOLA #2")
print("Hola soy Richard")
print("hello")
class Persona:
    def __init__(self,nombre,edad):
        self.nombre=nombre
        self.edad=edad
    def imprimirDatos(self):
        print("El nombre de la persona es ",self.nombre)
persona1=Persona("Jose",22)  #Persona persona1=new Persona()
persona1.imprimirDatos()