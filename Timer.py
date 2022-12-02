
import shutil
import time
from datetime import datetime

revision = None
last_revision = None

### Función para archivar log antiguo

def archiveLog():

    ## Contadores

    lineas_totales = 0
    correctos = 0

    ## Leemos el archivo para comprobar el porcentaje de fallos

    with open("./Logs/log.txt", 'r') as f:
        for linea in f:
            if('Transferencia' in linea):
                correctos = correctos +1
            lineas_totales = lineas_totales+1

    ## En caso de que el log no tenga ninguna entrada ponemos un uno por defecto para que no intente hacer una división entre 0

    if(lineas_totales==0):
        lineas_totales=1

    ## Creamos el nuevo log

    file = open('./Logs/log-'+str(datetime.now())[:10]+'.txt','w')
    file.write('##########################################################################\n\tEl porcentaje sin fallos de integridad es '+str(correctos*100/lineas_totales)[:5]+"%\n##########################################################################\n\n")
    file.close()

    ## Escribirmos el log antiguo en el nuevo para tener el registro
    file = open('./Logs/log-'+str(datetime.now())[:10]+'.txt','a')
    with open("./Logs/log.txt", 'r') as f:
        for linea in f:
            file.write(linea)
    file.close()

    ## Limpiamos el archivo log original para empezar a escribirlo de nuevo
    file = open('./Logs/log.txt','w')
    file.write('')
    file.close()

    return 0


### Función para la comprobación de si se ha modificado la configuración

def check_var():

    # Declaramos las variables globales para poder modificarlas

    global last_revision

    # Leemos el archivo de configuración y establecemos variables

    with open('./Data/dataTimer', "r") as conf_file:
            lines = conf_file.readlines()
            last_revision= lines[0][:-1]

    return 0

### Función para actualizar el archivo de configuración

def update_conf_file(last_chek):

    # Abrimos el fichero y escribimos la nueva configuración

    file = open('./Data/dataTimer','w')
    file.write(str(last_chek)+'\n')
    file.close()

    return 0

### Esta función se utiliza para comprobar si han pasado los días necesarios para la revisión

def check_revision():

    # Declaramos la variable global para poder modificarla

    global last_revision

    # Obtenemos el dia actual y comprobamos si han pasado los dias necesarios para una nueva revisión

    current_date = datetime.now()

    update_conf_file(str(current_date)[:10])

    # Miramos si ya ha pasado un mes y en ese caso enviamos un correo con el archivo correspondiente
    if(current_date.month!=datetime.strptime(last_revision, "%Y-%m-%d").month):

        archiveLog()

    return 0

### Función principal del timer

def main_method():

    while(True):
        # Comprobamos si se han modificado las variables globales
        check_var()
        # Hacemos la comprobación de si ha pasado el tiempo necesario
        check_revision()
        # Espera un minuto para la siguiente comprobación
        time.sleep(60*60*24) 


if __name__ == "__main__":
    main_method()