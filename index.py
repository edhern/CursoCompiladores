import os

nombre_archivo = "archivo.txt"
ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"  # Opcional: especifica la ruta del archivo
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

# Integrantes Wilson Peñate y Eddison Rafael

if os.path.exists(ruta_completa):
    # Ejercicio 1
    archivo = open(ruta_completa, "r")
    contenido = archivo.read()
    archivo.close()
    
    num_lineas = len(contenido.split('\n'))

    num_palabras = len(contenido.split())

    print("Conteo de palabras:", num_palabras)
    print("Conteo de líneas:", num_lineas)

    # Ejercicio 2
    numero_ingresado = input("Ingresa un número: ")

    try:
        numero = float(numero_ingresado)
        if numero.is_integer():
            print("entero")
        else:
            print("decimal")
    except ValueError:
        print("Error")
        
else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()



