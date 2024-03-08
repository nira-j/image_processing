# ////// niraj  //////
from __future__ import print_function
from pyzbar.pyzbar import ZBarSymbol
import pyzbar.pyzbar as pyzbar
import cv2
import sys
import os

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im,symbols=[ZBarSymbol.I25])
    return decodedObjects

def get_croped_barcode(img):
    grayInput = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold via Otsu:
    _, binaryImage = cv2.threshold(grayInput, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cannyImage = cv2.Canny(binaryImage, threshold1=120, threshold2=255, edges=1)
    contours, hierarchy = cv2.findContours(cannyImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    fp=[]
    sp=[]
    barc=[]
    for cnt in contours:
        x,y,w,h=cv2.boundingRect(cnt)
        if (x>30 and x < 230 and y > 130 and y < 490 and h < 279 and h > 265 and w > 90 and w < 110):
            area=cv2.contourArea(cnt)
            image=cv2.rectangle(img,(x,y),(x+w, y+h),(0,255,0),2)  
            barc=[y, y+h ,x+7, x+w-3]
        
        if (x>30 and x < 200 and y > 50 and y < 140):
            area=cv2.contourArea(cnt)
            if(area > 590 and area < 650):
                image=cv2.rectangle(img,(x,y),(x+w, y+h),(10,0,255),2)
                fp=[x,y]
                # cv2.imshow("image" ,image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            
        if (x > 440 and x < 650 and y > 60 and y < 150):
            area=cv2.contourArea(cnt)
            if(area > 570 and area < 650):
                image=cv2.rectangle(img,(x,y),(x+w, y+h),(10,0,255),2)
                sp=[x,y]
                # cv2.imshow("image" ,image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    return barc, sp, fp


if __name__=='__main__':  
    barcode='' 
    imgno = sys.argv[0]
    decodedObjects = []
    path = sys.argv[1:]
    path=path[0]
    
    # path="C://omr//rotated_images//rotated_images//307346.jpg"

    if(os.path.isfile(path)):
        try:
            image=cv2.imread(path)
            barc, sp, fp = get_croped_barcode(image.copy())
            # print(img, barc, sp, fp)

            if(len(barc) != 0):
                im=image[barc[0]:barc[1], barc[2]:barc[3]]
                
                # cv2.imshow("image" ,im)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                barcode_obj=decode(im)
                for obj in barcode_obj:
                    barcode = obj.data
                    print(barcode)


            if(len(sp) != 0 and barcode == ''):
                # for marks
                x=sp[0]-335
                y=sp[1]+90
                # x=sp[0]-523
                # y=sp[1]+92
                w=90
                h=270  
                im=image[y:y+h, x:x+w]

                # cv2.imshow("image" ,im)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                barcode_obj=decode(im)
                for obj in barcode_obj:
                    barcode = obj.data
                    print(barcode)
                   

            if(len(fp) != 0 and barcode == ''):
                x=fp[0]-23
                y=fp[1]+91
                w=90
                h=270 
                im=image[y:y+h, x:x+w]

                # cv2.imshow("image" ,im)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                barcode_obj=decode(im)
                for obj in barcode_obj:
                    barcode = obj.data
                    print(barcode)
                    
        except:
            print("")
