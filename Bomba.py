import RPi.GPIO as GPIO
import time

# Configura el modo de los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Define el pin al que está conectado el relé
pin_rele = 20

# Configura el pin del relé como una salida
GPIO.setup(pin_rele, GPIO.OUT)

try:
    # Enciende la bomba de agua
    print("Encendiendo la bomba de agua")
    GPIO.output(pin_rele, GPIO.HIGH)
    
    # Espera durante un período de tiempo (por ejemplo, 10 segundos)
    time.sleep(1)
    
    # Apaga la bomba de agua
    print("Apagando la bomba de agua")
    GPIO.output(pin_rele, GPIO.LOW)

except KeyboardInterrupt:
    # Maneja la interrupción de teclado (Ctrl+C) para apagar la bomba de agua
    GPIO.output(pin_rele, GPIO.LOW)

finally:
    # Limpia los pines GPIO y termina
    GPIO.cleanup()
