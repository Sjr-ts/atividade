import cv2

# Carregar imagem
img = cv2.imread(r"C:\Users\ECP6NA-10\Downloads\atividade-main\atividade-main\aula\media\exemplo.jpg")

# Exibir imagem em uma janela
cv2.imshow("Minha Imagem", img)

# Espera até pressionar uma tecla
cv2.waitKey(0)

cv2.destroyAllWindows()