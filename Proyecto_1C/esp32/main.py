import sys, select, time, math
from machine import Pin, PWM, I2C
import ssd1306

SERVO_PIN = 13
PIR_PIN = 14
LUZ_PIN = 4
LUZ_PIN_2 = 25
LUZ_PIN_3 = 26
LUZ_PIN_4 = 27
LED_ROJO_PIN = 18
LED_VERDE_PIN = 19
I2C_SDA = 21
I2C_SCL = 22

led_rojo = Pin(LED_ROJO_PIN, Pin.OUT)
led_verde = Pin(LED_VERDE_PIN, Pin.OUT)
led_rojo.value(0)
led_verde.value(1)

pir = Pin(PIR_PIN, Pin.IN)

servo = PWM(Pin(SERVO_PIN), freq=50)

def set_angle(angle):
    angle = max(0, min(180, angle))
    servo.freq(50)
    pulso_us = 500 + (angle / 180) * 2000
    duty = int(pulso_us / 20000 * 65535)
    servo.duty_u16(duty)

VENTANA_CERRADA = 180
VENTANA_ABIERTA = 120
ventana_abierta = False
set_angle(VENTANA_CERRADA)

luz = PWM(Pin(LUZ_PIN), freq=1000)
luz2 = PWM(Pin(LUZ_PIN_2), freq=1000)
luz3 = PWM(Pin(LUZ_PIN_3), freq=1000)
luz4 = PWM(Pin(LUZ_PIN_4), freq=1000)
luces = (luz, luz2, luz3, luz4)
for l in luces:
    l.duty(0)

NIVELES_LUZ = {0: 0, 1: 300, 2: 650, 3: 1023}
modo_luz_auto = True
nivel_luz_actual = 0

def aplicar_luz(nivel):
    global nivel_luz_actual
    nivel_luz_actual = nivel
    duty = NIVELES_LUZ.get(nivel, 0)
    for l in luces:
        l.duty(duty)

i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

MPU_ADDR = 0x68
mpu_disponible = True
try:
    i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')
except OSError:
    mpu_disponible = False
    print("MPU6050 no detectado: la alerta sísmica queda desactivada.")

def leer_accel():
    datos = i2c.readfrom_mem(MPU_ADDR, 0x3B, 6)

    def conv(alto, bajo):
        val = (alto << 8) | bajo
        if val > 32767:
            val -= 65536
        return val / 16384.0

    ax = conv(datos[0], datos[1])
    ay = conv(datos[2], datos[3])
    az = conv(datos[4], datos[5])
    return ax, ay, az

def magnitud_vibracion():
    if not mpu_disponible:
        return 0.0
    try:
        ax, ay, az = leer_accel()
        mag = math.sqrt(ax * ax + ay * ay + az * az)
        return abs(mag - 1.0)
    except OSError:
        return 0.0

UMBRAL_LEVE = 0.15
UMBRAL_FUERTE = 0.35

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

def procesar_comando(cmd):
    global ventana_abierta, modo_luz_auto
    cmd = cmd.strip()
    if cmd == 'W1':
        set_angle(VENTANA_ABIERTA)
        ventana_abierta = True
    elif cmd == 'W0':
        set_angle(VENTANA_CERRADA)
        ventana_abierta = False
    elif cmd == 'LA':
        modo_luz_auto = True
    elif cmd in ('L0', 'L1', 'L2', 'L3'):
        modo_luz_auto = False
        aplicar_luz(int(cmd[1]))

ultimo_movimiento = 0
TIEMPO_APAGADO_AUTO = 8
ultimo_parpadeo = 0
estado_parpadeo = False

print("Sótano inteligente listo. Esperando comandos y monitoreando sensores...")

while True:
    try:
        ahora = time.time()

        if poll.poll(0):
            linea = sys.stdin.readline()
            procesar_comando(linea)

        movimiento = pir.value()
        if movimiento:
            ultimo_movimiento = ahora
            if modo_luz_auto:
                aplicar_luz(2)
        else:
            if modo_luz_auto and (ahora - ultimo_movimiento > TIEMPO_APAGADO_AUTO):
                aplicar_luz(0)

        vib = magnitud_vibracion()
        if vib >= UMBRAL_FUERTE:
            alerta_sismica = True
            nivel_sismo = "FUERTE"
        elif vib >= UMBRAL_LEVE:
            alerta_sismica = True
            nivel_sismo = "LEVE"
        else:
            alerta_sismica = False
            nivel_sismo = ""

        if alerta_sismica:
            led_verde.value(0)
            if ahora - ultimo_parpadeo > 0.2:
                estado_parpadeo = not estado_parpadeo
                led_rojo.value(estado_parpadeo)
                ultimo_parpadeo = ahora
        else:
            led_rojo.value(0)
            led_verde.value(1)

        oled.fill(0)
        if alerta_sismica:
            oled.text("!! ALERTA !!", 10, 0)
            oled.text("Sismo: " + nivel_sismo, 10, 20)
            oled.text("Revisar sotano", 5, 40)
        else:
            oled.text("Sotano OK", 20, 0)
            oled.text("Mov: " + ("SI" if movimiento else "NO"), 0, 16)
            oled.text("Ventana: " + ("ABIERTA" if ventana_abierta else "CERRADA"), 0, 30)
            modo_txt = "AUTO" if modo_luz_auto else "MANUAL"
            oled.text("Luz: " + modo_txt + " (" + str(nivel_luz_actual) + ")", 0, 44)
            if not mpu_disponible:
                oled.text("(MPU6050 offline)", 0, 56)
        oled.show()

    except Exception as e:
        print("Error en el ciclo (ignorado, sigue corriendo):", e)

    time.sleep(0.1)
