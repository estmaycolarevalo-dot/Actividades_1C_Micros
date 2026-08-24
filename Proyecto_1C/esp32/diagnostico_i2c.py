from machine import Pin, I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
dispositivos = i2c.scan()

print("Dispositivos I2C encontrados:", dispositivos)

if 60 in dispositivos:
    print("OLED (0x3c) detectado correctamente.")
else:
    print("OLED NO detectado. Revisa VCC, GND, SDA (21) y SCL (22).")

if 104 in dispositivos:
    print("MPU6050 (0x68) detectado correctamente.")
else:
    print("MPU6050 NO detectado.")
