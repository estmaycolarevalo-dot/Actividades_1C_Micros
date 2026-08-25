import cv2
import serial
import time
from ultralytics import YOLO

PUERTO_SERIAL = 'COM3'  
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Conexión serial establecida en {PUERTO_SERIAL}")
except Exception as e:
    print(f"Modo solo pantalla: {e}")
    esp32 = None

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    deteccion = "NONE"

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf = float(box.conf[0])

            if conf > 0.50:
                if cls_name == 'car':
                    deteccion = "CARRO"
                    break
                elif cls_name in ['motorcycle', 'motorbike']:
                    deteccion = "MOTO"
                    break

    if deteccion == "CARRO":
        print("-> Detección actual: CARRO (LED Rojo ON)")
        if esp32:
            esp32.write(b'CARRO\n')
    elif deteccion == "MOTO":
        print("-> Detección actual: MOTO (LED Verde ON)")
        if esp32:
            esp32.write(b'MOTO\n')
    else:
        print("Buscando vehículos...")
        if esp32:
            esp32.write(b'NONE\n')

    annotated_frame = results[0].plot()
    cv2.imshow("Detección YOLO", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if esp32:
    esp32.close()
cv2.destroyAllWindows()
