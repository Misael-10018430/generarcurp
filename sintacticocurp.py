import ply.lex as lex
import ply.yacc as yacc

ESTADOS_VALIDOS = {
    'AS': 'AGUASCALIENTES','BC': 'BAJA CALIFORNIA','BS': 'BAJA CALIFORNIA SUR','CC': 'CAMPECHE',
    'CL': 'COAHUILA DE ZARAGOZA','CM': 'COLIMA','CS': 'CHIAPAS','CH': 'CHIHUAHUA','DF': 'CIUDAD DE MÉXICO',
    'DG': 'DURANGO','GT': 'GUANAJUATO','GR': 'GUERRERO','HG': 'HIDALGO','JC': 'JALISCO','MC': 'MÉXICO',
    'MN': 'MICHOACÁN DE OCAMPO','MS': 'MORELOS','NT': 'NAYARIT','NL': 'NUEVO LEÓN','OC': 'OAXACA','PL': 'PUEBLA',
    'QT': 'QUERÉTARO','QR': 'QUINTANA ROO','SP': 'SAN LUIS POTOSÍ','SL': 'SINALOA','SR': 'SONORA','TC': 'TABASCO',
    'TS': 'TAMAULIPAS','TL': 'TLAXCALA','VZ': 'VERACRUZ DE IGNACIO DE LA LLAVE','YN': 'YUCATÁN','ZS': 'ZACATECAS',
    'NE': 'NO ESPECIFICADO','NA': 'NO APLICA','SI': 'SE IGNORA'
}

def obtener_vocal(texto):
    vocales = 'AEIOUÁÉÍÓÚ'
    texto = texto.upper()
    for i in range(1, len(texto)):
        if texto[i] in vocales:
            return texto[i].replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    return 'X'

def obtener_consonante(texto):
    consonantes = 'BCDFGHJKLMNÑPQRSTVWXYZ'
    texto = texto.upper()
    for i in range(1, len(texto)):
        if texto[i] in consonantes:
            return texto[i]
    return 'X'

def calcular_homoclave(curp_16, anio):
    valores = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
        'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'Ñ': 24, 'O': 25, 'P': 26, 'Q': 27,
        'R': 28, 'S': 29, 'T': 30, 'U': 31, 'V': 32, 'W': 33, 'X': 34, 'Y': 35, 'Z': 36
    }
    
    suma = 0
    for i, caracter in enumerate(curp_16):
        valor = valores.get(caracter, 0)
        suma += valor * (18 - i)
    
    residuo = suma % 10
    resultado = 10 - residuo
    
    if anio < 2000:
        return str(resultado % 10)
    else:
        indice = resultado % 26
        return chr(65 + indice)

def calcular_digito_verificador(curp):
    valores = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
        'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'Ñ': 24, 'O': 25, 'P': 26, 'Q': 27,
        'R': 28, 'S': 29, 'T': 30, 'U': 31, 'V': 32, 'W': 33, 'X': 34, 'Y': 35, 'Z': 36
    }
    suma = 0
    for i, caracter in enumerate(curp[:17]):
        valor = valores.get(caracter, 0)
        suma += valor * (18 - i)
    
    modulo = suma % 10
    if modulo == 0:
        return '0'
    else:
        return str(10 - modulo)

def validar_datos(nombre, apellido, segundo_apellido, dia, mes, anio, sexo, estado):
    errores = []
    if not nombre:
        errores.append("ERROR: El campo NOMBRE es obligatorio")
    elif not nombre.replace(' ', '').isalpha():
        errores.append("ERROR LÉXICO: NOMBRE solo debe contener letras")
    if not apellido:
        errores.append("ERROR: El campo PRIMER APELLIDO es obligatorio")
    elif not apellido.replace(' ', '').isalpha():
        errores.append("ERROR LÉXICO: PRIMER APELLIDO solo debe contener letras")
    if not segundo_apellido:
        errores.append("ERROR: El campo SEGUNDO APELLIDO es obligatorio")
    elif not segundo_apellido.replace(' ', '').isalpha():
        errores.append("ERROR LÉXICO: SEGUNDO APELLIDO solo debe contener letras")
    if not dia:
        errores.append("ERROR: El campo DÍA DE NACIMIENTO es obligatorio")
    else:
        try:
            dia_int = int(dia)
            if dia_int < 1 or dia_int > 31:
                errores.append(f"ERROR SINTÁCTICO: DÍA inválido '{dia}'. Debe estar entre 01 y 31")
        except ValueError:
            errores.append(f"ERROR LÉXICO: DÍA '{dia}' debe ser un número")
    if not mes:
        errores.append("ERROR: El campo MES DE NACIMIENTO es obligatorio")
    else:
        try:
            mes_int = int(mes)
            if mes_int < 1 or mes_int > 12:
                errores.append(f"ERROR SINTÁCTICO: MES inválido '{mes}'. Debe estar entre 01 y 12")
        except ValueError:
            errores.append(f"ERROR LÉXICO: MES '{mes}' debe ser un número")
    if not anio:
        errores.append("ERROR: El campo AÑO DE NACIMIENTO es obligatorio")
    else:
        try:
            anio_int = int(anio)
            if anio_int < 1900 or anio_int > 2025:
                errores.append(f"ERROR SINTÁCTICO: AÑO inválido '{anio}'. Debe estar entre 1900 y 2025")
        except ValueError:
            errores.append(f"ERROR LÉXICO: AÑO '{anio}' debe ser un número")
    if not sexo:
        errores.append("ERROR: El campo SEXO es obligatorio")
    elif sexo not in ['H', 'M']:
        errores.append(f"ERROR SINTÁCTICO: SEXO inválido '{sexo}'. Solo se permite 'H' (Hombre) o 'M' (Mujer)")
    if not estado:
        errores.append("ERROR: El campo ESTADO es obligatorio")
    elif estado not in ESTADOS_VALIDOS:
        errores.append(f"ERROR SINTÁCTICO: ESTADO inválido '{estado}'. Debe seleccionar un estado válido del catálogo")
    return errores

