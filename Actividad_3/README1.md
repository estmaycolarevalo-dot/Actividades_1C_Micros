# Actividad 3: Chatbot Domótico con Control por Voz (ESP32)

## 1. Descripción del Proyecto
Este proyecto implementa un chatbot domótico accionado por comandos de voz capaz de interpretar instrucciones verbales y enviar comandos a una placa ESP32 para controlar el encendido y apagado de un LED.

---

## 2. Puntos Desarrollados
* **Reconocimiento de Voz y Chatbot:** Procesamiento de audio en tiempo real para interpretar comandos domóticos (como encender o apagar dispositivos).
* **Control de Salidas (ESP32):** Recepción de peticiones y control del estado del pin GPIO donde está conectado el LED.
* **Integración del Sistema:** Enlace entre el script principal en Python (Chatbot) y la ESP32 mediante peticiones en red local / comunicación serial.

---

## 3. Diagrama de Conexión
* **LED:** Conectado a una salida digital (GPIO) de la ESP32 con su respectiva resistencia de protección a GND.
<img width="536" height="645" alt="image" src="https://github.com/user-attachments/assets/6e1b1a9e-4b89-4e0b-a0a8-6481d08e97a3" />


https://github.com/user-attachments/assets/8c853a81-4212-43c4-a05a-69172da969ed


---

## 4. Instrucciones de Ejecución
1. Cargar el firmware/script de control en la placa ESP32.
2. Asegurar la conexión a la misma red o puerto de comunicación.
3. Ejecutar el script principal del chatbot domótico:
   ```bash
   python chatbot_voz.py
