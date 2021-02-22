import threading
import comms
from datetime import datetime
import time
import json


# Clase encargada de manejar la sesion de entrenamiento
class Session:
    def __init__(self, sessionid, sessionLength, reward, inputs):
        # - Variables -
        self.sessionid = sessionid  # Nombre de la session y del archivo resultante
        self.reward = reward  # Cantidad de comida a recompensar
        self.sessionLength = sessionLength  # Duracion total de la sesion
        self.sessionIsActive = False  # True significa que la sesion esta activa
        self.intervalIsActive = False  # True si estamos en un intervalo fijo en el momento
        self.intervalLength = None
        self.isListening = False
        # Inicializacion de clase de comunicacion por puerto serial
        self.comms = comms.Communication(inputs)
        # hilo que recibe los datos del arduino en segundo plano
        self.arduinoDataThread = threading.Thread(target=self.listenToArduino)
        self.initialTime = 0
        self.programInfo = None
        # Se configura logging para escribir en un archivo de texto con nombre igual a la variable sessionid
        with open('frames/'+sessionid +'.json', 'w') as fp:
            json.dump(self.programInfo,fp, indent=4)


    # Escucha los datos que recibe del arduino y los escribe en un archivo de texto
    def listenToArduino(self):
        self.isListening = True
        while self.isListening:
            msg = self.comms.readMessage()  # Mensaje recibido del arduino(Lista con inputs)
            if(self.intervalIsActive):
                self.programInfo["Lecturas"].append({
                    time.time()-self.initialTime:{
                    "Respuesta": msg[0],
                    "Intervalo Activo": True,
                    "Recompensa": 0,
                    "Duracion de intervalo": self.intervalLength
                }})
            else:
                if(msg[0] == 1):
                    self.programInfo["Lecturas"].append({
                        time.time()-self.initialTime: {
                        "Respuesta": 1,
                        "Intervalo Activo": False,
                        "Recompensa": self.reward,
                        "Duracion de intervalo": self.intervalLength
                    }})
                    # Se dispensa la cantidad de comida especificada
                    self.comms.doAction(self.reward)
                else:
                    self.programInfo["Lecturas"].append({
                        time.time()-self.initialTime:{
                        "Respuesta": 0,
                        "Intervalo Activo": False,
                        "Recompensa": 0,
                        "Duracion de intervalo": self.intervalLength
                    }})

    # Empieza a contar el tiempo de un intervalo fijo
    def startInterval(self, interval):
        self.intervalIsActive = True
        initialTime = time.time()
        while self.intervalIsActive:
            if (time.time() - initialTime) >= interval:
                self.intervalIsActive = False

    # Comienza un programa de intervalo fijo
    def startFIProgram(self, fi):
        self.intervalLength = fi
        self.programInfo = {
            "Frame": self.sessionid,
            "Duracion": self.sessionLength,
            "Programa": "Intervalo Fijo",
            "Hora de inicio de la sesion": self.initialTime,
            "Cantidad de recompensa": self.reward,
            "Lecturas": [

            ]
        }
        self.comms.setLedState(True)
        self.initialTime = time.time()
        self.arduinoDataThread.start()
        self.startInterval(self.intervalLength)
        while True:
            if((self.initialTime+self.sessionLength) < time.time()):
                self.intervalIsActive = False
                self.isListening = False
                self.comms.setLedState(False)
                # Se escriben los datos en un archivo json
                with open('frames/'+self.sessionid +'.json', 'w') as fp:
                    json.dump(self.programInfo,fp, indent=4)
                return
        



   # def startFVRandomProgram(self, n1, n2):
        

    #def startFVNormalDistProgram(self, media, desvEst):

    #def startFVPoisonDistProgram(self, media, desvEst):
