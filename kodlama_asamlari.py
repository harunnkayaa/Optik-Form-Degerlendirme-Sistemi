import cv2
#görüntü işleme için gerekli

import numpy as np
#########################
path="1.jpg"
wiheightImg = 700
widthImg  = 700 #foto büyüklüklerini ayarlama
########################
img = cv2.imread(path)#image pathini aldık ve  ve daha sonrasında imagei readle okuyup ekranda show olmasını sağladık  

cv2.imshow("Original",img)
cv2.waitKey(0)