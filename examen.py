# import os
# import re

# def tokenize(input_str):
#     tokens = []
#     pattern = r"([0-9]+\.[0-9]+|[0-9]+|\+|\-|\*|\/|\(|\))"
#     matches = re.finditer(pattern, input_str)

#     for match in matches:
#         token = match.group()
#         if re.match(r"[0-9]+\.[0-9]+", token):
#             tokens.append(("NUMERO_DECIMAL", token))
#         elif re.match(r"[0-9]+", token):
#             tokens.append(("NUMERO_ENTERO", token))
#         elif token in "+-*/":
#             tokens.append(("SIGNO_MAS" if token == "+" else "SIGO_MULTIPLICACION", token)) 
#         elif token == "(":
#             tokens.append(("PARENTESIS_IZQ", token))
#         elif token == ")":
#             tokens.append(("PARENTESIS_DER", token))
#         else:
#             tokens.append(("ERROR", token))
    
#     return tokens

# nombre_archivo = "numeros.txt"
# ruta_archivo = "C:/Users/Rafael/OneDrive/Escritorio/Compiladores"
# ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

# if os.path.exists(ruta_completa):
#     archivo = open(ruta_completa, "r", encoding="utf-8")
#     contenido = archivo.read()
#     archivo.close()

#     tokens = tokenize(contenido)
#     for token_type, token_value in tokens:
#         print(f"{token_type:20} {token_value:10}")

# else:
#     archivo = open(ruta_completa, "w")
#     archivo.write("Curso de compiladores.\n")
#     archivo.close()
import os
import re

def tokenize(input_str):
    tokens = []
    pattern = r"([0-9]+\.[0-9]+|[0-9]+|\+|\-|\*|\/|\(|\))"
    matches = re.finditer(pattern, input_str)

    for line_number, line in enumerate(input_str.split('\n'), start=1):
        for match in re.finditer(pattern, line):
            token = match.group()
            if re.match(r"[0-9]+\.[0-9]+", token):
                if token.count('.') > 1:
                    tokens.append(("ERROR_DECIMAL", token, line_number))
                else:
                    tokens.append(("NUMERO_DECIMAL", token, line_number))
            elif re.match(r"[0-9]+", token):
                tokens.append(("NUMERO_ENTERO", token, line_number))
            elif token in "+-*/":
                tokens.append(("SIGNO_MAS" if token == "+" else "SIGNO_MENOS" if token == "-" else "SIGNO_MULTIPLICACION" if token == "*" else "SIGNO_DIVISION", token, line_number))
            elif token == "(":
                tokens.append(("PARENTESIS_IZQ", token, line_number))
            elif token == ")":
                tokens.append(("PARENTESIS_DER", token, line_number))
            else:
                tokens.append(("ERROR", token, line_number))
    
    return tokens

nombre_archivo = "numeros.txt"
ruta_archivo = "C:/Users/Rafael/OneDrive/Escritorio/Compiladores"
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()

    tokens = tokenize(contenido)
    for token_type, token_value, line_number in tokens:
        print(f"{token_type:20} {token_value:10} Línea: {line_number}")

else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()
