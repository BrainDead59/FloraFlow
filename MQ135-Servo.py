import RPi.GPIO as GPIO
from gpiozero import AngularServo
from time import sleep

DIGITAL_PIN = 16
servo = AngularServo(12, min_pulse_width=0.0006, max_pulse_width=0.0023)

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
            servo.angle = 90
        else:
            print("No se detecta gas")
            servo.angle = 0
        
        sleep(1)  # Espera 1 segundo antes de la próxima lectura

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa detenido. Pines limpiados y GPIO liberado.")
