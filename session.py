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
        self.initialTime = 0
        # Se configura logging para escribir en un archivo de texto con nombre igual a la variable sessionid
        logging.basicConfig(filename='frames/'+sessionid+'.txt', level=logging.INFO, format='%(message)s')

    # Da comienzo a la sesion de entrenamiento    
    def startSession(self):
        self.sessionIsActive = True
        self.initialTime = time.time()
        self.comms.setLedState(True)
        
        print('Comenzando sesion')
        logging.info(' --- Frame: '+str(self.sessionid)+' --- ')
        logging.info('Duración: '+ str(self.sessionLength))
        logging.info('Intervalo Fijo: '+ str(self.fixedInterval))
        logging.info('Hora de inicio de sesión: '+ str(datetime.now()))
        logging.info('Cantidad de recompensa: ' + str(self.reward))
        logging.info('-----------------------------------------')
        logging.info('Tiempo - Respuesta - IF - Recompensa')
        logging.info('-----------------------------------------')

        self.arduinoDataThread.start() # Se inicia el hilo que lee los datos que manda el arduino
        self.startFixedInterval() # Puede necesitar cambios *****
        while True:
            if((self.initialTime+self.sessionLength) < time.time()):
                logging.info('-----------------------------------------')
                self.fixedIntervalIsActive = False
                return


    # Escucha los datos que recibe del arduino y los escribe en un archivo de texto
    def listenToArduino(self):
        print('Escuchando al arduino')
        while True:
            if(self.sessionIsActive):
                msg = self.comms.readMessage() # Mensaje recibido del arduino(Lista con inputs)
                if(self.fixedIntervalIsActive):
                    log = str(time.time()-self.initialTime)+' - '+msg[0]+ ' - '+ 'No'
                else:
                    if msg[0] == 1: # Checa si el input del arduino muestra que se activó el sensor
                        self.comms.doAction(self.reward) # Se le manda una instruccion al arduino para que dispense el alimento especificado
                        log = str(time.time()-self.initialTime)+' - '+msg[0]+ ' - '+'Si'
                        self.startFixedInterval() # Una vez entregada la recompenza se activa el intervalo fijo de nuevo
                    else:
                        log = str(time.time()-self.initialTime)+' - '+msg[0]+ ' - '+ 'No'
                logging.info(log)
    
    # Empieza a contar el tiempo de un intervalo fijo
    def startFixedInterval(self):
        print("Comenzando intervalo fijo")
        self.fixedIntervalIsActive = True
        initialTime = time.time()
        while self.fixedIntervalIsActive:
            if (time.time() - initialTime) >= self.fixedInterval:
                self.fixedIntervalIsActive = False




