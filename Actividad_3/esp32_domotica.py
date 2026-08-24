import sys, select, time
from machine import Pin

led_rojo = Pin(18, Pin.OUT)
led_verde = Pin(19, Pin.OUT)

# Escucha el puerto serial (USB) sin bloquear el programa
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

print("ESP32 listo, esperando señales...")

while True:
    if poll.poll(0):
        linea = sys.stdin.readline().strip()
        if linea == 'C':
            led_rojo.value(1)
            led_verde.value(0)
        elif linea == 'M':
            led_verde.value(1)
            led_rojo.value(0)
        elif linea == 'N':
            led_rojo.value(0)
            led_verde.value(0)
    time.sleep(0.05)
