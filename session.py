import threading
import logging
import comms


# Clase encargada de manejar la sesion de entrenamiento
class Session:
    def __init__(self, sessionid, sessionLength, fixedInterval, reward):
        # - Variables -
        self.sessionid = sessionid # Nombre de la session y del archivo resultante
        self.reward = reward # Cantidad de comida a recompensar
        self.fixedInterval = fixedInterval # Intervalo fijo de espera antes de activar el sistema de recompensa
        self.sessionLength = sessionLength # Duracion total de la sesion
        self.sessionIsActive = False
        self.comms = comms.Communication(3)

        # Se configura logging para escribir en un archivo de texto con nombre igual a la variable sessionid
        logging.basicConfig(filename=sessionid,level=logging.INFO, format='%(asctime)s:%(message)s')

    # Da comienzo a la sesion de entrenamiento    
    def startSession(self):
        self.sessionIsActive = True
        


    # Escucha los datos que recibe del arduino y los escribe en un archivo de texto
    def listenToArduino(self):
        while True:
            if(self.sessionIsActive):
                logging.info(self.comms.readMessage())


    def 



