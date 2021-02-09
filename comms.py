# Author: Jesús Ricardo Quintero Serrano
import serial
import msvcrt
import serial.tools.list_ports

# Clase encargada de recibir datos del arduino y mandarle instrucciones
class Communication:
    def __init__(self, numInputs):
        # - Variables -
        # Inputs recibidos del arduino
        self.numInputs = numInputs

        self.arduino = serial.Serial(self.findArduino(), 9600)
        

    # Detecta el puerto serial en el que se conecto el arduino //aun no valida que solo exista un arduino conectado
    def findArduino(self):
        ports = serial.tools.list_ports.comports()
        commPort = 'None'
        numConnection = len(ports)

        for i in range(0,numConnection):
            port = ports[i]
            strPort = str(port)

            # Se valida si la descripcion es de arduino original o clon
            if 'USB-SERIAL CH340' in strPort or 'Arduino' in strPort:
                splitPort = strPort.split(' ')
                commPort = splitPort[0]
        return commPort



    # Lee los datos del arduino del puerto serial y los regresa en una lista
    def escucharSerial(self):
        mensaje = self.arduino.readline()[:-2]
        datos = list()
        for i in range(0,self.numInputs):
            datos.append(mensaje[i])
        return datos


    # Escuchar teclado para prender y apagar el led de arduino 1 = Apagado, 2 = Prendido
    # Utiliza el modulo msvcrt put para escuchar cuando se presiona una tecla del teclado
    def escucharTeclado(self, tecla1, tecla2):
        tecla = msvcrt.getch()
        # Evalua si la tecla es q para mandar comando de apagar led
        if(tecla == bytes(tecla1)):
            self.arduino.write(b'1')
        # Evalua si la tecla es a para mandar comando de prender led
        elif(tecla == bytes(tecla2)):
            self.arduino.write(b'0')
    
    
