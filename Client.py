import socket
import Encrypt
import Diccionario
# El cliente debe tener las mismas especificaciones del servidor
host = socket.gethostname()

# Especificamos que puerto vamos a utilizar 

port = 12345

# Especificamos tamaño del buffer

BUFFER_SIZE = 1024

# Iniciamos la prueba de conexión

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
    
    ### Declaramos todos los inputs que debe hacer el usuario que quiere enviar el mensaje

    print("Establecer número de cuenta origen:")
    nCuentaOrigen = input()
    print("Establecer número de cuenta destino:")
    nCuentaDest = input()
    print("Indicar cantidad:")
    value = input()
    print("Indicar tipo de encriptación:\n\tSHA1: 0\n\tSHA256:1")
    tipo = input()

    ### Comprobamos si los inputs enviados tienen el formato correcto, en este caso numérico y tipo de encriptación correcta

    if (type(int(nCuentaOrigen)) or type(int(nCuentaDest)) or type(int(value)))!=type(1):
        print("CUENTA DESTINO, CUENTA ORIGEN Y CANTIDAD DEBEN SER DATOS NUMÉRICOS")
        print("Pulsa cualquier botón para cerrar...")
        input()
        exit()

    if tipo!='0' and tipo!='1':
        print("TIPO NO VÁLIDO.")
        print("Pulsa cualquier botón para cerrar...")
        input()
        exit()

    ### Creamos un nonce aleatorio para nuestro mensaje a enviar

    nonce = Encrypt.generaNonce()

    ### Buscamos la clave del usuario si es que existe

    key = Diccionario.checkDict(nCuentaOrigen)

    if key == None:
        print('La cuenta no tiene una clave asociada. Dirigase a la sucursal más cercana.')
    
    else:

        ### Creamos el mensaje con el formato establecido

        message = "({nCuentaO},{nCuentaD},{valueI})\n{Nonce}".format(nCuentaO=nCuentaOrigen,nCuentaD=nCuentaDest,valueI=value,Nonce=nonce)

        ### Creamos el hmac correspondiente al tipo de encriptación

        if tipo =='0':
            hash = Encrypt.createHmacSHA1(message,key)
        else:
            hash = Encrypt.createHmacSHA256(message,key)

        ### Ordenamos todo el mensaje que se va a enviar y conectamos cn el host y puerto

        send = message+"\n"+hash+"\n"+tipo
        socket_tcp.connect((host, port))
        
        # Convertimos str a bytes y enviamos
        
        socket_tcp.send(send.encode('utf-8'))

        data = socket_tcp.recv(BUFFER_SIZE)
        input = data.decode('utf-8')
        message,nonce,hmac = input.split("\n")
        Encrypt.checkMessageClient(message+"\n"+nonce,nCuentaOrigen,tipo,hmac,nonce)
        print(message)

