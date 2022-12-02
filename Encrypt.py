import hmac
import secrets
import hashlib
import Diccionario
import datetime
import random

setNonces = set()


#### FUNCIONES CREACIÓN DE HASH ####

### Funcion para crear hash SHA1

def createHmacSHA1(message,key):

    # Creamos el hmac del menssage con la clave correspondiente, la parseamos y devolvemos

    hashed = hmac.new(key=key,msg=message.encode('utf-8'),digestmod=hashlib.sha1)
    hashed_hmac= hashed.hexdigest()

    return hashed_hmac

### Funcion para crear hash SHA256

def createHmacSHA256(message,key):
    
    # Creamos el hmac del menssage con la clave correspondiente, la parseamos y devolvemos

    hashed = hmac.new(key=key,msg=message.encode('utf-8'),digestmod=hashlib.sha256)
    hashed_hmac= hashed.hexdigest()
    return hashed_hmac 

### Función para la creacion aleatoria de un nonce
def generaNonce():

    # Declaramos el conjunto para poder modificarlo

    global setNonces

    # Generamos un nonce aleatorio

    nonce = str(secrets.token_bytes(16))[2:-1]
    nonce = nonce.replace(',','')

    return nonce

### Función para cargar en el conjunto los nonces ya utilizados

def loadSet():

    # Declaramos el conjunto para poder modificarlo

    global setNonces

    # Leemos el archivo de guardado y lo añadimos al conjunto

    with open("./Data/nonces",'r') as f:
        for line in f:
            setNonces.add(line[:-1])

    return 0

### Funcion comprobar el nonce dado

def checkSet(nonce):

    # Creamos variable para devolver

    res = False

    # Cargamos el conjunto

    loadSet()

    # Comprobamos si el nonce dado ya está en el conjunto

    if nonce in setNonces:
        res=True

    # En funcion del resultado lo añadimos al listado o devolvemos un error

    if not res:
        file = open("./Data/nonces",'a')
        file.write(nonce+"\n")
        file.close()

    return res

### Función para comprobar message

def checkMessage(message,cuentaOrigen,tipo,hmac,nonce):

    # Comprobar repetión nonce (REPPLY)

    if not checkSet(nonce):

        # Escogemos la clave del cliente

        clave = Diccionario.checkDict(cuentaOrigen)

        # Escogemos el tipo de encriptación

        if tipo =='0':
            hash = createHmacSHA1(message,clave)
        else:
            hash = createHmacSHA256(message,clave)
        
        ### Probabilidad de fallo MAN IN THE MIDDLE(20%)
        prob = random.random()
        
        if 0.2>prob:
            hash = 'HMAC MODIFICADO'

        # Comprobamos si el nuevo hmac creado coincide con el enviado
        # y guardamos en el archivo log

        if hash == hmac:
            file = open('./Logs/log.txt','a')
            file.write(str(datetime.datetime.now())+" -- Transferencia realizada desde la cuenta "+cuentaOrigen+"\n")
            file.close()
        else:
            file = open('./Logs/log.txt','a')
            file.write(str(datetime.datetime.now())+" -- Posible ataque MAN IN THE MIDDLE a cuenta "+cuentaOrigen+"\n")
            file.close()

    else:
        # Escribimos en el log el resultado de un posible ataque

        file = open('./Logs/log.txt','a')
        file.write(str(datetime.datetime.now())+" -- Posible ataque REPPLY a cuenta "+cuentaOrigen+"\n")
        file.close()
        print("Posible ataque REPPLY a cuenta "+cuentaOrigen)

    return 0


### Función para comprobar message

def checkMessageClient(message,cuentaOrigen,tipo,hmac,nonce):

    # Comprobar repetión nonce (REPPLY)

    if not checkSet(nonce):

        # Escogemos la clave del cliente

        clave = Diccionario.checkDict(cuentaOrigen)

        # Escogemos el tipo de encriptación

        if tipo =='0':
            hash = createHmacSHA1(message,clave)
        else:
            hash = createHmacSHA256(message,clave)

        if hash == hmac:
            print('CLIENTE: MENSAJE CORRECTO')
        else:
            print('CLIENTE: POSIBLE MENSAJE MODIFICADO')
    else:
        # Escribimos en el log el resultado de un posible ataque

        print("CLIENTE: Posible ataque REPPLY a cuenta "+cuentaOrigen)

    return 0



### Función para esoger un nonce ya utilizado para crear fallos simulados

def nonceError():

    # Cargamos el conjunto

    loadSet()

    # Seleccionamos el primer nonce ya registrado y lo guardamos

    for nonce in setNonces:
        return nonce
