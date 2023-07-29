import os
import re

nombre_archivo = "archivo.txt"
ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores" 
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()

    # Expresión regular para obtener palabras que contengan letras solamente
    palabras = re.findall(r'\b[a-zA-Z]+\b', contenido)

    # Expresión regular para obtener palabras que contengan letras y números, pero no enteros ni decimales
    palabras_con_numeros = re.findall(r'\b[a-zA-Z]*\d+[a-zA-Z]*\b', contenido)
    palabras_con_numeros = [palabra for palabra in palabras_con_numeros if not re.match(r'^[+-]?\d+(\.\d+)?$', palabra)]
    numeros_enteros = re.findall(r'\b[+-]?\d+\b', contenido)
    numeros_decimales = re.findall(r'\b[+-]?\d+\.\d+\b', contenido)
    signos_puntuacion_simbolos = re.findall(r'[^\w\s]', contenido)

    todas_las_palabras = palabras + palabras_con_numeros
    todosNumeros = numeros_enteros + numeros_decimales

    print("Palabras:", todas_las_palabras)
    print("Números:", todosNumeros)
    print("Signos de puntuación y símbolos:", signos_puntuacion_simbolos)

    def es_palabra(cadena):
        estado_actual = 0
        estados_aceptacion = {1}

        for caracter in cadena:
            if estado_actual == 0 and caracter.isalpha():
                estado_actual = 1
            elif estado_actual == 1 and caracter.isalnum():
                continue
            else:
                return False

        return estado_actual in estados_aceptacion

    def es_numero(cadena):
        estado_actual = 0
        estados_aceptacion = {1, 2, 3}

        for caracter in cadena:
            if estado_actual == 0 and caracter in ('-', '+'):
                estado_actual = 1
            elif estado_actual == 0 and caracter.isdigit():
                estado_actual = 2
            elif estado_actual == 1 and caracter.isdigit():
                estado_actual = 2
            elif estado_actual == 2 and caracter.isdigit():
                continue
            elif estado_actual == 2 and caracter == '.':
                estado_actual = 3
            elif estado_actual == 3 and caracter.isdigit():
                estado_actual = 3
            else:
                return False

        return estado_actual in estados_aceptacion



    def es_signo(cadena):
        return all(not caracter.isalnum() and not caracter.isspace() for caracter in cadena)

    # Obtener palabras, números y signos del contenido
    palabras = [palabra for palabra in contenido.split() if es_palabra(palabra)]
    numeros = [numero for numero in contenido.split() if es_numero(numero)]
    signos = [signo for signo in contenido.split() if es_signo(signo)]

    print("Palabras:", palabras)
    print("Números:", numeros)
    print("Signos de puntuación y símbolos:", signos)

else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()
