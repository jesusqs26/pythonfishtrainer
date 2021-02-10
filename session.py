import threading
import logging
import comms
from datetime import datetime
import time


# Clase encargada de manejar la sesion de entrenamiento
class Session:
    def __init__(self, sessionid, sessionLength, fixedInterval, reward):
        # - Variables -
        self.sessionid = sessionid # Nombre de la session y del archivo resultante
        self.reward = reward # Cantidad de comida a recompensar
        self.fixedInterval = fixedInterval # Intervalo fijo de espera antes de activar el sistema de recompensa
        self.sessionLength = sessionLength # Duracion total de la sesion
        self.sessionIsActive = False # True significa que la sesion esta activa
        self.fixedIntervalIsActive = False # True si estamos en un intervalo fijo en el momento
        self.comms = comms.Communication(1) # Inicializacion de clase de comunicacion por puerto serial
        self.arduinoDataThread = threading.Thread(target=self.listenToArduino) # hilo que recibe los datos del arduino en segundo plano
        self.actualTime
        self.initialTime
        
        # Se configura logging para escribir en un archivo de texto con nombre igual a la variable sessionid
        logging.basicConfig(filename=sessionid, level=logging.INFO)

    # Da comienzo a la sesion de entrenamiento    
    def startSession(self):
        self.sessionIsActive = True
        self.initialTime = time.time()
        self.comms.setLedState(True)

        logging.info(' --- Frame: '+self.sessionid+' --- ')
        logging.info('Duración: '+ self.sessionLength)
        logging.info('Intervalo Fijo: '+ self.fixedInterval)
        logging.info('Hora de inicio de sesión: '+ datetime.now())
        logging.info('Cantidad de recompensa: ' + self.reward)
        logging.info('-----------------------------------------')
        logging.info('Tiempo - Respuesta - IF - Recompensa')
        logging.info('-----------------------------------------')
        self.actualTime = time.time()
        while((self.initialTime+self.sessionLength) < time.time()):
            self.arduinoDataThread.start() # Se inicia el hilo que lee los datos que manda el arduino
            self.startFixedInterval()
            self.actualTime = time.time()



    # Escucha los datos que recibe del arduino y los escribe en un archivo de texto
    def listenToArduino(self):
        while True:
            if(self.sessionIsActive):
                msg = self.comms.readMessage() # Mensaje recibido del arduino(Lista con inputs)
                if(self.fixedIntervalIsActive):
                    logging.info((self.actualTime-self.initialTime)+' - '+', '.join(msg), ' - ', 'No')
                else:
                    self.comms.doAction(self.reward) # Se le manda una instruccion al arduino para que dispense el alimento especificado
                    logging.info((self.actualTime-self.initialTime)+' - '+', '.join(msg), ' - ', 'Si')
    
    # Empieza a contar el tiempo de un intervalo fijo
    def startFixedInterval(self):
        self.fixedIntervalIsActive = True
        initialTime = time.time()
        while self.fixedIntervalIsActive:
            if (time.time() - initialTime) >= self.fixedInterval:
                self.fixedIntervalIsActive = False




