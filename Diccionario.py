
import secrets

### Creamos una variable global dicionario de claves

diccionarioClaves = dict()

### Función para la creación de un diccionario con claves aleatorias

def crearDicc():

    # Declaramos la variable global para poder modificarla

    global diccionarioClaves

    # Creamos una lista de cuentas de clientes

    lista = [str(num) for num in range(10)]

    # Asociamos cada cuenta a una clave

    for cuenta in lista:
        diccionarioClaves[cuenta] = str(secrets.token_bytes(16)).replace(',','')[2:-1]

    # Escribimos el diccionario en un archivo externo para poder recuperarlo en caso de que nos haga falta

    file = open('./Data/Claves','w')
    for cuenta in diccionarioClaves:
        file.write(cuenta+','+diccionarioClaves[cuenta]+"\n")

    # Cerramos el archivo

    file.close()

    return 0

### Función para cargar el diccionario en la variable global

def loadDict():

    # Declaramos la variable global para poder modificarla

    global diccionarioClaves

    # Leemos el archivo de guardado y lo pasamos a la variable global diccionario

    with open('./Data/Claves','r') as f:
        for line in f:
            cuenta = line.split(',')[0]
            clave = line.split(',')[1]
            diccionarioClaves[cuenta] = clave
    
    return 0

### Función para la comprobación de si una cuenta existe en el diccionario

def checkDict(cuenta):

    # Declaramos la variable clave que se va a devolver por defecto con un valor nulo

    clave = None

    # Cargamos el diccionario

    loadDict()

    # Comprobamos si existe, y en ese caso devolvemos la clave

    if cuenta in diccionarioClaves:
        clave = diccionarioClaves[cuenta]
        return bytes(clave,'utf-8')
        
    return clave
