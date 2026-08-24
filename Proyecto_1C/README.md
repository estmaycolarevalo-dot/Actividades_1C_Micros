# 🏠 Sótano Inteligente — Sistema IoT con ESP32

**Reto propuesto:** Sótano Inteligente
**Requisitos cubiertos:** Ventana inteligente · Sensor de movimiento · Iluminación de varias intensidades · OLED con alerta temprana sísmica

Sistema de automatización para un sótano, construido sobre un **ESP32** programado en **MicroPython**, con control manual por **voz desde una PC** (Python + reconocimiento de voz). Integra apertura de ventana, iluminación de varias intensidades, detección de movimiento y alerta temprana sísmica.

# Arquitectura del sistema
<img width="1076" height="651" alt="image" src="https://github.com/user-attachments/assets/33810777-ef85-49aa-81c9-698396f14c6e" />


---

## 📋 Tabla de contenidos

- [1. Introducción y objetivo](#1-introducción-y-objetivo)
- [2. Diseño](#2-diseño)
- [3. Simulación y validación](#3-simulación-y-validación)
- [4. Implementación](#4-implementación)
- [5. Explicación del funcionamiento](#5-explicación-del-funcionamiento)
- [6. Tecnologías utilizadas](#6-tecnologías-utilizadas)
- [7. Problemas encontrados y soluciones](#7-problemas-encontrados-y-soluciones)
- [8. Instalación y puesta en marcha](#9-instalación-y-puesta-en-marcha)
- [9. Comandos de voz disponibles](#10-comandos-de-voz-disponibles)
- [10. Estado actual del MPU6050](#11-estado-actual-del-mpu6050)
- [11. Conclusiones y mejoras futuras](#12-conclusiones-y-mejoras-futuras)

---

## 1. Introducción y objetivo

El reto consistía en diseñar un sistema de automatización para un sótano que cumpliera con cuatro requisitos funcionales: una ventana que pudiera abrirse/cerrarse de forma inteligente, detección de movimiento, iluminación con varias intensidades, y una pantalla que mostrara alertas tempranas ante actividad sísmica. Se decidió usar un **ESP32** como controlador central por su capacidad de manejar múltiples periféricos (PWM, I2C, GPIO digital) simultáneamente, y se añadió como valor agregado un **control manual por voz** desde una PC, para dar al usuario control directo sobre la ventana y la iluminación además de la lógica automática.

## 2. Diseño

### 2.1 Requisitos funcionales del reto y su solución de diseño

| Requisito del reto | Solución elegida | Justificación |
|---|---|---|
| Ventana inteligente | Servomotor SG90 controlado por PWM, activado por comando de voz | Se decidió que la apertura de ventana sea una decisión manual (no automática), ya que abrir o cerrar una ventana depende de criterio humano (clima, ventilación deseada), no de un sensor. |
| Sensor de movimiento | Sensor PIR HC-SR501 | Es el estándar en proyectos de detección de presencia por bajo costo y facilidad de integración digital (una sola salida HIGH/LOW). |
| Iluminación de varias intensidades | 4 LEDs controlados por PWM, sincronizados a un mismo nivel | El PWM permite variar el "brillo promedio" percibido variando el ciclo de trabajo (duty cycle), sin necesitar componentes analógicos adicionales. Se usaron 4 LEDs para simular una cobertura de iluminación más realista del espacio. |
| OLED con alerta sísmica | Pantalla SSD1306 (I2C) + acelerómetro MPU6050 (I2C) | El MPU6050 permite calcular la magnitud de vibración respecto al reposo (1g); superando un umbral, se considera actividad sísmica y se refleja en la pantalla en tiempo real. |

### 2.2 Arquitectura general

El sistema se dividió en dos nodos que se comunican por **puerto serial (USB)**:

1. **Nodo ESP32 (embebido)** — corre `esp32/main.py` en MicroPython. Es el controlador central: lee los sensores en un ciclo continuo (~10 veces por segundo), toma decisiones automáticas (luz por PIR, alarma por MPU6050), y ejecuta los comandos manuales que le llegan por serial (ventana, override de luz).
2. **Nodo PC (control por voz)** — corre `pc/voz_control_pc.py` en Python estándar. Captura audio del micrófono, lo transcribe a texto con la API de reconocimiento de voz de Google, interpreta el comando, y lo envía como un código corto (ej. `W1`, `L3`) por el puerto serial hacia el ESP32.

Ver el diagrama completo en [`docs/arquitectura.svg`](docs/arquitectura.svg).

### 2.3 Protocolo de comunicación (diseño de mensajes)

Se diseñó un protocolo de texto simple, un comando por línea (terminado en `\n`), para minimizar la complejidad de parseo en MicroPython:

| Comando | Efecto |
|---|---|
| `W1` | Abrir ventana (servo) |
| `W0` | Cerrar ventana (servo) |
| `L0` | Luz manual — apagada |
| `L1` | Luz manual — baja |
| `L2` | Luz manual — media |
| `L3` | Luz manual — alta |
| `LA` | Volver a modo automático de luz (control por PIR) |

### 2.4 Selección de pines (diagrama de conexiones)

| Componente | Pin(es) en ESP32 | Alimentación |
|---|---|---|
| Servo SG90 (ventana) | GPIO13 (señal) | 5V / VIN |
| Sensor PIR HC-SR501 | GPIO14 (OUT) | 5V |
| MPU6050 (I2C) | SDA=GPIO21, SCL=GPIO22, AD0→GND | 3.3V |
| OLED SSD1306 (I2C) | SDA=GPIO21, SCL=GPIO22 | 3.3V |
| 4x LED iluminación | GPIO4, GPIO25, GPIO26, GPIO27 | 3.3V (vía GPIO) |
| LED de alarma (rojo) | GPIO18 | 3.3V (vía GPIO) |
| LED de estado (verde) | GPIO19 | 3.3V (vía GPIO) |

> ⚠️ El OLED y el MPU6050 comparten el mismo bus I2C (SDA=21, SCL=22) — esto es una decisión de diseño válida en I2C: cada dispositivo responde en una dirección distinta (`0x3C` para el OLED, `0x68` para el MPU6050), por lo que ambos pueden convivir en el mismo bus sin conflicto.

## 3. Simulación y validación

En vez de simular el circuito en software antes de construirlo, se optó por un enfoque de **validación incremental sobre hardware real**: cada subsistema (servo, PIR, luces, OLED, MPU6050) se programó y probó de forma aislada con pequeños scripts de diagnóstico antes de integrarlo al programa principal. Este enfoque permitió detectar y corregir fallas específicas de cada componente sin que un error en un subsistema ocultara o afectara la validación de los demás. Los scripts de prueba usados durante el desarrollo están documentados en la sección [7](#7-problemas-encontrados-y-soluciones), y ejemplos de ellos se incluyen en `esp32/diagnostico_i2c.py`.

Esta metodología de "probar cada pieza por separado antes de integrar" es equivalente en espíritu a una simulación por software (aislar variables para confirmar el comportamiento esperado de cada bloque), pero realizada directamente sobre el hardware final, lo cual también permitió detectar fallas reales de componentes (ver sección 11) que una simulación en software no habría revelado.

## 4. Implementación

### 4.1 Requisitos de hardware

- 1x ESP32 DevKit
- 1x Servomotor SG90
- 1x Sensor PIR HC-SR501
- 1x MPU6050 (acelerómetro/giroscopio)
- 1x Pantalla OLED SSD1306 128x64 (I2C)
- 4x LED + resistencias 220-330Ω (iluminación)
- 1x LED rojo + resistencia (alarma)
- 1x LED verde + resistencia (estado)
- Protoboard y cables jumper

### 4.2 Requisitos de software

- Firmware MicroPython v1.28.0 en el ESP32
- Thonny IDE (programación del ESP32)
- Python 3.12 (PC) + librerías `SpeechRecognition`, `pyaudio`, `pyserial`
- Visual Studio Code (desarrollo del script de PC)

## 5. Explicación del funcionamiento

### Iluminación (automática + manual)
El PIR se lee en cada ciclo. Si detecta movimiento, enciende la luz a nivel medio automáticamente y mantiene ese estado; si no hay movimiento por más de 8 segundos, la apaga. Si llega un comando de voz (`L0`-`L3`), el sistema pasa a **modo manual** y fija ese nivel hasta que se reciba el comando `LA` (auto), que devuelve el control al PIR.

### Ventana (manual)
El servo se mueve exclusivamente por comando de voz (`W1`/`W0`), moviéndose 60° entre la posición cerrada y abierta.

### Alerta sísmica
El MPU6050 entrega la aceleración en 3 ejes. En reposo, la magnitud combinada de esos 3 valores es ≈1g (solo gravedad). El sistema calcula qué tan lejos está esa magnitud de 1g en cada ciclo; si la desviación supera un umbral, se considera vibración anómala:

- `< 0.15` → sin alerta
- `0.15 – 0.35` → alerta **leve**
- `≥ 0.35` → alerta **fuerte**

Durante la alerta, el LED rojo parpadea (cada 0.2s), el LED verde se apaga, y el OLED muestra el aviso. En cuanto la vibración vuelve a estar bajo el umbral, el sistema regresa solo al estado normal.

### Panel OLED
Se refresca en cada ciclo del programa, mostrando: estado de movimiento, estado de la ventana, modo y nivel de luz actual, y la alerta sísmica cuando corresponde.

## 6. Tecnologías utilizadas

- **MicroPython** — firmware y lenguaje que corre directamente en el ESP32.
- **Protocolo I2C** — comunicación con OLED y MPU6050 (bus compartido, direcciones distintas).
- **PWM (Pulse Width Modulation)** — controla el ángulo del servo y la intensidad (brillo) de los LEDs.
- **Comunicación serial (UART sobre USB)** — enlace entre el ESP32 y la PC.
- **Python 3** (en PC) — control de voz y puente serial.
- **SpeechRecognition + PyAudio** — captura y transcripción de audio.
- **API de reconocimiento de voz de Google** — convierte audio a texto (requiere conexión a internet).
- **pyserial** — librería de Python para comunicación por puerto serial.
- **Thonny IDE** — entorno usado para programar y depurar el ESP32.

## 7. Problemas encontrados y soluciones

Durante el desarrollo se presentaron varios problemas reales de integración hardware/software, documentados aquí como parte del proceso de ingeniería del proyecto:

| Problema | Diagnóstico | Solución aplicada |
|---|---|---|
| El servo giraba sin control al recibir cualquier ángulo | Al agregar el PWM de la luz (freq=1000Hz), el ESP32 reconfiguró el temporizador de hardware compartido con el del servo (freq=50Hz) | Se reafirma `servo.freq(50)` antes de cada movimiento. En un intento posterior se descubrió que el servo físico usado era de rotación continua, no posicional — se reemplazó por un servo posicional adecuado. |
| `OSError: [Errno 19] ENODEV` al iniciar el MPU6050 | El pin AD0 no estaba conectado a GND, causando que el sensor respondiera en la dirección alterna (0x69) en vez de la esperada (0x68) | Se conectó AD0 a GND físicamente, confirmando con `i2c.scan()` que el sensor respondía en 0x68. |
| El sistema dejaba de responder a comandos después de un rato | El programa `main.py` se detenía silenciosamente ante cualquier excepción no controlada (p.ej. un error transitorio de I2C) | Se envolvió el ciclo principal completo en un bloque `try/except`, de forma que un error puntual se registra en consola pero no detiene el programa. |
| `OSError: [Errno 116] ETIMEDOUT` al iniciar el OLED | Un cable del bus I2C se soltó físicamente al manipular la protoboard | Se realizaron pruebas de aislamiento (desconectar cada dispositivo I2C por separado, correr `i2c.scan()`) para identificar cuál dispositivo específico había perdido conexión. |
| El comando de voz "luz automática" nunca se reconocía | El texto transcrito por la API de Google incluía tildes (`automática`), pero el código comparaba contra la palabra sin tilde (`automatica`) | Se agregó una función de normalización de texto (`unicodedata`) que elimina acentos del texto reconocido antes de compararlo con los comandos. |
| `pyaudio` fallaba al instalar, pidiendo un compilador de C++ | El entorno virtual usaba Python 3.14, una versión demasiado nueva sin wheels precompilados disponibles para esa librería en Windows | Se recreó el entorno virtual con Python 3.12, que sí cuenta con wheels precompilados para todas las dependencias. |
| El MPU6050 dejó de responder por completo en el bus I2C | Pruebas de aislamiento (con solo el MPU6050 conectado, sin el OLED) confirmaron que el sensor no respondía bajo ninguna configuración de cableado válida | Se determinó que el sensor sufrió una falla de hardware. Ver sección 11 para el manejo de este caso en el código. |


## 8. Instalación y puesta en marcha

### En el ESP32 (Thonny)
1. Flashear MicroPython en el ESP32 (si no lo tiene ya).
2. Abrir `esp32/main.py` y `esp32/ssd1306.py` en Thonny.
3. Guardar ambos en el dispositivo (`Archivo → Guardar como → MicroPython device`), guardando `main.py` con ese nombre exacto para que se ejecute automáticamente al encender.
4. Conectar todos los componentes según la tabla de conexiones (sección 2.4).
5. Alimentar el ESP32 por USB; el sistema arranca solo.

### En la PC (control por voz)
1. Crear un entorno virtual con Python 3.11 o 3.12 (evitar versiones muy nuevas por compatibilidad de librerías):
   ```bash
   py -3.12 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Instalar dependencias:
   ```bash
   pip install SpeechRecognition pyaudio pyserial
   ```
3. Ajustar el puerto COM en `pc/voz_control_pc.py`.
4. Ejecutar:
   ```bash
   python pc/voz_control_pc.py
   ```

## 9. Comandos de voz disponibles

| Frase | Acción |
|---|---|
| "abrir ventana" | Abre el servo de la ventana |
| "cerrar ventana" | Cierra el servo de la ventana |
| "luz alta" | Iluminación al máximo (manual) |
| "luz media" | Iluminación media (manual) |
| "luz baja" | Iluminación baja (manual) |
| "luz apagada" / "apagar luz" | Apaga la luz (manual) |
| "luz automática" / "modo automático" | Devuelve el control de la luz al sensor PIR |

## 10. Estado actual del MPU6050

El requisito de "OLED con alerta temprana sísmica" está **completamente implementado en el código** (`esp32/main.py`, funciones `leer_accel()` y `magnitud_vibracion()`), y fue validado funcionalmente durante el desarrollo: el sistema detectaba correctamente vibraciones simuladas (golpes suaves sobre la mesa de montaje) y mostraba la alerta en el OLED junto con el parpadeo del LED rojo, tal como se describe en la sección 5.

Durante las últimas etapas del proyecto, el módulo MPU6050 físico utilizado presentó una **falla de hardware** (dejó de responder en el bus I2C bajo cualquier configuración de cableado válida, confirmado mediante pruebas de aislamiento — ver sección 7), y no fue posible conseguir un reemplazo a tiempo para la entrega. Por esta razón, el montaje físico actual de la maqueta funciona **sin el MPU6050 conectado**.

Para que esta falla puntual de un componente no comprometiera el resto del sistema, se implementó **detección automática de disponibilidad** del sensor:

```python
mpu_disponible = True
try:
    i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')
except OSError:
    mpu_disponible = False
    print("MPU6050 no detectado: la alerta sísmica queda desactivada.")
```

Si el sensor no responde al iniciar, el sistema continúa funcionando con normalidad (ventana, iluminación, PIR, OLED), mostrando el aviso `(MPU6050 offline)` en pantalla en vez de fallar. **En cuanto se conecte un MPU6050 en buen estado, el sistema lo detecta automáticamente sin requerir ningún cambio de código**, activando de nuevo la función de alerta sísmica.

## 11. Conclusiones y mejoras futuras

El proyecto permitió integrar múltiples protocolos de comunicación (I2C, PWM, UART/Serial) sobre un mismo microcontrolador, así como resolver problemas reales de integración hardware/software documentados en la sección 7 — experiencia que refleja el tipo de depuración que ocurre en proyectos de sistemas embebidos reales, más allá del código en sí.

**Mejoras futuras propuestas:**
- Envío de notificaciones (correo/Telegram) al detectar un sismo.
- Registro histórico de eventos (movimiento, sismos) en una tarjeta SD o servidor remoto.
- Interfaz web local para monitorear el sistema sin necesidad de la app de voz.
- Sensor de luz ambiental (LDR) para ajustar la iluminación según la luz natural disponible.
