import socket
import Encrypt
import Diccionario
import datetime
import random

# Esta función nos da el nombre de la máquina

host = socket.gethostname() 

# Especificamos el puerto a utilizar

port = 12345

# Usamos un número pequeño para tener una respuesta rápida 

BUFFER_SIZE = 1024 
'''Los objetos socket soportan el context manager type
así que podemos usarlo con una sentencia with, no hay necesidad
de llamar a socket_close()
'''
### Creamos el diccinario de claves

Diccionario.crearDicc()

# Creamos un objeto socket tipo TCP y dejamos abierto el servidor

while True:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
        socket_tcp.bind((host, port)) 
        socket_tcp.listen(5) # Esperamos la conexión del cliente 
        conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente 
        with conn:

            # Mensaje de comprobación del servidor

            print('SERVIDOR: [*] Conexión establecida') 
            while True:
                # Recibimos bytes, convertimos en str
                data = conn.recv(BUFFER_SIZE)
                # Verificamos que hemos recibido datos
                if not data:
                    break
                else:
                    print('SERVIDOR: [*] Datos recibidos')

                    # Parseamos los datos recibidos en sus variables correspondientes

                    input = data.decode('utf-8')
                    message,nonce,hash,tipo = input.split('\n')
                    nCuentaO,nCuentaD,value = message[1:-1].split(',')

                    ### Message a comprobar con probabilidad de fallos REPLAY(20%)

                    messageEntero = message+"\n"+nonce


                    if 0.2>random.random():
                        nonce = Encrypt.nonceError()
                        messageEntero = message+"\n"+nonce

                    # Comprobar integridad mensaje

                    Encrypt.checkMessage(messageEntero,nCuentaO,tipo,hash,nonce)

                response_message = 'SERVIDOR: TRANSFERENCIA RECIBIDA\n'+Encrypt.generaNonce()
                
                key = Diccionario.checkDict(nCuentaO)

                if tipo =='0':
                    hash = Encrypt.createHmacSHA1(response_message,key)
                else:
                    hash = Encrypt.createHmacSHA256(response_message,key)

                response_message = response_message + "\n" + hash

                conn.send(bytes(response_message,'utf-8'))
