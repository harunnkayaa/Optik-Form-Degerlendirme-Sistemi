import cv2
import numpy as np
## TÜM GÖRÜNTÜLERİ TEK BİR PENCEREDE YIĞMAK İÇİN
def stackImages(imgArray, scale, labels=[]):
    rows = len(imgArray)  # Görüntü dizisinin satır sayısı
    cols = len(imgArray[0])  # Görüntü dizisinin sütun sayısı
    rowsAvailable = isinstance(imgArray[0], list)  # Satırların mevcut olup olmadığını kontrol eder
    width = imgArray[0][0].shape[1]  # İlk görüntünün genişliği
    height = imgArray[0][0].shape[0]  # İlk görüntünün yüksekliği
    
    if rowsAvailable:  # Eğer satırlar mevcutsa
        for x in range(0, rows):  # Satırlar üzerinde döngü
            for y in range(0, cols):  # Sütunlar üzerinde döngü
                # Ölçek parametresine göre her bir görüntüyü yeniden boyutlandır
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                # Eğer görüntü gri tonlamalıysa BGR (3 kanallı) formatına dönüştür
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)  # Boş bir görüntü oluştur
        hor = [imageBlank] * rows  # Yatay birleştirme için liste
        hor_con = [imageBlank] * rows  # Yatay birleştirme için başka bir liste
        for x in range(0, rows):  # Görüntüleri yatay olarak birleştir
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)  # Satırları dikey olarak birleştir
        ver_con = np.concatenate(hor)  # Satırları dikey olarak birleştir (concatenate)
    else:
        for x in range(0, rows):  # Tek satır, iç içe liste yok
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:  # Gri tonlamalı ise BGR'ye dönüştür
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)  # Yatay birleştir
        hor_con = np.concatenate(imgArray)  # Yatay birleştir (concatenate)
        ver = hor  # Sadece bir satır var

    # Etiketleri eklemek için etiket listesi boş değilse
    if len(labels) != 0:
        eachImgWidth = int(ver.shape[1] / cols)  # Her bir görüntünün genişliği
        eachImgHeight = int(ver.shape[0] / rows)  # Her bir görüntünün yüksekliği
        for d in range(0, rows):
            for c in range(0, cols):
                # Etiketler için dikdörtgen çiz
                cv2.rectangle(ver, (c * eachImgWidth, eachImgHeight * d), 
                              (c * eachImgWidth + len(labels[d][c]) * 13 + 27, 30 
                               + eachImgHeight * d), 
                              (255, 255, 255), cv2.FILLED)
                # Metin etiketini yerleştir
                cv2.putText(ver, labels[d][c], (eachImgWidth * c + 10, 
                                                eachImgHeight * d + 20), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver  # Sonuç olarak birleştirilmiş gör


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    print(add)
    print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)# biggest olandan başlamak için reverse true yaptıı doğru mu?
    #print(len(rectCon))
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitBoxes(img):
    rows = np.vsplit(img,5)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,5)
        for box in cols:
            boxes.append(box)
    return boxes

def drawGrid(img,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

def showAnswers(img,myIndex,grading,ans,questions=5,choices=5):
     secW = int(img.shape[1]/questions)
     secH = int(img.shape[0]/choices)
     for x in range(0,questions):
         myAns= myIndex[x]
         cX = (myAns * secW) + secW // 2
         cY = (x * secH) + secH // 2
         if grading[x]==1:
            myColor = (0,255,0)
            #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
            cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
         else:
            myColor = (0,0,255)
            #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
            cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)
            # CORRECT ANSWER
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
            20,myColor,cv2.FILLED)




