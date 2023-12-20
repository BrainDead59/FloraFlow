import RPi.GPIO as GPIO
import time

DIGITAL_PIN = 16

# Configura la numeración de pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Configura el pin como entrada
GPIO.setup(DIGITAL_PIN, GPIO.IN)

try:
    while True:
        # Lee el estado del pin digital (0 o 1)
        humedad = GPIO.input(DIGITAL_PIN)
        
        if humedad==0:
            print("Humedo")
        else:
            print("Seco")
        
        time.sleep(1)  # Espera 1 segundo antes de la próxima lectura

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa detenido. Pines limpiados y GPIO liberado.")

