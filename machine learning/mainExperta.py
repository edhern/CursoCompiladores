import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from experta import *
from datetime import datetime
import collections
import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Monkey patch para evitar error de compatibilidad con collections.Mapping en experta
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping


# Conexión a SQL Server
def conectar_bd():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=LAPTOP-9NOGDVI8\\SQLSERVER2022DV;"  
        "DATABASE=SistemaDiagnostico;"  
        "UID=sa;" 
        "PWD=secreto123+;"  
    )
    return conn


# Función para insertar una nueva enfermedad
def agregar_enfermedad():
    nombre = entry_enfermedad.get()
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Enfermedad (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Enfermedad agregada")
    entry_enfermedad.delete(0, tk.END)
    cargar_enfermedades()

# Función para insertar un nuevo síntoma
def agregar_sintoma():
    nombre = entry_sintoma.get()
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Sintoma (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Síntoma agregado")
    entry_sintoma.delete(0, tk.END)
    cargar_sintomas()

# Función para asociar un síntoma a una enfermedad
def asociar_sintoma():
    enfermedad = combo_enfermedad.get()
    sintoma = combo_sintoma.get()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_enfermedad FROM Enfermedad WHERE nombre = ?", (enfermedad,))
    id_enfermedad = cursor.fetchone()[0]
    
    cursor.execute("SELECT id_sintoma FROM Sintoma WHERE nombre = ?", (sintoma,))
    id_sintoma = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO EnfermedadSintoma (id_enfermedad, id_sintoma) VALUES (?, ?)", (id_enfermedad, id_sintoma))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Síntoma asociado a la enfermedad")

# Función para cargar las enfermedades en el combobox
def cargar_enfermedades():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Enfermedad")
    enfermedades = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    combo_enfermedad['values'] = enfermedades

# Función para cargar los síntomas en el combobox
def cargar_sintomas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Sintoma")
    sintomas = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    combo_sintoma['values'] = sintomas
    combo_sintoma1['values'] = sintomas
    combo_sintoma2['values'] = sintomas
    combo_sintoma3['values'] = sintomas


# Definir la clase Condiciones para el sistema experto
class Condiciones(Fact):
    """Información sobre las condiciones basadas en los síntomas."""
    pass

# Sistema experto con reglas estáticas para cada enfermedad
class SistemaExpertoDiagnostico(KnowledgeEngine):
    """Clase del sistema experto que define las reglas para diagnosticar enfermedades."""

    @Rule(Condiciones(fiebre=True, flujo_nasal=True, dolor_de_cabeza=True))
    def diagnosticar_gripe(self):
        self.diagnostico_final = "Gripe"
        print("Diagnóstico: Gripe.")

    @Rule(Condiciones(tos=True, fiebre=True, dolor_de_garganta=True))
    def diagnosticar_infeccion_garganta(self):
        self.diagnostico_final = "Infección de garganta"
        print("Diagnóstico: Infección de garganta.")

    @Rule(Condiciones(fiebre=True, dolor_de_cuerpo=True, perdida_sentido_olfato=True))
    def diagnosticar_covid(self):
        self.diagnostico_final = "Covid"
        print("Diagnóstico: Covid.")

    @Rule(Condiciones(fiebre=True, dolor_de_cabeza=True, dolor_lumbar=True))
    def diagnosticar_dengue(self):
        self.diagnostico_final = "Dengue"
        print("Diagnóstico: Dengue.")

# Función para obtener los síntomas registrados
def obtener_sintomas_registrados():
    """Obtener la lista de síntomas almacenados en la base de datos."""
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Sintoma")
    sintomas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sintomas

# Función para guardar el diagnóstico en la base de datos
def guardar_diagnostico(nombre_paciente, resultado_diagnostico):
    """Guardar el nombre del paciente y el diagnóstico en la base de datos."""
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO DiagnosticoPaciente (nombre_paciente, resultado_diagnostico) VALUES (?, ?)",
        (nombre_paciente.strip(), resultado_diagnostico.strip())  # Usar strip() para eliminar espacios adicionales
    )
    conn.commit()
    conn.close()
    print(f"Diagnóstico guardado: {nombre_paciente} - {resultado_diagnostico}")

# Función para obtener los diagnósticos registrados
def obtener_diagnosticos_registrados():
    """Obtener todos los diagnósticos registrados en la base de datos."""
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_paciente, resultado_diagnostico, fecha FROM DiagnosticoPaciente ORDER BY fecha DESC")
    diagnosticos = cursor.fetchall()
    conn.close()
    return diagnosticos

# Función para actualizar el listado de diagnósticos en la interfaz gráfica
def actualizar_listado_diagnosticos():
    """Actualizar el Treeview con los diagnósticos obtenidos de la base de datos."""
    diagnosticos = obtener_diagnosticos_registrados()
    listado_diagnosticos.delete(*listado_diagnosticos.get_children())  # Elimina las filas actuales
    for diag in diagnosticos:
        # Asegurar que los valores se muestren como cadenas sin espacios ni caracteres adicionales
        nombre_paciente, resultado, fecha = diag
        listado_diagnosticos.insert("", tk.END, values=(nombre_paciente.strip(), resultado.strip(), fecha))

