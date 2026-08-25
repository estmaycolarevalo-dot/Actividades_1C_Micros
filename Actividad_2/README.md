# Actividad 2: Integración de la ESP32 con YOLO y MicroPython

## 🔗 Enlace a la Simulación en Wokwi
* [Ver Proyecto y Circuito Interactivo en Wokwi](https://wokwi.com/projects/473196769659239425)

---
<img width="882" height="801" alt="image" src="https://github.com/user-attachments/assets/df999192-c36d-4c30-a2d4-ad6d7ce769c8" />

## 1. Código de Control en MicroPython

from machine import Pin
from time import sleep

btn_rojo = Pin(13, Pin.IN, Pin.PULL_DOWN)
btn_azul = Pin(12, Pin.IN, Pin.PULL_DOWN)

led_rojo = Pin(18, Pin.OUT)
led_verde = Pin(4, Pin.OUT)

while True:
    if btn_rojo.value() == 1:
        led_rojo.value(1)
        led_verde.value(0)
    elif btn_azul.value() == 1:
        led_rojo.value(0)
        led_verde.value(1)
    else:
        led_rojo.value(0)
        led_verde.value(0)
        
    sleep(0.05)

## 2. Explicación de la Arquitectura YOLO

YOLO (*You Only Look Once*) es un algoritmo de detección de objetos en tiempo real que replantea la detección como un problema de regresión de mapeo directo de píxeles de imagen a coordenadas de cuadros delimitadores (*bounding boxes*) y probabilidades de clase.

* **Procesamiento de Red Convencional:** Divide la imagen de entrada en una cuadrícula de S X S. Cada celda es responsable de predecir los objetos cuyo centro cae dentro de ella.
* **Extracción de Características:** Utiliza una red neuronal convolucional (CNN) backbone (como Darknet o versiones optimizadas YOLOv8/v11) para extraer mapas de características a múltiples escalas.
* **Inferencia de una Solamente Pasada:** A diferencia de algoritmos basados en regiones (R-CNN), procesa la imagen completa en una sola evaluación hacia adelante (*forward pass*), logrando velocidades de procesamiento óptimas para ejecuciones en tiempo real.

---

## 3. Integración Paso a Paso con la Detección de Vehículos

* **Paso 1: Configuración del Circuito en la ESP32**
  Se configuraron dos salidas digitales para el control de los indicadores lumínicos: el **LED Rojo en el GPIO 18** (para la detección de carros) y el **LED Verde en el GPIO 4** (para la detección de motos). Ambas salidas inician en nivel bajo (`LOW`) y se comunican con el computador mediante el puerto serie a una tasa de **115200 baudios**.

* **Paso 2: Procesamiento Visual con YOLOv8 en el Host**
  Dado que la ejecución directa de redes neuronales convolucionales complejas excede la capacidad de cómputo del microcontrolador, la captura de video en tiempo real y la inferencia se ejecutan en la máquina host mediante Python, OpenCV y la librería `ultralytics` cargando el modelo preentrenado `yolov8n.pt`.

* **Paso 3: Protocolo de Comunicación Serial (UART)**
  El script en Python evalúa los objetos detectados por la cámara con un umbral de confianza superior al 50% (`conf > 0.50`):
  * Si la clase detectada es `car`, asigna la bandera `"CARRO"`.
  * Si la clase detectada es `motorcycle` o `motorbike`, asigna la bandera `"MOTO"`.
  * Si no se detectan vehículos de interés, asigna la bandera `"NONE"`.
  
  Esta instrucción se transmite a la ESP32 a través de `pyserial` codificada en bytes finalizando con salto de línea (por ejemplo, `b'CARRO\n'`).

* **Paso 4: Evaluación de Comandos en el Firmware de la ESP32**
  El firmware desarrollado en C++ lee continuamente el puerto serie mediante la función `Serial.readStringUntil('\n')`:
  * Al recibir la cadena `"CARRO"`, conmuta el **GPIO 18 (LED Rojo) a nivel alto (`HIGH`)** y el GPIO 4 a nivel bajo (`LOW`).
  * Al recibir la cadena `"MOTO"`, conmuta el **GPIO 4 (LED Verde) a nivel alto (`HIGH`)** y el GPIO 18 a nivel bajo (`LOW`).
  * Ante la ausencia de estos eventos (`"NONE"` u otro valor), conmuta ambos pines a nivel bajo (`LOW`), apagando los indicadores.
<img width="1080" height="1266" alt="image" src="https://github.com/user-attachments/assets/3f6e2305-d5ec-4331-aa4a-390617755176" />
<img width="938" height="1254" alt="image" src="https://github.com/user-attachments/assets/b3e94846-ee8f-4fd0-81c1-787a428d2ad3" />



```

```
