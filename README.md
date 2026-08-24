# Actividad 2: Integración de la ESP32 con YOLO y MicroPython

## 🔗 Enlace a la Simulación en Wokwi
* [Ver Proyecto y Circuito Interactivo en Wokwi](https://wokwi.com/projects/473196769659239425)

---

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

* **Paso 1: Configuración del Circuito en Wokwi**
Se conectan las salidas digitales a las resistencias de limitación de corriente para encender el **LED Rojo en GPIO 4** y el **LED Verde en GPIO 2**. Las entradas digitales en **GPIO 34** y **GPIO 35** reciben la señal lógica de los eventos de clasificación.
* **Paso 2: Entrenamiento / Selección del Modelo YOLO**
Se toma un modelo YOLO entrenado con el dataset COCO (el cual ya incluye las clases `car` y `motorbike` por defecto) o un dataset personalizado de juguetes mediante supervisión de etiquetas.
* **Paso 3: Canal de Comunicación con el Embebido**
Dado que ejecutar una red convolucional compleja como YOLO directamente en el microcontrolador desborda la SRAM de la ESP32, el procesamiento de visión se realiza en una computadora host mediante Python/OpenCV. Al detectar el objeto `car` o `motorbike`, el script envía una señal de bandera por puerto serie (UART) a la ESP32.
* **Paso 4: Evaluación de Condicionales en MicroPython**
El firmware cargado en la ESP32 lee continuamente la señal recibida (simulada por hardware mediante los pulsadores de la imagen):
* Al recibir el evento de **Carro**, la ESP32 conmuta la salida del GPIO 4 a nivel alto (3.3V), encendiendo el **LED Rojo**.
* Al recibir el evento de **Moto**, conmuta la salida del GPIO 2 a nivel alto, encendiendo el **LED Verde**.
* Si la clase no corresponde o finaliza la detección, las salidas retornan a cero lógico.



```

```
