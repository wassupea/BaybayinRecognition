#from keras.models import load_model
from operator import itemgetter
from unittest import main
import cv2
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import collections
from fuzzywuzzy import process, fuzz
import itertools 

#model = load_model('./model/final_baybayin_model.h5') 



def preprocess(img):
    print ('-------RUNNING PREPROCESSING -------')
    #gaussian blur the image  --- used for noise removal of the image
    blur = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

    #convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    image_blurred = cv2.GaussianBlur(gray, (9, 9), 0)
  

    image_blurred_d = cv2.dilate(image_blurred, None)
  

    #create a binary threshold image
    ret, binary = cv2.threshold(image_blurred_d, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion = cv2.erode(binary, kernel, iterations = 1)
   

    kernel1 = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(erosion, kernel1, iterations = 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion1 = cv2.erode(dilation, kernel, iterations = 5)
    return erosion1

def lpreprocess(img):
    print ('-------RUNNING PREPROCESSING -------')
    #gaussian blur the image  --- used for noise removal of the image
    blur = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

    #convert image to grayscale
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    image_blurred = cv2.GaussianBlur(gray, (9, 9), 0)
  

    image_blurred_d = cv2.dilate(image_blurred, None)
  

    #create a binary threshold image
    ret, binary = cv2.threshold(image_blurred_d, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion = cv2.erode(binary, kernel, iterations = 1)
   

    kernel1 = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(erosion, kernel1, iterations = 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion1 = cv2.erode(dilation, kernel, iterations = 5)
    return erosion1



def x_cord_contour(contours):
    #Returns the X cordinate for the contour centroid
    M = cv2.moments(contours)
    return (int(M['m10']/M['m00']))
    
def y_cord_contour(contours):
    #Returns the Y cordinate for the contour centroid
    M = cv2.moments(contours)
    return (int(M['m01']/M['m00']))
    
def ret_x_cord_contour(contours):
    if cv2.contourArea(contours) > 5:
        cent_moment = cv2.moments(contours)
        return(int(cent_moment['m10']/cent_moment['m00']))
    else:
        pass




def qualifier_process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return binary


def segment(img):
    preprocessed = preprocess(img)
    upper = cv2.imread('./upper.png')
    lower = cv2.imread('./lower.png')

    ugray = lpreprocess(upper)
    lgray =  lpreprocess(lower)

    final_predict=[]
    output=""
    segmented =[]

  
    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ucontours, hierarchy = cv2.findContours(ugray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    lcontours, hierarchy = cv2.findContours(lgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_left_2_right = sorted(contours,key = x_cord_contour,reverse=False)
    usort = sorted(ucontours,key = x_cord_contour,reverse=False)
    lsort = sorted(lcontours,key = x_cord_contour,reverse=False)
    count =0
    lX=[]
    uX=[]


    upper_qualifier = []
    lower_qualifier = []
    joined = []
    #lX,uX,cX =0


    
    for (i,c) in enumerate(contours_left_2_right):
        x, y, w, h = cv2.boundingRect(c)
        cropped_contour=img[y:y + h, x:x + w]
        count+=1
        print(x,y)
        M = cv2.moments(c)
        cX = [M["m10"] / M["m00"]]
        cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)
        
        resize_contour = cv2.resize(cropped_contour, (64, 64), interpolation=cv2.INTER_AREA)
        resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
        main_predict = [1,6,13]
        for c in main_predict:
            joined.append(c)  
        cv2.imshow('segment no:'+str(i),cropped_contour)



        for (ui,uc) in enumerate(usort):

            x, y, w, h = cv2.boundingRect(uc)
            upper_contour=upper[y:y + h, x:x + w]
            UM = cv2.moments(uc)
            uX = [UM["m10"] / UM["m00"]]
            print(uX)
            #joined.append(uX)
                
            cv2.rectangle(upper,(x,y),( x + w, y + h ),(90,0,255),2)
            resize_contour = cv2.resize(upper_contour, (64, 64), interpolation=cv2.INTER_AREA)
            resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
            cv2.imshow('lower no:'+str(i),upper_contour)
            upper_predict = [21,21,21]
            for x1 in upper_predict:
                joined.append(x1)  
            
            joined.append(upper_predict)
            

        for (i,lc) in enumerate(lsort):
            x, y, w, h = cv2.boundingRect(lc)
            lower_contour=lower[y:y + h, x:x + w]
            UL = cv2.moments(lc)
            lX = [UL["m10"] / UL["m00"]]
            print(lX)
            #joined.append(lX)

            cv2.rectangle(lower,(x,y),( x + w, y + h ),(90,0,255),2)
            resize_contour = cv2.resize(lower_contour, (64, 64), interpolation=cv2.INTER_AREA)
            resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
            lower_predict = [19]
            joined.append(lower_predict)

   

    print(final_predict)
            



   

        

    print("joined",joined)
 



        
    
    


    




    print('Number of probable words', count)

 


   


def recognition(img):
    final_predict=[]
    for baybayin_char in final_predict:
        if baybayin_char==0:
            output+='a'
        elif baybayin_char==1:
                output+='b'
        elif baybayin_char==2:
            output+= 'ba'
        elif baybayin_char==3:
            output+= 'be'
        elif baybayin_char==4:
            output+= 'bo'
        elif baybayin_char==5:
            output+='d'
        elif baybayin_char==6:
            output+='dara'
        elif baybayin_char==7:
            output+='de'
        elif baybayin_char==8:
            output+='do'
        elif baybayin_char==9:
            output+='ei'
        elif baybayin_char==10:
            output+='g'
        elif baybayin_char==11:
            output+='ga'
        elif baybayin_char==12:
            output+='ge'
        elif baybayin_char==13:
            output+='go'
        elif baybayin_char==14:
            output+='h' 
        elif baybayin_char==15:
            output+='ha'
        elif baybayin_char==16:
            output+='he' 
        elif baybayin_char==17:
                output+='ho' 
        elif baybayin_char==18:
            output+= 'k'
        elif baybayin_char==19:
            output+= 'ka'
        elif baybayin_char==20:
            output+= 'ke'
        elif baybayin_char==21:
            output+='ko'
        elif baybayin_char==22:
            output+='l'
        elif baybayin_char==23:
            output+='la'
        elif baybayin_char==24:
            output+='le'
        elif baybayin_char==25:
            output+='lo'
        elif baybayin_char==26:
            output+='m'
        elif baybayin_char==27:
            output+='ma'
        elif baybayin_char==28:
            output+='me'
        elif baybayin_char==29:
            output+='mo'
        elif baybayin_char==30:
            output+='n' 
        elif baybayin_char==31:
            output+='na'
        elif baybayin_char==32:
            output+='ne'
        elif baybayin_char==33:
                output+='ng'
        elif baybayin_char==34:
            output+='nga'
            output+= 'nge'
        elif baybayin_char==35:
             output+= 'nge'
           
        elif baybayin_char==36:
             output+= 'ngo'
           
        elif baybayin_char==37:
             output+= 'no'
            
        elif baybayin_char==38:
            output+='ou'
        elif baybayin_char==39:
            output+='p'
        elif baybayin_char==40:
            output+='pa'
        elif baybayin_char==41:
            output+='pi'
        elif baybayin_char==42:
            output+='po'
        elif baybayin_char==43:
            output+='r'
        elif baybayin_char==44:
            output+='ra'
        elif baybayin_char==45:
            output+='re'
        elif baybayin_char==46:
            output+='ro' 
        elif baybayin_char==47:
            output+='s'
        elif baybayin_char==48:
            output+='sa' 
        elif baybayin_char==49:
            output+='se' 
        elif baybayin_char==50:
            output+= 'so'
        elif baybayin_char==51:
            output+= 't'
        elif baybayin_char==52:
            output+= 'ta'
        elif baybayin_char==53:
            output+='te'
        elif baybayin_char==54:
            output+='to'
        elif baybayin_char==55:
            output+='w'
        elif baybayin_char==56:
            output+='wa'
        elif baybayin_char==57:
            output+='we'
        elif baybayin_char==58:
            output+='wo'
        elif baybayin_char==59:
            output+='y'
        elif baybayin_char==60:
            output+='ya'
        elif baybayin_char==61:
            output+='ye'
        elif baybayin_char==62:
            output+='yo' 
           
    return output