import cv2

VIDEO_PATH = r"media\race.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise FileNotFoundError(f"Não foi possível carregar o vídeo: {VIDEO_PATH}")

while True:
    ok, frame = cap.read()

    if not ok:
        print("Fim do vídeo ou erro ao ler frame.")
        break

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