def generar_curp_desde_formulario(nombre, apellido, segundo_apellido, dia, mes, anio, sexo, estado):
    errores = validar_datos(nombre, apellido, segundo_apellido, dia, mes, anio, sexo, estado)
    if errores:
        return {
            'tipo': 'error',
            'mensaje': '\n'.join(errores)
        }
    dia_int = int(dia)
    mes_int = int(mes)
    anio_int = int(anio)
    curp = ""
    curp += apellido[0]
    curp += obtener_vocal(apellido)
    curp += segundo_apellido[0]
    curp += nombre[0]
    curp += str(anio_int)[-2:]
    curp += f"{mes_int:02d}"
    curp += f"{dia_int:02d}"
    curp += sexo
    curp += estado
    curp += obtener_consonante(apellido)
    curp += obtener_consonante(segundo_apellido)
    curp += obtener_consonante(nombre)
    
    homoclave = calcular_homoclave(curp, anio_int)
    curp += homoclave
    
    digito_verificador = calcular_digito_verificador(curp)
    curp += digito_verificador
    
    return {
        'tipo': 'exito',
        'curp': curp,
        'mensaje': 'CURP GENERADA',
        'nota': 'NOTA: Los dos caracteres en rojo (posiciones 17 y 18) son la HOMOCLAVE y el DÍGITO VERIFICADOR. El dígito verificador depende de la homoclave, así que si la homoclave está mal, el verificador también estará mal. Estos se calculan mediante algoritmo aproximado basado en documentación oficial. El gobierno mexicano puede asignar valores diferentes si detecta duplicados en su base de datos nacional. Para verificar tu CURP oficial, consulta: www.gob.mx/curp'
    }

reserved = {
    'nombre': 'NOMBRE','apellido': 'APELLIDO','segundoapellido': 'SEGUNDOAPELLIDO',
    'sexo': 'SEXO','dia': 'DIA','mes': 'MES','anio': 'ANIO','estado': 'ESTADO',
    'generar': 'GENERAR'
}
tokens = [
    'ID','NUMERO','OPERADOR','DELIMITADOR'
] + list(reserved.values())
t_OPERADOR = r'='
t_DELIMITADOR = r';'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_ID(t):
    r'[a-zA-ZÑñáéíóúÁÉÍÓÚ]+'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore = ' \t'
def t_error(t):
    print(f"ERROR LÉXICO: Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)
lexer = lex.lex()
error_sintactico = None
datos_curp_parser = {}

def p_programa(p):
    '''
    programa : asignaciones GENERAR
    '''
    p[0] = "Programa válido"
def p_asignaciones(p):
    '''
    asignaciones : asignacion asignaciones
                 | asignacion
    '''
    pass
def p_asignacion(p):
    '''
    asignacion : NOMBRE OPERADOR ID
               | APELLIDO OPERADOR ID
               | SEGUNDOAPELLIDO OPERADOR ID
               | SEXO OPERADOR ID
               | DIA OPERADOR NUMERO
               | MES OPERADOR NUMERO
               | ANIO OPERADOR NUMERO
               | ESTADO OPERADOR ID
    '''
    campo = p[1].lower()
    valor = p[3]
    datos_curp_parser[campo] = valor
def p_error(p):
    global error_sintactico
    if p:
        error_sintactico = f"ERROR SINTÁCTICO - Token inesperado: '{p.value}' en línea {p.lineno}"
    else:
        error_sintactico = "ERROR SINTÁCTICO - Fin de entrada inesperado"
parser = yacc.yacc()
def analizar_lexico(texto):
    lexer.input(texto)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append(tok)
    return tokens_encontrados
def analizar_sintactico(texto):
    global error_sintactico, datos_curp_parser
    error_sintactico = None
    datos_curp_parser = {}
    lexer.lineno = 1
    try:
        resultado = parser.parse(texto, lexer=lexer)
        if error_sintactico:
            return error_sintactico
        return "Análisis sintáctico completado correctamente"
    except Exception as e:
        return f"ERROR SINTÁCTICO: {str(e)}"