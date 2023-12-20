import os
import telebot
import Adafruit_DHT
import Adafruit_IO
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

#Definicion de los sensores y de puertos que utilizan.
sensorDHT22 = Adafruit_DHT.DHT22
factory = PiGPIOFactory()
servoMotorHumedad = AngularServo(12, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)

#Pines que se vana utilizar para los sensores, y relevador
pinRelevador = 20
pinSensorMQ135 = 8
pinSensorDHT22 = 16
pinSensorHumedad = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pinRelevador, GPIO.OUT)
GPIO.setup(pinSensorMQ135, GPIO.IN)
GPIO.setup(pinSensorHumedad, GPIO.IN)

#Configuraciond e la conexión con Telegram
API_TOKEN= '5987306630:AAEIzI69r1QRQQNPc9Py3XHIhi6To9DV_hw'
bot=telebot.TeleBot(API_TOKEN)

#Variables globales para el control de los eventos
estado=False
instruccion=0
mensaje=""
estadoServoHumedadEstatico=False
estadoRelayEstatico=False

estadoServoHumedadDinamico=False
estadoRelayDinamico=False
modo=False

#Funcionalidades individuales de la bomba y del servomotor
#Se verifica el estado del dispositivo que se activa y se marca con una bandera
#Se debe de verificar cuando se hace en estado dinamico o en estatico
def compuertaAbre(opcion):
    servoMotorHumedad.angle = -90
    if opcion==1:
        estadoServoHumedadEstatico=True
    elif opcion==2:
        estadoServoHumedadDinamico=True

def compuertaCierra(opcion):
    servoMotorHumedad.angle = 0
    if opcion==1:
        estadoServoHumedadEstatico=False
    elif opcion==2:
        estadoServoHumedadDinamico=False
    
def riegoEmpieza(opcion):
    GPIO.output(pinRelevador, GPIO.HIGH)
    if opcion==1:
        estadoRelayEstatico=True
    elif opcion==2:
        estadoRelayDinamico=True

def riegoTermina(opcion):
    GPIO.output(pinRelevador, GPIO.LOW)
    if opcion==1:
        estadoRelayEstatico=False
    elif opcion==2:
        estadoRelayDinamico=False
    

#Definicion del comportamiento del sensor de temperatura y humedad del aire.
def DHT22():
    global mensaje
    bot.reply_to(mensaje,"\U0001F331 ESTATUS DEL INVERNADERO \U0001F331")
    humedad,temperatura = Adafruit_DHT.read(sensorDHT22,pinSensorDHT22)
    if humedad is not None and temperatura is not None:
        bot.reply_to(mensaje,"\U0001F321 Temperatura={0:0.1f}C Humedad={1:0.1f}%".format(temperatura,humedad))
        if temperatura < 28:
            bot.reply_to(mensaje,"\U00002600 Temperatura baja, abrire el techo.")
            compuertaAbre(2)
        else:
            bot.reply_to(mensaje,"\U00002705 Temperatura correcta.")
            compuertaCierra(2)
    sleep(1)

#Definicion del comportamiento del sensor de humedad, para activar la bomba
def humedad():
    global mensaje
    humedadTierra = GPIO.input(pinSensorHumedad)
    if humedadTierra==0:
        bot.reply_to(mensaje,"\U00002705 Tierra humeda.")
        riegoTermina(2)
    else:
        bot.reply_to(mensaje,"\U0001F4A7 Tierra seca, no te preocupes yo la riego.")
        riegoEmpieza(2)
        sleep(2)
        riegoTermina(2)
    sleep(1)

#Definicion del sensor de aire, para idenficar gases.
def MQ135():
    global mensaje
    gas = GPIO.input(pinSensorMQ135)
    if not gas:
        bot.reply_to(mensaje,"\U0001F343 Detecto gases, abrire las ventanas.")
        compuertaAbre(2)
    else:
        bot.reply_to(mensaje,"\U00002705 No se detectan gases.")
        compuertaCierra(2)
    sleep(1)

