#  Program to align, misaligned omr sheet
# niraj
import cv2 
import imutils
import numpy as np
import math
import imutils
import os


def displayImage(image):
    image=cv2.resize(image, (500,700))
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_coordinate(image):  
    
    # Convert BGR to grayscale:
    grayInput = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold via Otsu:
#     _, binaryImage = cv2.threshold(grayInput, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, binaryImage = cv2.threshold(grayInput, 100, 255, cv2.THRESH_BINARY)
    
#     displayImage(binaryImage)
    gausimg=cv2.GaussianBlur(binaryImage, (3,3),cv2.BORDER_DEFAULT)
    # displayImage(gausimg)
    cannyImage = cv2.Canny(gausimg, threshold1=180, threshold2=255, edges=1)
    # displayImage(cannyImage)
    fp=[]
    sp=[]
    contours, hierarchy = cv2.findContours(cannyImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x,y,w,h=cv2.boundingRect(cnt)
        if (x>50 and x < 290 and y > 40 and y < 205):
            area=cv2.contourArea(cnt)
            if(area > 500 and area < 650):
                image=cv2.rectangle(image,(x,y),(x+w, y+h),(0,255,0),2)
                fp=[x,y]
                
                # displayImage(image)

        if (x > 430 and x < 650 and y > 40 and y < 250):
            area=cv2.contourArea(cnt)
            if(area > 500 and area < 650):
                image=cv2.rectangle(image,(x,y),(x+w, y+h),(0,255,0),2)
                sp=[x,y]

    return fp,sp

if __name__=='__main__': 
    
    #image source path assign to src
    src="" 
    #image destination path assign to dest
    dest=""
    lis=os.listdir(src)
    # print(lis)
    # lis=['500872.jpg']
    cropedimg=[]
    notcropedimg=[]
    rotated=''
    for img in lis:
        image=cv2.imread(src+img) 
        try:
            print(img)
            
#             displayImage(image)
            bimage=cv2.copyMakeBorder(image.copy() ,15,15,55,10,cv2.BORDER_CONSTANT,value=[255,255,255])
            
#             displayImage(bimage)

            fp,sp=get_coordinate(bimage.copy())
            print("before rotation:- ", fp, sp)
            angle = math.degrees(math.atan2(sp[1] - fp[1], sp[0] - fp[0]))
            print(angle)
           
            rotated=imutils.rotate(bimage,angle)
            
#             displayImage(rotated)
            
            fp,sp=get_coordinate(rotated.copy())
            print("after rotation:- ", fp, sp)
            first_point=[fp[0]-120,fp[1]-80] # marks
            # first_point=[fp[0]-50,fp[1]-80] # pd
            second_point=[fp[0]+720,fp[1]-80]

            print(first_point,second_point)
            print()
        
            croped = rotated[first_point[1]:first_point[1]+2135, first_point[0]:second_point[0]]
            cropedimg.append(img)
#             cv2.imwrite('rotated_images/'+img, rotated)
            cv2.imwrite(dest+img, croped)

        except:
            print("co-ordinate not found")
            cv2.imwrite(dest+img, image)
            notcropedimg.append(img)
            
    print("Total rotated and croped pd image:", len(cropedimg))
    print("Not rotated and croped pd image:", len(notcropedimg))
    print("Not rotated and croped pd image:", notcropedimg)