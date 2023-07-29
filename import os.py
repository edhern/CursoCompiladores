import os
import re

nombre_archivo = "archivo.txt"
ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores" 
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

# Integrantes Wilson Peñate y Eddison Rafael

if os.path.exists(ruta_completa):
    # Ejercicio 1
    archivo = open(ruta_completa, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()
    
    num_lineas = len(contenido.split('\n'))

    num_palabras = len(contenido.split())

    print("Conteo de palabras:", num_palabras)
    print("Conteo de líneas:", num_lineas)

    # Ejercicio 2
    # numero_ingresado = input("Ingresa un número: ")

    # try:
    #     numero = float(numero_ingresado)
    #     if numero.is_integer():
    #         print("entero")
    #     else:
    #         print("decimal")
    # except ValueError:
    #     print("Error")

    # Ejercicio 3
    palabras = re.findall(r'\b[a-zA-Z]+\b', contenido)
    forNums = re.findall(r'\b\w+\b', contenido)
    numeros = []
    for palabra in forNums:
        try:
            numero = int(forNums)
            numeros.append(numero)
        except ValueError:
            pass

    signos = re.findall(r'[^\w\s]', contenido)

    # def es_palabra(cadena):
    #     estado_actual = 0
    #     estados_aceptacion = {1}

    #     for caracter in cadena:
    #         if estado_actual == 0 and caracter.isalpha():
    #             estado_actual = 1
    #         elif estado_actual == 1 and caracter.isalnum():
    #             continue
    #         else:
    #             return False

    #     return estado_actual in estados_aceptacion

    # def es_numero(cadena):
    #     estado_actual = 0
    #     estados_aceptacion = {1}

    #     for caracter in cadena:
    #         if estado_actual == 0 and caracter in ('-', '+'):
    #             estado_actual = 2
    #         elif estado_actual in (0, 2) and caracter.isdigit():
    #             estado_actual = 1
    #         elif estado_actual == 1 and caracter.isdigit():
    #             continue
    #         elif estado_actual == 2 and caracter.isdigit():
    #             estado_actual = 1
    #         else:
    #             return False

    #     return estado_actual in estados_aceptacion

    # def es_signo(cadena):
    #     return all(not caracter.isalnum() and not caracter.isspace() for caracter in cadena)

    # # Obtener palabras, números y signos del contenido
    # palabras = [palabra for palabra in contenido.split() if es_palabra(palabra)]
    # numeros = [numero for numero in contenido.split() if es_numero(numero)]
    # signos = [signo for signo in contenido.split() if es_signo(signo)]


    print("Palabras:", palabras)
    print("Números:", numeros)
    print("Signos:", signos)    
else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()



