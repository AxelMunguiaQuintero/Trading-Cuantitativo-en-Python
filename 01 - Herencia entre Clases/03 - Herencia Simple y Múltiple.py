# -*- coding: utf-8 -*-
# Definir clase base "Persona"
class Persona:
    
    def __init__(self, nombre):
        self.nombre = nombre
        
    def presentarse(self):
        print("Hola, mi nombre es", self.nombre)
        

class Actividad:
    
    def __init__(self, nombre_actividad):
        self.nombre_actividad = nombre_actividad
        
    def realizar_actividad(self):
        pass
    
# Clase "Estudiante" que hereda de "Persona" y "Actividad"
class Estudiante(Persona, Actividad):
    
    def __init__(self, nombre, curso, nombre_actividad):
        # Inicializar 
        Persona.__init__(self, nombre)
        Actividad.__init__(self, nombre_actividad)
        self.curso = curso
        
    def realizar_actividad(self):
        print(f"Soy {self.nombre} y estoy participando en la actividad: {self.nombre_actividad}")
        
    def tareas(self):
        print(f"Hola, soy {self.nombre}, estoy haciendo mi tarea y actualmente curso:", self.curso)
        
    
# Generar instancia
estudiante1 = Estudiante(nombre="Juan", curso="10° Grado", nombre_actividad="Fútbol")
estudiante1.presentarse()
estudiante1.realizar_actividad()
estudiante1.tareas()

# Recordatorio:
#   - La herencia de clases en Python permite a las subclases heredar atributos y métodos de las super clases, promoviendo
#     la reutilización de código y la modularidad del sistema.
