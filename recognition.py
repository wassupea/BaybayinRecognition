from cv2 import resize
from keras.models import load_model
import cv2
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import collections
from skimage.morphology import skeletonize
from thefuzz import process
model = load_model('./model/baybayin_model2.h5')
qualifier_model = load_model('./model/qualifier-only.h5')



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
    erosion1 = cv2.erode(dilation, kernel, iterations = 4)

    blur1 = cv2.medianBlur(erosion1, 3)
    img_copy = cv2.fastNlMeansDenoising(blur1)

    cv2.imshow('im', img_copy)

    return img_copy

def qualifier_process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return binary

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

    upper = cv2.imread('./upper.png')
    lower = cv2.imread('./lower.png')

    ugray = qualifier_process(upper)
    lgray =  qualifier_process(lower)
    print ('-------RUNNING SEGMENTATION -------')
    final_predict=[]
    output=""
    segmented =[]
    joined=[]
    upper_predict=[]
    lower_predict=[]
    joined_x=[]
    main_position=[]
    u_position=[]
    l_position=[]

  
    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ucontours, hierarchy = cv2.findContours(ugray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    lcontours, hierarchy = cv2.findContours(lgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_left_2_right = sorted(contours,key = ret_x_cord_contour,reverse=False)
    usort = sorted(ucontours,key = ret_x_cord_contour,reverse=False)
    lsort = sorted(lcontours,key = ret_x_cord_contour,reverse=False)

    #try:
        #contours_left_2_right = sorted(contours,key = ret_x_cord_contour,reverse=False)
    #except:
        #output='fixed drawing'
      

   

    for (i,c) in enumerate(contours_left_2_right):
            x, y, w, h = cv2.boundingRect(c)
            cropped_contour=img[y:y + h, x:x + w]
     
            
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            main_position.append(cX)
            cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)
            resize_contour = cv2.resize(cropped_contour, (64,64), interpolation=cv2.INTER_AREA)
            resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)
            cv2.imshow('main_contour', cropped_contour)
            img_reshape = resize_contour.reshape(1,64,64,1)
            img_reshape = img_reshape/255
            pred = model.predict([img_reshape])[0]
            
            
            final = np.argmax(pred)
          
            final_predict.append(final)
            if 8 in final_predict:
                ma_index = final_predict.index(8)
                before = ma_index-1
                
                print('before index', before)
                if before > -1:
                    before_char = final_predict[before]
                    print('before', before_char)
                    if before_char == 15:
                        print('popped')
                        final_predict.pop(before)
            joined.append(final_predict)
            data = str(final) + ':' +str((max(pred))*100)+'%'
            #acc = max(pred)
        
            #print(data)
    print("main_position",main_position)
    for (ui,uc) in enumerate(usort):

     
        x, y, w, h = cv2.boundingRect(uc)
        upper_contour=upper[y:y + h, x:x + w]
        cv2.imshow('upper_contour',upper_contour)
        UM = cv2.moments(uc)
        uX = int(UM["m10"] / UM["m00"])
        u_position.append(uX)
                        
        cv2.rectangle(upper,(x,y),( x + w, y + h ),(90,0,255),2)
           
            
        u_resize_contour = cv2.resize(upper_contour, (56,56), interpolation=cv2.INTER_AREA)
        u_resize_contour = cv2.cvtColor(u_resize_contour, cv2.COLOR_RGB2GRAY)
        u_img_reshape = u_resize_contour.reshape(1,56,56,1)
        u_img_reshape = u_img_reshape/255
        u_pred = qualifier_model.predict([u_img_reshape])[0]
        u_final = np.argmax(u_pred)
        valls = 18
        upper_predict.append(valls)
        joined.append(valls)
        print("upper",upper_predict)

    for (i,lc) in enumerate(lsort):
            
        x, y, w, h = cv2.boundingRect(lc)
        lower_contour=lower[y:y + h, x:x + w]
        
        UL = cv2.moments(lc)
        lX = int(UL["m10"] / UL["m00"])
        l_position.append(lX)
        cv2.rectangle(lower,(x,y),( x + w, y + h ),(90,0,255),2)
        
        l_resize_contour = cv2.resize(lower_contour, (56,56), interpolation=cv2.INTER_AREA)
        l_resize_contour = cv2.cvtColor(l_resize_contour, cv2.COLOR_RGB2GRAY)
        #cv2.imshow('lower', l_resize_contour)
        l_img_reshape = l_resize_contour.reshape(1,56,56,1)
        l_img_reshape = l_img_reshape/255
        l_pred = qualifier_model.predict([l_img_reshape])[0]
        l_final = np.argmax(l_pred)
        
        if l_final == 0:
            print('cross')
            l_final = l_final+17

        if l_final == 1:
            l_final = l_final+18

        lower_predict.append(l_final)
        joined.append(l_final)
        print("lower",lower_predict)

    main_joined = dict(zip(main_position, final_predict))
    upper_joined = dict(zip(u_position, upper_predict))
    lower_joined = dict(zip(l_position, lower_predict))
    merged ={}
    merged.update(main_joined)
    merged.update(upper_joined)
    merged.update(lower_joined)
    sorted_d={}
    sorted_d = dict(sorted(merged.items()))
    values=sorted_d.values()
    print(values)

    for baybayin_char in values:
        if baybayin_char==0:
            output+='a'
        elif baybayin_char==1:
                output+='ba'
        elif baybayin_char==2:
            output+= 'da'
        elif baybayin_char==3:
            output+= 'ei'
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
            output+='ou'
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
            output=output[:-1] + "ei"
        elif baybayin_char==19:
            output=output[:-1] + "ou"
            #output+='.'

    #a_file = open("tagalog_dict.txt", "r")

    #tagalog_words = []

    #for line in a_file:
        #stripped_line = line.strip()
        #line_list = stripped_line.split()
        #tagalog_words.append(line_list)

    #a_file.close()


    #highest=""

    #print(output)
    #Ratios = process.extract(output,tagalog_words)
    #print(Ratios)
    #highest = process.extractOne(output,tagalog_words)
    

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