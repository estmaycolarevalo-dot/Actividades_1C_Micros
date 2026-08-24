import speech_recognition as sr
import serial
import time
import unicodedata

PUERTO = 'COM3'
BAUDIOS = 115200

def quitar_acentos(texto):
    """Convierte 'automática' -> 'automatica', para que la comparación
    de comandos no falle por culpa de las tildes."""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Sistema listo. Comandos disponibles:")
print(" - abrir ventana / cerrar ventana")
print(" - luz baja / luz media / luz alta / luz apagada")
print(" - luz automatica")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)

def enviar(comando):
    ser.write((comando + '\n').encode())
    print(f"-> Enviado al ESP32: {comando}")

while True:
    with mic as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES").lower()
        texto = quitar_acentos(texto)
        print(f"Escuché: {texto}")

        if "abrir ventana" in texto:
            enviar("W1")
        elif "cerrar ventana" in texto:
            enviar("W0")
        elif "luz alta" in texto:
            enviar("L3")
        elif "luz media" in texto:
            enviar("L2")
        elif "luz baja" in texto:
            enviar("L1")
        elif "luz apagada" in texto or "apagar luz" in texto:
            enviar("L0")
        elif "luz automatica" in texto or "modo automatico" in texto:
            enviar("LA")
        else:
            print("Comando no reconocido, intenta de nuevo.")

    except sr.UnknownValueError:
        print("No entendí, intenta de nuevo")
    except sr.RequestError:
        print("Error de conexión con el servicio de reconocimiento")
