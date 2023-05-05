from typing import List
from tinydb import TinyDB, Query
import datetime
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
        self.actualizada = datetime.datetime.now().strftime('%Y-%m-%d')


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

def mostrar_menu():
    print("Selecciona una opción:")
    print("1. Agregar tarea")
    print("2. Agregar varias tareas")
    print("3. Traer tarea")
    print("4. Actualizar estado de tarea")
    print("5. Eliminar tarea")
    print("6. Traer todas las tareas")
    print("7. Salir")

def input_valido(mensaje: str, predeterminado: str = "") -> str:
    valor = input(mensaje)
    return valor if valor.strip() != "" else predeterminado

if __name__ == "__main__":
    db_path = "tareas.json"
    admin_tarea = AdminTarea(db_path)

    corriendo = True
    while corriendo:
        mostrar_menu()
        opcion = input_valido("Ingrese una opción: ")

        if opcion == "1":
            titulo = input_valido("Ingrese el título de la tarea: ")
            descripcion = input_valido("Ingrese la descripción de la tarea: ")
            estado = input_valido("Ingrese el estado de la tarea: ")

            if not all([titulo, descripcion, estado]):
                print("Todos los campos son requeridos")
                continue

            tarea = Tarea(titulo=titulo, descripcion=descripcion, estado=estado, creada=datetime.datetime.now().strftime('%Y-%m-%d'), actualizada=datetime.datetime.now().strftime('%Y-%m-%d'))
            tarea_id = admin_tarea.agregar_tarea(tarea)
            print(f"Tarea agregada con ID {tarea_id}")

        elif opcion == "2":
            tareas = []
            cantidad_tareas = int(input_valido("Ingrese la cantidad de tareas que desea agregar: "))
            for i in range(cantidad_tareas):
                titulo = input_valido(f"Ingrese el título de la tarea {i+1}: ")
                descripcion = input_valido(f"Ingrese la descripción de la tarea {i+1}: ")
                estado = input_valido(f"Ingrese el estado de la tarea {i+1}: ")
                tarea = Tarea(titulo=titulo, descripcion=descripcion, estado=estado, creada=datetime.datetime.now().strftime('%Y-%m-%d'), actualizada=datetime.datetime.now().strftime('%Y-%m-%d'))
                tareas.append(tarea)
            tarea_ids = admin_tarea.agregar_tareas(tareas)
            print(f"Se agregaron las tareas con IDs {tarea_ids}")

        elif opcion == "3":
            tarea_id = int(input_valido("Ingrese el ID de la tarea que desea traer: "))
            tarea = admin_tarea.traer_tarea(tarea_id)
            if tarea:
                print(tarea.to_dict())
            else:
                print(f"No se encontró ninguna tarea con el id {tarea_id}")

        elif opcion == "4":
            tarea_id = int(input_valido("Ingrese el ID de la tarea que desea actualizar: "))
            estado = input_valido("Ingrese el nuevo estado de la tarea: ")
            admin_tarea.actualizar_estado_tarea(tarea_id, estado)
            print("Tarea actualizada")

        elif opcion == "5":
            tarea_id = int(input_valido("Ingrese el ID de la tarea que desea eliminar: "))
            admin_tarea.eliminar_tarea(tarea_id)
            print("Tarea eliminada")

        elif opcion == "6":
            tareas = admin_tarea.traer_todas_tareas()
            if not tareas:
                print("No hay tareas")
                print()
                continue
            for tarea in tareas:
                print(tarea.to_json())

        elif opcion == "7":
            print("Saliendo...")
            corriendo = False

        else:
            print("Opción inválida. Intente de nuevo.")
        
        print() # Salto de línea