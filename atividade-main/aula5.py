
import cv2

img = cv2.imread(r"C:\Users\ECP6NA-10\Downloads\atividade-main\atividade-main\aula\media\exemplo.jpg")
negativo = 255 - img

cv2.imshow("Original", img)
cv2.imshow("Negativo", negativo)
cv2.waitKey(0)
cv2.destroyAllWindows()