import speech_recognition as sr
import serial
import time

ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Sistema listo. Di 'rojo', 'verde' o 'apagar'.")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)

while True:
    with mic as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES").lower()
        print(f"Escuché: {texto}")

        if "rojo" in texto:
            ser.write(b'C\n')
        elif "verde" in texto:
            ser.write(b'M\n')
        elif "apagar" in texto:
            ser.write(b'N\n')

    except sr.UnknownValueError:
        print("No entendí, intenta de nuevo")
    except sr.RequestError:
        print("Error de conexión con el servicio de reconocimiento")
