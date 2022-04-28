from cv2 import resize
from keras.models import load_model
import cv2
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import collections
from skimage.morphology import skeletonize
from thefuzz import process
model = load_model('./model/4qualifier.h5') 



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

def ret_x_cord_contour(contours):
    if cv2.contourArea(contours) > 10:
        cent_moment = cv2.moments(contours)
        return(int(cent_moment['m10']/cent_moment['m00']))
    else:
        pass

def segment(img):
    preprocessed = preprocess(img)
    img_copy = img.copy()
    img_copy = cv2.medianBlur(img_copy, 3)
    img_copy = cv2.fastNlMeansDenoising(img_copy)
    #cv2.imshow('copr', img_copy)
    print ('-------RUNNING SEGMENTATION -------')
    final_predict=[]
    output=""
    segmented =[]

  
    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        contours_left_2_right = sorted(contours,key = ret_x_cord_contour,reverse=False)
    except:
        output='fixed drawing'
    count=0

    for (i,c) in enumerate(contours_left_2_right):
            x, y, w, h = cv2.boundingRect(c)
            cropped_contour=img_copy[y:y + h, x:x + w]
            count+=1
            cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)
            resize_contour = cv2.resize(cropped_contour, (64,64), interpolation=cv2.INTER_AREA)
            resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
            cv2.imshow('sd', cropped_contour)
            img_reshape = resize_contour.reshape(1,64,64,1)
            img_reshape = img_reshape/255
            pred = model.predict([img_reshape])[0]
            final = np.argmax(pred)
            
            final_predict.append(final)  
            data = str(final) + ':' +str((max(pred))*100)+'%'
            acc = max(pred)
        
            print(data)
    
        
    last = len(final_predict)-1

    for baybayin_char in final_predict:
        if baybayin_char==0:
            output+='a'
        elif baybayin_char==1:
                output+='ba'
        elif baybayin_char==2:
            output+= 'da/ra'
        elif baybayin_char==3:
            output+= 'e/i'
        elif baybayin_char==4:
            output+= 'ga'
        elif baybayin_char==5:
            output+='ha'
        elif baybayin_char==6:
            output+='ka'
        elif baybayin_char==7:
            output+='la'
        elif baybayin_char==8:
            output+='ma'
        elif baybayin_char==9:
            output+='na'
        elif baybayin_char==10:
            output+='nga'
        elif baybayin_char==11:
            output+='o/u'
        elif baybayin_char==12:
            output+='pa'
        elif baybayin_char==13:
            output+='sa'
        elif baybayin_char==14:
            output+='ta' 
        elif baybayin_char==15:
            output+='wa' # or i
        elif baybayin_char==16:
            output+='ya' # or u
        elif baybayin_char==17:
            output=output[:-1]
        elif baybayin_char==18:
            output+='tuldok' # or u
           
    return output
    
           




def recognition(img):
    baybayin_chars = []
    output = ""
    #print(img)

 
    for i in img:
        #print(i.shape)
        img_reshape = i.reshape(1,64,64,1)
        img_reshape = img_reshape/255
        pred = model.predict([img_reshape])[0]
        final = np.argmax(pred)
        baybayin_chars.append(final)         



    for baybayin_char in baybayin_chars:
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
            output+='s'
        elif baybayin_char==44:
            output+='sa' 
        elif baybayin_char==45:
            output+='se' 
        elif baybayin_char==46:
            output+= 'so'
        elif baybayin_char==47:
            output+= 't'
        elif baybayin_char==48:
            output+= 'ta'
        elif baybayin_char==49:
            output+='te'
        elif baybayin_char==50:
            output+='to'
        elif baybayin_char==51:
            output+='w'
        elif baybayin_char==52:
            output+='wa'
        elif baybayin_char==53:
            output+='we'
        elif baybayin_char==54:
            output+='wo'
        elif baybayin_char==55:
            output+='y'
        elif baybayin_char==56:
            output+='ya'
        elif baybayin_char==57:
            output+='ye'
        elif baybayin_char==58:
            output+='yo' 