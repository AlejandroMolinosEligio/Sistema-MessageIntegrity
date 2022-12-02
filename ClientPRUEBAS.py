import random
import socket
import Encrypt
import Diccionario

# El cliente debe tener las mismas especificaciones del servidor
host = socket.gethostname()
port = 12345
BUFFER_SIZE = 1024

### Realizaremos el envio de 20 mensajes a modo de prueba para tener datos en el registro log

for _ in range(100):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:

        ### De forma aleatoria generamos 3 valores numéricos aleatorios y escogemos un tipo de encriptación

        nCuentaOrigen = str(random.randint(0,9))
        nCuentaDest = str(random.randint(0,9))
        value = str(random.randint(0,1000))
        tipo = str(random.randint(0,1))
        
        ### Generamos un nonce nuevo y comprobamos la clave del cliente

        nonce = Encrypt.generaNonce()
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

