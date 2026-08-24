# Actividad 3: Chatbot Domótico e Integración con YOLO

## 1. Descripción del Proyecto
Implementación de un chatbot domótico accionado por comandos de voz e integración con la arquitectura de visión por computador YOLO para el control del encendido y apagado de LEDs en una ESP32.

## 2. Puntos Desarrollados
* **Control por Voz:** Integración del chatbot para procesamiento de instrucciones domóticas.
* **Detección Visual (YOLO):**
  * **Carro de juguete:** Al ser detectado por la cámara, activa el **LED Rojo**.
  * **Moto de juguete:** Al ser detectada por la cámara, activa el **LED Verde**.
* **ESP32:** Control de salidas GPIO a través de peticiones enviadas desde el script principal.

## 3. Diagrama de Conexión y Wokwi
* **LED Rojo:** Conectado al GPIO 12.
* **LED Verde:** Conectado al GPIO 14.
* **Enlace al circuito interactivo:** [Insertar Link de Wokwi si aplica]

## 4. Instrucciones de Ejecución
1. Cargar el firmware/script en la ESP32.
2. Ejecutar el detector y chatbot:
   ```bash
   python chatbot_voz.py
