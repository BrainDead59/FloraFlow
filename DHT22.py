import Adafruit_DHT
from time import sleep

sensor=Adafruit_DHT.DHT22
pin=16

try:
    while True:
        humedad,temperatura = Adafruit_DHT.read(sensor,pin)
        if humedad is not None and temperatura is not None:
            print("Temperatura={0:0.1f}C Humedad={1:0.1f}%".format(temperatura,humedad))
        else:
            print("Valores")
        sleep(3)
        
except KeyboardInterrupt:
    print("Programa detenido. Pines limpiados y GPIO liberado.")
