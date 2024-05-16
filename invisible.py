


import cv2 
import numpy as np 
import time 

# Função de callback vazia que é chamada para a criação de trackbars
def nothing(x):
    pass

# Cria uma janela chamada 'INVISIBLE Cloak'
cv2.namedWindow('INVISIBLE Cloak')

# Define os valores iniciais para capa azul (alterar de acordo com a preferência)
h_min_initial = 91
s_min_initial = 64
v_min_initial = 120
h_max_initial = 120
s_max_initial = 255
v_max_initial = 255

# Cria trackbars para ajustar os valores mínimo e máximo de H, S e V
cv2.createTrackbar('H_min', 'INVISIBLE Cloak', h_min_initial, 180, nothing)
cv2.createTrackbar('S_min', 'INVISIBLE Cloak', s_min_initial, 255, nothing)
cv2.createTrackbar('V_min', 'INVISIBLE Cloak', v_min_initial, 255, nothing)
cv2.createTrackbar('H_max', 'INVISIBLE Cloak', h_max_initial, 180, nothing)
cv2.createTrackbar('S_max', 'INVISIBLE Cloak', s_max_initial, 255, nothing)
cv2.createTrackbar('V_max', 'INVISIBLE Cloak', v_max_initial, 255, nothing)

# Inicia a captura de vídeo 
capture_video = cv2.VideoCapture(0)
time.sleep(1)
count = 0
background = 0 

# Captura o frame de fundo e inverte
for i in range(60): 
    return_val, background = capture_video.read() 
    if return_val == False : 
        continue 
    background = np.flip(background, axis = 1) 

# Loop principal(Captura dos frames e caso ocorra com sucesso é armazenado em count e
# é transformado para hsv)
while (capture_video.isOpened()): 
    return_val, img = capture_video.read() 
    if not return_val : 
        break 
    count = count + 1
    img = np.flip(img, axis = 1) 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    # Obtém os valores das trackbars
    h_min = cv2.getTrackbarPos('H_min', 'INVISIBLE Cloak')
    s_min = cv2.getTrackbarPos('S_min', 'INVISIBLE Cloak')
    v_min = cv2.getTrackbarPos('V_min', 'INVISIBLE Cloak')
    h_max = cv2.getTrackbarPos('H_max', 'INVISIBLE Cloak')
    s_max = cv2.getTrackbarPos('S_max', 'INVISIBLE Cloak')
    v_max = cv2.getTrackbarPos('V_max', 'INVISIBLE Cloak')

    # Define os limites de cor para a detecção
    lower_color = np.array([h_min, s_min, v_min])        
    upper_color = np.array([h_max, s_max, v_max]) 
    mask1 = cv2.inRange(hsv, lower_color, upper_color)  

    # Aplica transformações morfológicas para remover ruído
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),np.uint8), iterations = 2) #abertura para remover ruidos
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1) #dilata(aumenta o tamanho das bordas) para suavizar as bordas
    mask2 = cv2.bitwise_not(mask1) #inverte a imagem

    # Cria a imagem final
    res1 = cv2.bitwise_and(background, background, mask = mask1) 
    res2 = cv2.bitwise_and(img, img, mask = mask2) 
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 

    # Mostra a imagem final
    cv2.imshow("INVISIBLE Cloak", final_output) 
    k = cv2.waitKey(10) 
    if k == 27:  # Se a tecla 'esc' for pressionada, sai do loop
        break


