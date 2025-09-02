import cv2

img = cv2.imread(r"C:\Users\ECP6NA-10\Downloads\atividade-main\atividade-main\aula\media\exemplo.jpg")
# Selecionar região (y1:y2, x1:x2)
roi = img[50:200, 100:300]

cv2.imshow("Original", img)
cv2.imshow("Recorte", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()