# Rene Gerardo Kipper Peña - A01283516
# reflexion al final
import sys
import os

palabras_reservadas = [
    "False",
    "await",
    "else",
    "import",
    "pass",
    "None",
    "break",
    "except",
    "in",
    "raise",
    "True",
    "class",
    "finally",
    "is",
    "return",
    "and",
    "continue",
    "for",
    "lambda",
    "try",
    "as",
    "def",
    "from",
    "nonlocal",
    "while",
    "assert",
    "del",
    "global",
    "not",
    "with",
    "async",
    "elif",
    "if",
    "or",
    "yield",
    # tipos de datos
    "int",
    "float",
    "string",
    "char",
    "long",
    "list", 
    "tuple" 
]
# Tokens
ASIG = 100   # Asignación (=)
SUM = 101    # Suma (+)
MULT = 102   # Multiplicación (*)
POW = 103    # Potencia (^)
LRP = 104    # Abre Paréntesis (
RRP = 105    # Cierra Paréntesis )
VAR = 106    # Nombre de Variable Ej. atributo_1
INT = 107    # Número Entero
FLT = 108    # Número Flotante
DIV = 109    # División
RES = 110    # Resta
COM = 111    # Comentario
PER = 112    # Coma
FUNC = 113   # Funcion
DOU = 114    # Dos Puntos
STR = 115    # String
OBR = 116    # [
CBR = 117    # ] 
PUN = 118    # .
ESP = 119    # " "
ERR = 200    # Error, token inválido

# Matriz de transiciones DFA
#       Letra     _    Entero   .    E,e     =      +        *      /      ^       (        )    esp     -     ,     :    "   [     ]      #
MT = [[   1   ,  ERR  ,   2  ,  3  ,  1  ,  ASIG,  SUM  ,  MULT  ,  6  ,  POW  ,  LRP  ,   RRP,   ESP   ,  8 ,  PER,  DOU, 9  , OBR, CBR,  7 ], # State 0 - Initial
      [   1   ,   1   ,   1  , VAR ,  1  ,  VAR ,  VAR  ,  VAR   ,  VAR,  VAR  ,  FUNC ,   VAR,  VAR  , VAR,  VAR,  VAR, VAR, VAR, VAR, VAR], # State 1 - Variable
      [  ERR  ,  ERR  ,   2  ,  3  , ERR ,  INT ,  INT  ,  INT   ,  INT,  INT  ,  INT  ,   INT,  INT  , INT,  INT,  INT, INT, INT, INT, INT], # State 2 - Entero
      [  ERR  ,  ERR  ,   3  , ERR ,  4  ,  FLT ,  FLT  ,  FLT   ,  FLT,  FLT  ,  FLT  ,   FLT,  FLT  , FLT,  FLT,  FLT, FLT, FLT, FLT, FLT], # State 3 - Float Antes del Exponencial E
      [  ERR  ,  ERR  ,   4  , ERR , ERR ,  FLT ,  FLT  ,  FLT   ,  FLT,  FLT  ,  FLT  ,   FLT,  FLT  ,  5 ,  FLT,  FLT, FLT, FLT, FLT, FLT], # State 4 - Float Después del Exponencial E
      [  ERR  ,  ERR  ,   5  , ERR , ERR ,  FLT ,  FLT  ,  FLT   ,  FLT,  FLT  ,  FLT  ,   FLT,  FLT  , FLT,  FLT,  FLT, FLT, FLT, FLT, FLT], # State 5 - Float Negativo
      [  DIV  ,  ERR  ,  DIV , DIV , DIV ,  DIV ,  DIV  ,  DIV   ,  DIV  ,  DIV  ,  DIV  ,   DIV,  DIV  , DIV,  DIV,  DIV, DIV, DIV,DIV,DIV], # State 6 - Comentario/División
      [   7   ,   7   ,   7  ,  7  ,  7  ,   7  ,   7   ,   7    ,  7  ,   7   ,   7   ,    7 ,   7   ,  7 ,   7,    7,   7 ,   7,  7,   7], # State 7 - Comentario
      [   8   ,  RES  ,  2 ,  2  ,  3  ,  RES ,  RES  ,  RES   , RES ,  RES  ,  RES  ,   RES,  RES  , RES,    RES,  RES, RES, RES, RES, RES], # State 8 - Resta o Real
      [   9   ,   9   ,  9   ,  9  ,  9  ,   9  ,   9   ,   9    ,  9  ,   9   ,   9   ,    9,    9   ,  9 ,   9,    9,  STR,  9 ,  9,   9]] # State 9 - String 



