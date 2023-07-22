import os

nombre_archivo = "archivo.txt"
ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"  # Opcional: especifica la ruta del archivo
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)



if os.path.exists(ruta_completa):
    # Leer el archivo para contar palabras y líneas
    archivo = open(ruta_completa, "r")
    contenido = archivo.read()
    archivo.close()

    # Contar cantidad de líneas
    num_lineas = len(contenido.split('\n'))

    # Contar cantidad de palabras
    num_palabras = len(contenido.split())

    print("Conteo de palabras:", num_palabras)
    print("Conteo de líneas:", num_lineas)

    print(contenido)
else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()



