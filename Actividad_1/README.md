# Actividad 1: Introducción y Arquitectura de la ESP-WROOM-32

## 1. Definición de la Placa ESP32, Estructura y Arquitectura

### Definición
La **ESP-WROOM-32** (o simplemente ESP32) es un módulo SoC (*System on Chip*) de alto rendimiento y bajo costo diseñado por **Espressif Systems**. Integra conectividad inalámbrica **Wi-Fi (802.11 b/g/n)** y **Bluetooth (v4.2 BR/EDR y Bluetooth Low Energy - BLE)**, lo que la convierte en una de las plataformas más utilizadas en proyectos de IoT (Internet de las Cosas), robótica y sistemas embebidos.

### Estructura y Arquitectura
* **Procesador:** Cuenta con un microprocesador dual-core (doble núcleo) **Tensilica Xtensa 32-bit LX6**, capaz de operar a frecuencias de reloj de hasta **240 MHz** y ofrecer un rendimiento de hasta 600 DMIPS.
* **Memoria Interna:**
  * **SRAM:** 520 KB para datos e instrucciones.
  * **ROM:** 448 KB para arranque y funciones del sistema.
  * **Memoria Flash Externa:** Generalmente incorpora 4 MB (ampliable vía SPI) para el almacenamiento de código y datos.
* **Coprocesador de Ultra Bajo Consumo (ULP):** Permite realizar mediciones de periféricos (como sensores o pines ADC) mientras los núcleos principales están en modo de suspensión profunda (*Deep Sleep*).
* **Gestión de Energía:** Incluye un regulador de voltaje incorporado, modos avanzados de ahorro de energía y gestión de reloj.

---

## 2. Características, Conexiones, Pines y Periféricos

### Características Principales
* **Voltaje de Operación:** 3.3V (Alimentación típica por puerto microUSB/USB-C a 5V mediante regulador interno).
* **Lógica I/O:** 3.3V (¡No soporta 5V directamente en sus pines de E/S!).
* **Consumo:** Desde microamperios (μA) en modo *Deep Sleep* hasta 240mA transmitiendo Wi-Fi/Bluetooth.

### Distribución de Pines (Pinout) y Conexiones
La placa breakout típica de ESP32 dispone de 30 o 38 pines. A continuación se resumen sus principales tipos y funciones de periféricos:

* **GPIO (General Purpose Input/Output):** Dispone de hasta 36 pines digitales configurables.
  * **Nota:** Algunos pines son solo de entrada (GPIO 34, 35, 36/VP, 39/VN).
* **ADC (Convertidor Analógico a Digital):**
  * Incluye 2 ADC de 12 bits de resolución (valores entre 0 y 4095).
  * **ADC1:** 8 canales (GPIOs 32-39). Es seguro usarlo junto con Wi-Fi.
  * **ADC2:** 10 canales. Compartido con las funciones de Wi-Fi (su uso puede entrar en conflicto cuando el Wi-Fi está encendido).
* **DAC (Convertidor Digital a Analógico):**
  * Posee **2 canales de 8 bits** reales (GPIO 25 y GPIO 26).
  * Permite generar señales analógicas de voltaje real (de 0V a 3.3V).
* **PWM (Pulse Width Modulation):**
  * Soporta PWM por hardware en todos los pines GPIO de salida a través del módulo **LEDC** (Low Power PWM Controller).
  * Ofrece resolución configurable (hasta 16 bits) y frecuencia programable.
* **Comunicaciones Serie:**
  * **UART:** 3 interfaces independientes.
  * **SPI:** 3 buses (SPI, HSPI, VSPI).
  * **I2C:** 2 interfaces principales (SDA/SCL configurables en casi cualquier GPIO).
  * **Touch Pins:** 10 capacitivos (pines sensitivos al tacto).

---

## 3. Cuadro Comparativo: Programación en C/C++ vs. MicroPython

| Criterio | Programación en C / C++ (ESP-IDF / Arduino IDE) | Programación en MicroPython |
| :--- | :--- | :--- |
| **Ventajas** | • **Rendimiento Máximo:** Ejecución rápida directamente sobre el hardware.<br>• **Control de Memoria:** Menor footprint y consumo optimizado de RAM/Flash.<br>• **Acceso Total:** Acceso completo al framework nativo ESP-IDF y sistemas operativos en tiempo real (FreeRTOS).<br>• **Gran Biblioteca:** Amplia ecosistema de librerías en C/C++. | • **Simplicidad:** Sintaxis limpia y fácil de aprender.<br>• **Desarrollo Rápido:** Prototipado ágil sin necesidad de recompilar el firmware constantemente.<br>• **REPL Interactivo:** Posibilidad de probar líneas de código directamente en la placa en tiempo real.<br>• **Gestión de Memoria:** Recolección de basura (*Garbage Collector*) automática. |
| **Desventajas** | • **Curva de Aprendizaje:** Requiere gestión manual de memoria y manejo de punteros.<br>• **Tiempos de Compilación:** Proceso de compilación y subida de firmware más lento.<br>• **Complejidad:** Mayor código para realizar tareas sencillas de alto nivel. | • **Menor Rendimiento:** Velocidad de ejecución más lenta por ser un lenguaje interpretado.<br>• **Uso de RAM:** Mayor consumo de memoria por el intérprete de Python.<br>• **Soporte de Hardware Limitado:** Algunos periféricos avanzados o funciones de bajo nivel de la ESP32 no están expuestos en todas las librerías. |
