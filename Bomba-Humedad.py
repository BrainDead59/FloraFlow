import RPi.GPIO as GPIO
import time

DIGITAL_PIN = 16
pin_rele = 12

# Configura la numeración de pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configura el pin como entrada
GPIO.setup(DIGITAL_PIN, GPIO.IN)
GPIO.setup(pin_rele, GPIO.OUT)

try:
    while True:
        # Lee el estado del pin digital (0 o 1)
        humedad = GPIO.input(DIGITAL_PIN)
        
        if humedad==0:
            GPIO.output(pin_rele, GPIO.LOW)
        else:
            GPIO.output(pin_rele, GPIO.HIGH)
        
        time.sleep(1)  # Espera 1 segundo antes de la próxima lectura

except KeyboardInterrupt:
    GPIO.output(pin_rele, GPIO.LOW)

finally:
    # Limpia los pines GPIO y termina
    GPIO.cleanup()
    print("Programa detenido. Pines limpiados y GPIO liberado.")


