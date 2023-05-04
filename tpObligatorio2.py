# Crear una aplicación de línea de comandos para administrar una lista de tareas. La aplicación permitirá al usuario agregar, ver, actualizar y eliminar tareas.

# Requisitos:

# Utiliza TinyDB para almacenar las tareas en una base de datos.

# Crea una clase Tarea que tenga las siguientes propiedades: id, titulo, descripción, estado, creada y actualizada.

# Crea una clase Administrador de Tareas (AdminTarea) que maneje la interacción con la base de datos TinyDB. La clase debe tener los siguientes métodos:

# agregar_tarea(tarea: Tarea) -> int: Agrega una nueva tarea a la base de datos y devuelve su ID.
# traer_tarea(tarea_id: int) -> Task: Obtiene una tarea de la base de datos según su ID y devuelve una instancia de la clase Tarea.
# actualizar_estado_tarea(tarea_id: int, estado: str): Actualiza el estado de una tarea en la base de datos según su ID.
# eliminar_tarea(tarea_id: int): Elimina una tarea de la base de datos según su ID.
# traer_todas_tareas() -> List[Tarea]: Obtiene todas las tareas de la base de datos y devuelve una lista de instancias de la clase Task.

from typing import List
from tinydb import TinyDB, Query
import datetime
from datetime import datetime
import json


class ModeloBase:
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Tarea(ModeloBase):
    def __init__(self, titulo: str, descripcion: str, estado: str, creada: str, actualizada: str):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.creada = creada
        self.actualizada = actualizada
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "creada": self.creada,
            "actualizada": self.actualizada
        }

    def to_json(self):
        return json.dumps(self.to_dict())
    
    def actualizar_fecha_actualizacion(self):
        self.actualizada = datetime.now().strftime('%Y-%m-%d')


class AdminTarea:
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)

    def agregar_tarea(self, tarea: Tarea) -> int:
        tarea_dict = tarea.to_dict()
        tarea_id = self.db.insert(tarea_dict)
        return tarea_id

    def agregar_tareas(self, tareas: List[Tarea]) -> List[int]:
        tareas_dict = [tarea.to_dict() for tarea in tareas]
        tarea_ids = self.db.insert_multiple(tareas_dict)
        return tarea_ids

    def traer_tarea(self, tarea_id: int) -> Tarea:
        tarea_dict = self.db.get(doc_id=tarea_id)
        tarea = Tarea.from_dict(tarea_dict)
        return tarea

    def actualizar_estado_tarea(self, tarea_id: int, estado: str):
        tarea = self.traer_tarea(tarea_id)
        tarea.estado = estado
        tarea.actualizar_fecha_actualizacion()
        tarea_dict = tarea.to_dict()
        self.db.update(tarea_dict, doc_ids=[tarea_id])

    def eliminar_tarea(self, tarea_id: int):
        self.db.remove(doc_ids=[tarea_id])

    def traer_todas_tareas(self) -> List[Tarea]:
        tareas_dicts = self.db.all()
        tareas = list(map(Tarea.from_dict, tareas_dicts))
        return tareas


if __name__ == "__main__":
    db_path = "dbb.json"
    admin_tarea = AdminTarea(db_path)

    corriendo = True
    while corriendo:
        print("1. Agregar tarea")
        print("2. Ver tarea")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Ver todas las tareas")
        print("6. Salir")
        opcion = input("Ingrese una opcion: ")
        
        if opcion == "1":
            titulo = input("Ingrese el titulo: ")
            descripcion = input("Ingrese la descripcion: ")
            estado = input("Ingrese el estado: ")
            creada = input("Ingrese la fecha de creacion (YYYY-MM-DD): ")
            actualizada = input("Ingrese la fecha de actualizacion (YYYY-MM-DD): ")
            
            if not all([titulo, descripcion, estado, creada, actualizada]):
                print("Todos los campos son requeridos")
                continue
            
            tarea = Tarea(titulo, descripcion, estado, creada, actualizada)
            tarea_id = admin_tarea.agregar_tarea(tarea)
            print(f"La tarea se agrego con el id {tarea_id}")
            
        elif opcion == "2":
            tarea_id = int(input("Ingrese el id de la tarea: "))
            tarea = admin_tarea.traer_tarea(tarea_id)
            if tarea:
                print(tarea.to_json())
            else:
                print(f"No se encontró ninguna tarea con el id {tarea_id}")
            
        elif opcion == "3":
            tarea_id = int(input("Ingrese el id de la tarea: "))
            estado = input("Ingrese el nuevo estado: ")
            admin_tarea.actualizar_estado_tarea(tarea_id, estado)
            print("La tarea se actualizó correctamente")
            
        elif opcion == "4":
            tarea_id = int(input("Ingrese el id de la tarea: "))
            admin_tarea.eliminar_tarea(tarea_id)
            print("La tarea se eliminó correctamente")
            
        elif opcion == "5":
            tareas = admin_tarea.traer_todas_tareas()
            if not tareas:
                print("No hay tareas")
                print()
                continue
            for tarea in tareas:
                print(tarea.to_json())
                
        elif opcion == "6":
            print("Gracias por usar el programa")
            corriendo = False
            
        else:
            print("Opción inválida")
        
        print()  # Imprimir una línea en blanco para separar los mensajes de las diferentes iteraciones