# O(n)
def filter(c):
        if c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c== '9':
            return 2
        elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13:
            return 12
        elif c == 'e' or c == 'E':
            return 4
        elif c == '-':
            return 13
        elif c.isalpha():
            return 0
        elif c == '_':
            return 1
        elif c == '.':
            return 3
        elif c == '=' or c == '<' or c == '>' or c == "!":
            return 5
        elif c == '+':
            return 6
        elif c == '*':
            return 7
        elif c == '/':
            return 8
        elif c == '^':
            return 9
        elif c == '(':
            return 10
        elif c == ')':
            return 11
        elif c == ',':
            return 14
        elif c == ':':
            return 15
        elif c == '"' or c == "\'":
            return 16
        elif c == '[' or c == '{':
            return 17
        elif c == ']' or c == '}':
            return 18
        elif c == '#':
            return 19
        else :
            return 12


# Cataloga char por char asignando el color de la palabra completa
# INPUT: linea por colorear y nombre del archivo de salida
# OUTPUT: nada 

# O(n^2 )
def scanner(linea, output):
    state = 0
    lexeme = ""
    tokens = []
    read = True
    charNum = 0
    linea = linea + "\n"
    contador = len(linea)
    f = open(output, "a", encoding="utf-8") 
    while (contador > 0):                                  # Mientras todavía queden caracteres por leer
        while state < 100:                               # Sólo se detiene si llega a un estado de aceptación o a un error
            if read:
                if charNum < len(linea):                 # Si no es el último caracter
                    c = linea[charNum]
                    charNum = charNum + 1
                    if(c == "\t"):
                        f.write('''&emsp;''')
            else: read = True

            state = MT[state][filter(c)]
            if state < 100 and state != 0: lexeme += c
            contador = contador - 1
            if charNum == len(linea) and state == 7:     # Si es el último carácter y es un comentario
                lexeme = lexeme.rstrip()
                state = COM

            if(contador == 0): break
        if state == INT :
            read = False
            f.write('''<span style="color:#E74C3C">''')
            f.write(lexeme)
            f.write('''</span>''')
            contador = contador + 1
        elif state == FLT:
            read = False
            f.write('''<span style="color:#E74C3C">''')
            f.write(lexeme)
            f.write('''</span>''')
            contador = contador + 1
        elif state == ASIG:
            lexeme += c
            f.write('''<span  style="color:#8E44AD ">''')
            f.write(lexeme)
            f.write('''</span>\n''')   
        elif state == SUM:
            lexeme += c
            f.write('''<span style="color:#48C9B0">''')
            f.write(lexeme)
            f.write('''</span>\n''')  
        elif state == MULT:
            lexeme += c
            f.write('''<span style="color:#48C9B0">''')
            f.write(lexeme)
            f.write('''</span>''')  
        elif state == POW:
            lexeme += c
            f.write('''<span style="color:#FF4949">''')
            f.write(lexeme)
            f.write('''</span>\n''')  
        elif state == LRP:
            lexeme += c
            f.write('''<span style="color:#B7950B">''')
            f.write(lexeme)
            f.write('''</span>''')  
        elif state == RRP:
            lexeme += c
            f.write('''<span style="color:#B7950B">''')
            f.write(lexeme)
            f.write('''</span>\n''') 
        elif state == VAR:
            read = False
            if(lexeme in palabras_reservadas): f.write('''<span style="color:#3498DB">''')
            else: f.write('''<span style="color:#922B21">''')
            f.write(lexeme)
            f.write('''</span>\n''')
            contador = contador + 1
        elif state == DIV:
            lexeme += c
            lexeme = lexeme[0]
            f.write('''<span style="color:#48C9B0">''')
            f.write(lexeme)
            f.write('''</span>\n''') 
        elif state == RES:
            lexeme += c
            lexeme = lexeme[0]
            f.write('''<span style="color:red">''')
            f.write(lexeme)
            f.write('''</span>\n''') 
        elif state == COM:
            read = False
            f.write('''<span style="color:#00FF44">''')
            f.write(lexeme)
            f.write('''</span>\n''')
            contador = contador + 1
        elif state == PER:
            lexeme += c
            f.write('''<span style="color:black">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == FUNC:
            read = False
            f.write('''<span style="color:#A9CCE3">''')
            f.write(lexeme)
            f.write('''</span>\n''')
            contador = contador + 1
        elif state == DOU:
            lexeme += c
            f.write('''<span style="color:black">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == STR:
            lexeme += c
            f.write('''<span style="color:orange">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == OBR:
            lexeme += c
            f.write('''<span style="color:#D2B4DE">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == CBR:
            lexeme += c
            f.write('''<span style="color:#D2B4DE">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == PUN:
            lexeme += c
            f.write('''<span style="color:black">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        elif state == ESP:
            f.write('''<span style="color:#1E8449">''')
            f.write("&nbsp;")
            f.write('''<span>\n''')
        elif state ==  ERR:
            read = False
            f.write('''<span style="color:black">''')
            f.write(lexeme)
            f.write('''</span>\n''')
        tokens.append(state)
        #if state == END: return tokens
        lexeme = ""
        state= 0
    f.close()


# (O(n^2))
def file_reading(file):
    try:
        output=sys.argv[2]#Tomamos el segundo argumento del comando para determinar la ruta del archivo de salida
    except:
        print("No se introdujo path de salida")

    # Iniciamos el archivo de salida , lo preparamos
    outputFile=open(output,'w',encoding='utf-8')
    outputFile.write("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lexer</title>
</head>
<body >
    <h3>
    <div align = "right">

    """)
    outputFile.close()
    with open(file ,'r',encoding='utf-8') as f:#leeremos el archivo , donde cada linea sera f
        #O(n) , esta funcion  ejecuta todas las lineas del archivo
        for linea in f:
            scanner(linea,output)
            outputFile = open(output, 'a', encoding="utf-8")
            # Genera un brinco de linea
            outputFile.write('''<br>''')
            outputFile.close()
    outputFile = open(output, 'a', encoding="utf-8")
    outputFile.write('''</div></h3></body></html>''')
    outputFile.close()
    # os.startfile(output)


if __name__ == "__main__":
    try:
        files = sys.argv[1]
        # le pasamos los argumentos del input a la funcion
        file_reading(files)
    except:
        print("Error: archivo de entrada no detectado")

# Complejidad del codigo: O(n^2), apreciable en sus iteraciones. En ciertos casos puede iterarse una sola vez;
# sin embargo, en el peor de los casos se requerirían múltiples iteraciones para poder completar el ciclo. 
# debido a esto, su complejidad en notación Big O sería de O(n^2)
# /* Reflexion */
# El codigo que compone a este dfa funciona mediante iteraciones; 
# por cada documento => por cada linea => por cada caracter se debe correr el ciclo para poder determinar el token 
# que este generará. En cuanto a los estados del autómata en sí, estos se manejan mediante una matriz de transiciones 
# con la que podemos determinar dado el estado actual y la siguiente lectura, los pasos a seguir del autómata.