from keras.models import load_model
import cv2
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import collections


model = load_model('./model/100.h5') 



def preprocess(img):
    print ('-------RUNNING PREPROCESSING -------')
    #gaussian blur the image  --- used for noise removal of the image
    blur = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

    #convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #create a binary threshold image
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return binary

def segment(img):
    preprocessed = preprocess(img)
    print ('-------RUNNING SEGMENTATION -------')
    final_predict=[]
    output=""
    segmented =[]

  
    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

     # draw all contours
    with_contours = cv2.drawContours(preprocessed, contours, -1, (0, 255, 0), 1)
    #sorted_ctrs = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    
    sorted_ctrs = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img.shape[1] )
   
    area_sort = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    

    for i, ctr in enumerate(sorted_ctrs):
        x, y, w, h = cv2.boundingRect(ctr)
        cropped_contour=img[y:y + h, x:x + w]
        resize_contour = cv2.resize(cropped_contour, (64, 64), interpolation=cv2.INTER_AREA)
        resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
        img_reshape = resize_contour.reshape(1,64,64,1)
        img_reshape = img_reshape/255
        pred = model.predict([img_reshape])[0]
        final = np.argmax(pred)
        
        final_predict.append(final)  
        data = str(final) + ':' +str((max(pred))*100)+'%'
        acc = max(pred)
     
        print(data)
        

    print(final_predict)

    for baybayin_char in final_predict:
        if baybayin_char==0:
            output+='a'
        elif baybayin_char==1:
                output+=' ba'
        elif baybayin_char==2:
            output+= 'da/ra'
        elif baybayin_char==3:
            output+= 'e/i'
        elif baybayin_char==4:
            output+= 'ga'
        elif baybayin_char==5:
            output+=' ha'
        elif baybayin_char==6:
            output+=' ka'
        elif baybayin_char==7:
            output+=' la'
        elif baybayin_char==8:
            output+=' ma'
        elif baybayin_char==9:
            output+=' na'
        elif baybayin_char==10:
            output+=' nga'
        elif baybayin_char==11:
            output+=' o/u'
        elif baybayin_char==12:
            output+=' pa'
        elif baybayin_char==13:
            output+=' sa'
        elif baybayin_char==14:
            output+=' ta' 
        elif baybayin_char==15:
            output+=' wa' # or i
        elif baybayin_char==16:
            output+=' ya' # or u
           
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
                output ='a'
            elif baybayin_char==1:
                output ='ba'
            elif baybayin_char==2:
                output = 'da/ra'
            elif baybayin_char==3:
                output = 'e/i'
            elif baybayin_char==4:
                output = 'ga'
            elif baybayin_char==5:
                output =' ha'
            elif baybayin_char==6:
                output =' ka'
            elif baybayin_char==7:
                output =' la'
            elif baybayin_char==8:
                output =' ma'
            elif baybayin_char==9:
                output =' na'
            elif baybayin_char==10:
                output =' nga'
            elif baybayin_char==11:
                output =' o/u'
            elif baybayin_char==12:
                output =' pa'
            elif baybayin_char==13:
                output='sa'
            elif baybayin_char==14:
                output='ta' 
            elif baybayin_char==15:
                output=' wa' # or i
            elif baybayin_char==16:
                output=' ya' # or u