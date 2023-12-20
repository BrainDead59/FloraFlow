import Adafruit_DHT
from gpiozero import AngularServo
from time import sleep

sensor=Adafruit_DHT.DHT22
servo = AngularServo(12, min_pulse_width=0.0006, max_pulse_width=0.0023)
pin=16

try:
    while True:
        humedad,temperatura = Adafruit_DHT.read(sensor,pin)
        if humedad is not None and temperatura is not None:
            print("Temperatura={0:0.1f}C Humedad={1:0.1f}%".format(temperatura,humedad))
            if temperatura < 28:
                servo.angle = 90
            else:
                servo.angle = 0  
        sleep(3)
        
except KeyboardInterrupt:
    print("Programa detenido. Pines limpiados y GPIO liberado.")