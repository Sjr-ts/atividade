import cv2
import time

VIDEO_PATH = r"media\race.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise FileNotFoundError(f"Não foi possível carregar o vídeo: {VIDEO_PATH}")

# Obter FPS do vídeo
video_fps = cap.get(cv2.CAP_PROP_FPS)
if video_fps == 0:
    video_fps = 30  # fallback
delay = int(1000 / video_fps)

# Ler o primeiro frame
ok, frame = cap.read()
if not ok or frame is None or frame.size == 0:
    cap.release()
    cv2.destroyAllWindows()
    raise RuntimeError("Falha ao carregar o primeiro frame do vídeo.")

# Converter para BGR se estiver em grayscale
if len(frame.shape) == 2:
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

# --- Função para selecionar ROI válida ---
def get_valid_roi(window_name, frame):
    while True:
        roi = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_name)
        if roi != (0, 0, 0, 0):
            x, y, w, h = map(int, roi)
            if x >= 0 and y >= 0 and x + w <= frame.shape[1] and y + h <= frame.shape[0]:
                return roi
            else:
                print("⚠ ROI fora da área do frame. Tente novamente.")
        else:
            print("⚠ Nenhuma ROI válida foi selecionada. Tente novamente.")

roi = get_valid_roi("Selecione a área (ROI) e pressione ENTER/ESPAÇO", frame)

def create_kcf():
    if hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerKCF_create"):
        return cv2.legacy.TrackerKCF_create()
    if hasattr(cv2, "TrackerKCF_create"):
        return cv2.TrackerKCF_create()
    raise RuntimeError("KCF Tracker não disponível. Instale opencv-contrib-python.")

tracker = create_kcf()
ok_init = tracker.init(frame, roi)
if not ok_init:
    cap.release()
    cv2.destroyAllWindows()
    raise RuntimeError("Falha ao inicializar o tracker com a ROI.")

# --- Loop de tracking ---
while True:
    ok, frame = cap.read()
    if not ok or frame is None or frame.size == 0:
        break

    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    t0 = time.time()
    ok, box = tracker.update(frame)
    fps = 1.0 / max(time.time() - t0, 1e-6)

    if ok:
        x, y, w, h = map(int, box)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        status_txt = "OK"
    else:
        status_txt = "FALHOU"
        cv2.putText(frame, "Perda de tracking - pressione 'r' para redefinir ROI",
                    (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, f"KCF | FPS: {int(fps)} | {status_txt}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 200, 50), 2)

    cv2.imshow("KCF Tracking (ESC/Q sai | R redefine ROI)", frame)
    key = cv2.waitKey(delay) & 0xFF  # usar delay baseado no FPS do vídeo

    if key in (27, ord('q')):
        break

    if key == ord('r'):
        new_roi = get_valid_roi("Redefinir ROI (ENTER/ESPAÇO confirma, ESC cancela)", frame)
        tracker = create_kcf()
        tracker.init(frame, new_roi)

cap.release()
cv2.destroyAllWindows()
