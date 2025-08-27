import cv2
import numpy as np

# Canvas size
WIDTH, HEIGHT = 960, 540

# Create white canvas
canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

# Initial settings
mode = "line"      # Default drawing mode
drawing = False    # Indicates if mouse left button is pressed
start_pt = None    # Starting point of drawing
curr_pt = None     # Current mouse point (for preview)


def put_help(img):
    """Draws a help bar with shortcuts on top of the image."""
    txt = "Teclas: [1]Linha [2]Ret [3]Circ [4]Livre | [c] limpar [s] salvar [ESC] sair"
    cv2.rectangle(img, (0, 0), (WIDTH, 30), (240, 240, 240), -1)
    cv2.putText(img, txt, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)


def mouse_cb(event, x, y, flags, param):
    """Controls drawing with the mouse."""
    global drawing, start_pt, curr_pt, canvas, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_pt = (x, y)
        curr_pt = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        curr_pt = (x, y)
        if drawing and mode == "free":
            cv2.line(canvas, start_pt, curr_pt, (50, 50, 50), 2)
            start_pt = curr_pt  # update for continuous line

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == "line":
            cv2.line(canvas, start_pt, (x, y), (0, 0, 255), 2)
        elif mode == "rect":
            cv2.rectangle(canvas, start_pt, (x, y), (0, 128, 255), 2)
        elif mode == "circle":
            r = int(((x - start_pt[0])**2 + (y - start_pt[1])**2)**0.5)
            cv2.circle(canvas, start_pt, r, (0, 255, 0), 2)


# Create window and set mouse callback
cv2.namedWindow("Canvas", cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("Canvas", mouse_cb)

# Main loop
while True:
    display = canvas.copy()

    # Preview drawing (line, rect, circle)
    if drawing and mode in ("line", "rect", "circle") and start_pt and curr_pt:
        if mode == "line":
            cv2.line(display, start_pt, curr_pt, (0, 0, 255), 1)
        elif mode == "rect":
            cv2.rectangle(display, start_pt, curr_pt, (0, 128, 255), 1)
        elif mode == "circle":
            r = int(((curr_pt[0] - start_pt[0])**2 +
                     (curr_pt[1] - start_pt[1])**2)**0.5)
            cv2.circle(display, start_pt, r, (0, 255, 0), 1)

    # Show help bar
    put_help(display)
    cv2.imshow("Canvas", display)

    # Keyboard events
    k = cv2.waitKey(20) & 0xFF
    if k == 27:  # ESC
        break
    elif k == ord('c'):
        canvas[:] = 255
    elif k == ord('s'):
        cv2.imwrite("canvas_saida.png", canvas)
        print("Imagem salva em canvas_saida.png")
    elif k == ord('1'):
        mode = "line"
    elif k == ord('2'):
        mode = "rect"
    elif k == ord('3'):
        mode = "circle"
    elif k == ord('4'):
        mode = "free"

cv2.destroyAllWindows()
