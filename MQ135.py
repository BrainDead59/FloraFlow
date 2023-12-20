import RPi.GPIO as GPIO
import time

DIGITAL_PIN = 16

# Configura el umbral de voltaje para la detección del gas
UMBRAL_VOLTAGE = 1.0

# Configura la numeración de pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Configura el pin como entrada
GPIO.setup(DIGITAL_PIN, GPIO.IN)

try:
    while True:
        # Lee el estado del pin digital (0 o 1)
        gas_detected = GPIO.input(DIGITAL_PIN)
        
        if not gas_detected:
            print("Gas detectado")
        else:
            print("No se detecta gas")
        
        time.sleep(1)  # Espera 1 segundo antes de la próxima lectura

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa detenido. Pines limpiados y GPIO liberado.")