# Función para diagnosticar una enfermedad basándose en los síntomas seleccionados
def diagnosticar():
    # Obtener los síntomas seleccionados de los comboboxes
    sintomas_seleccionados = [combo_sintoma1.get(), combo_sintoma2.get(), combo_sintoma3.get()]
    nombre_paciente = entry_paciente.get().strip()  # Remover espacios innecesarios en el nombre del paciente

    # Verificar que se hayan seleccionado todos los síntomas y se haya ingresado el nombre del paciente
    if not all(sintomas_seleccionados) or not nombre_paciente:
        messagebox.showwarning("Advertencia", "Por favor, ingrese su nombre y seleccione todos los síntomas antes de diagnosticar.")
        return

    print(f"Sintomas seleccionados por el usuario: {sintomas_seleccionados}")  # Mensaje de depuración

    # Normalizar los nombres de los síntomas
    sintomas_normalizados = [sintoma.replace(" ", "_") for sintoma in sintomas_seleccionados]
    print(f"Sintomas normalizados: {sintomas_normalizados}")  # Mensaje de depuración

    # Crear un diccionario con las condiciones basadas en los síntomas seleccionados
    condiciones_usuario = {sintoma: True for sintoma in sintomas_normalizados}
    print(f"Condiciones creadas para el usuario: {condiciones_usuario}")  # Mensaje de depuración

    # Crear y ejecutar el sistema experto
    sistema_experto = SistemaExpertoDiagnostico()
    sistema_experto.reset()
    sistema_experto.diagnostico_final = None  # Inicializar el resultado del diagnóstico
    sistema_experto.declare(Condiciones(**condiciones_usuario))
    sistema_experto.run()

    # Verificar si se encontró un diagnóstico
    if sistema_experto.diagnostico_final:
        resultado_diagnostico = sistema_experto.diagnostico_final
        messagebox.showinfo("Diagnóstico", f"La enfermedad que tengo es: {resultado_diagnostico}")
        print(f"Diagnóstico final: {resultado_diagnostico}")
        
        # Guardar el diagnóstico en la base de datos
        guardar_diagnostico(nombre_paciente, resultado_diagnostico)
        
        # Actualizar el listado de diagnósticos
        actualizar_listado_diagnosticos()
    else:
        messagebox.showinfo("Diagnóstico", "No se encontró ninguna coincidencia con las enfermedades en la base de datos.")
        print("No se encontraron coincidencias")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Sistema de Diagnóstico")


# Sección para agregar enfermedades y síntomas, y asociar síntomas a enfermedades
frame_enfermedad = tk.Frame(root)
frame_enfermedad.pack(pady=10)
tk.Label(frame_enfermedad, text="Agregar Enfermedad:").pack(side=tk.LEFT)
entry_enfermedad = tk.Entry(frame_enfermedad)
entry_enfermedad.pack(side=tk.LEFT)
tk.Button(frame_enfermedad, text="Agregar", command=agregar_enfermedad).pack(side=tk.LEFT)

frame_sintoma = tk.Frame(root)
frame_sintoma.pack(pady=10)
tk.Label(frame_sintoma, text="Agregar Síntoma:").pack(side=tk.LEFT)
entry_sintoma = tk.Entry(frame_sintoma)
entry_sintoma.pack(side=tk.LEFT)
tk.Button(frame_sintoma, text="Agregar", command=agregar_sintoma).pack(side=tk.LEFT)

frame_asociar = tk.Frame(root)
frame_asociar.pack(pady=10)
tk.Label(frame_asociar, text="Asociar Síntoma a Enfermedad:").pack(side=tk.LEFT)

combo_enfermedad = ttk.Combobox(frame_asociar)
combo_enfermedad.pack(side=tk.LEFT)

combo_sintoma = ttk.Combobox(frame_asociar)
combo_sintoma.pack(side=tk.LEFT)

tk.Button(frame_asociar, text="Asociar", command=asociar_sintoma).pack(side=tk.LEFT)



# Sección para ingresar el nombre del paciente
frame_paciente = tk.Frame(root)
frame_paciente.pack(pady=10)
tk.Label(frame_paciente, text="Nombre del Paciente:").pack(side=tk.LEFT)
entry_paciente = tk.Entry(frame_paciente)
entry_paciente.pack(side=tk.LEFT)



# Sección para seleccionar síntomas y diagnosticar
frame_diagnostico = tk.Frame(root)
frame_diagnostico.pack(pady=10)
tk.Label(frame_diagnostico, text="Selecciona Síntomas:").pack()

# Crear los Comboboxes para los síntomas
sintomas_disponibles = obtener_sintomas_registrados()  # Asegurarse de que los síntomas estén disponibles antes de usarse
combo_sintoma1 = ttk.Combobox(frame_diagnostico, values=sintomas_disponibles)
combo_sintoma1.pack()

combo_sintoma2 = ttk.Combobox(frame_diagnostico, values=sintomas_disponibles)
combo_sintoma2.pack()

combo_sintoma3 = ttk.Combobox(frame_diagnostico, values=sintomas_disponibles)
combo_sintoma3.pack()

# Botón para ejecutar el diagnóstico
tk.Button(frame_diagnostico, text="¿Qué enfermedad tengo?", command=diagnosticar).pack(pady=10)

# Sección para mostrar el listado de diagnósticos realizados
frame_listado = tk.Frame(root)
frame_listado.pack(pady=20)
tk.Label(frame_listado, text="Listado de Diagnósticos Realizados:").pack()

# Crear un Treeview para mostrar los diagnósticos realizados
listado_diagnosticos = ttk.Treeview(frame_listado, columns=("Paciente", "Diagnóstico", "Fecha"), show='headings')
listado_diagnosticos.heading("Paciente", text="Paciente")
listado_diagnosticos.heading("Diagnóstico", text="Diagnóstico")
listado_diagnosticos.heading("Fecha", text="Fecha")
listado_diagnosticos.pack()

# Cargar datos en el listado de diagnósticos al inicio
actualizar_listado_diagnosticos()

# Ejecutar la interfaz gráfica
root.mainloop()