#Funcion principal que ejecuta en paralelo para verificar el estado de los sensores.
#En la primer condicional se verifica que se haga de forma automatica y la otra de forma
#manual o solo por comando
#Se deben de comprobar el hardware que quedo activado en el otro modo de ejecución y se
#debe de terminar la ejecución antes de realizar modificaciones en el estado actual.
def sensores():
    try:
        while True:
            global estado
            global instruccion
            global estadoServoHumedadEstatico
            global estadoRelayEstatico
            global estadoServoHumedadDinamico
            global estadoRelayDinamico
            #Modo dinamico
            if estado==True:
                if estadoServoHumedadEstatico:
                    compuertaCierra(1)
                if estadoRelayEstatico:
                    riegoTermina(1)
                DHT22()
                humedad()
                MQ135()
                sleep(3) #Cambiar a 10 minutos
            #Modo estático
            else:
                if estadoRelayDinamico:
                    riegoTermina(2)
                if estadoServoHumedadDinamico:
                    compuertaCierra(2)
                #Ejecución de los comandos individuales
                if instruccion==1:
                    riegoEmpieza(1)
                elif instruccion==2:
                    riegoTermina(1)
                elif instruccion==3:
                    compuertaAbre(1)
                elif instruccion==4:
                    compuertaCierra(1)
            
    except KeyboardInterrupt:
        GPIO.output(pin_rele, GPIO.LOW)
        print("Programa detenido. Pines limpiados y GPIO liberado.")

    finally:
        GPIO.cleanup()
        print("Programa detenido. Pines limpiados y GPIO liberado.")
    
#Inicialización del hilo que ejecuta a los sensores.
sensoresThread = Thread(target=sensores)
sensoresThread.setDaemon(True)
sensoresThread.start()

#Hilo que va a mantener el chatbot y recibir los comandos desde telegram.
@bot.message_handler(commands=['help'])
def turn_on(message):
    bot.reply_to(message,"""\U0001F331 Bienvenid@ a FloraFlow \U0001F331
Envia /enciende para prender el modo automatico o /apaga para apagarlo además, puedes mandar los siguientes comandos:
- /comienzaRiego para encender la bomba
- /terminaRiego para apagar la bomba
- /abreTecho para abrir el techo del invernadero
- /cierraTecho para cerrar el techo del invernadero
    """)
    
@bot.message_handler(commands=['enciende'])
def turn_on(message):
    global estado
    global mensaje
    global modo
    modo=True
    bot.reply_to(message,"\U00002600 FloraFlow encendido \U00002600")
    estado=True
    mensaje=message
    
@bot.message_handler(commands=['apaga'])
def turn_off(message):
    global estado
    global modo
    modo=False
    bot.reply_to(message,"\U0001F311 FloraFlow apagado \U0001F311")
    estado=False

@bot.message_handler(commands=['comienzaRiego'])
def turn_off(message):
    global instruccion
    global modo
    if modo:
        bot.reply_to(message,"\U0001F6A8 Coriendo en modo automatico, no es posible \U0001F6A8")
    else:
        bot.reply_to(message,"\U0001F4A5 Regando la planta \U0001F4A5")
        instruccion=1

@bot.message_handler(commands=['terminaRiego'])
def turn_off(message):
    global instruccion
    global modo
    if modo:
        bot.reply_to(message,"\U0001F6A8 Coriendo en modo automatico, no es posible \U0001F6A8")
    else:
        bot.reply_to(message,"\U0001F4A5 Se termino de regar \U0001F4A5")
        instruccion=2

@bot.message_handler(commands=['abreTecho'])
def turn_off(message):
    global instruccion
    global modo
    if modo:
        bot.reply_to(message,"\U0001F6A8 Coriendo en modo automatico, no es posible \U0001F6A8")
    else:
        bot.reply_to(message,"\U0001F4A5 Abriendo el techo \U0001F4A5")
        instruccion=3

@bot.message_handler(commands=['cierraTecho'])
def turn_off(message):
    global instruccion
    global modo
    if modo:
        bot.reply_to(message,"\U0001F6A8 Coriendo en modo automatico, no es posible \U0001F6A8")
    else:
        bot.reply_to(message,"\U0001F4A5 Cerrando el techo \U0001F4A5")
        instruccion=4

bot.infinity_polling()