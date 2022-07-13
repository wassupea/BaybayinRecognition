#importing of necessary libraries
from cv2 import resize
from keras.models import load_model
import cv2
from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import collections
from thefuzz import process, fuzz

#loading the imported model
model = load_model('./model/baybayin_model2.h5')
qualifier_model = load_model('./model/qualifier-onlyx4848.h5')


#preprocessing of main character
def preprocess(img):
    print ('-------RUNNING PREPROCESSING -------')
    #gaussian blur the image  --- used for noise removal of the image
    blur = cv2.bilateralFilter(img,9,75,75)

    #convert image to grayscale
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
  

    #image_blurred_d = cv2.dilate(gray, None)
  
    #create a binary threshold image
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion = cv2.erode(binary, kernel, iterations = 1)
   

    kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    dilation = cv2.dilate(erosion, kernel1, iterations = 2)
   
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion1 = cv2.erode(dilation, kernel, iterations = 2)


    return erosion1

#preprocess of qualifiers
def qualifier_process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion = cv2.erode(binary, kernel, iterations = 1)
    kernel1 = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(erosion, kernel1, iterations = 1)
    return dilation

#getting the x position of every characters
def ret_x_cord_contour(contours):
    if cv2.contourArea(contours) > 10:
        cent_moment = cv2.moments(contours)
        return(int(cent_moment['m10']/cent_moment['m00']))
    else:
        pass

#detect each character
def segment(img):
    preprocessed = preprocess(img)
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

  
    # find the contours from the preprocessed image
    contours, hierarchy = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ucontours, hierarchy = cv2.findContours(ugray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    lcontours, hierarchy = cv2.findContours(lgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #sorting of characters
    contours_left_2_right = sorted(contours,key = ret_x_cord_contour,reverse=False)
    usort = sorted(ucontours,key = ret_x_cord_contour,reverse=False)
    lsort = sorted(lcontours,key = ret_x_cord_contour,reverse=False)

    
      

   
    #main character
    for (i,c) in enumerate(contours_left_2_right):
            x, y, w, h = cv2.boundingRect(c)
            cropped_contour=img[y:y + h, x:x + w]
     
            
            M = cv2.moments(c)
            #getting x position of every characters
            cX = int(M["m10"] / M["m00"])
            main_position.append(cX)
            cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)
            #resizing the characters
            resize_contour = cv2.resize(cropped_contour, (64,64), interpolation=cv2.INTER_AREA)
            resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_RGB2GRAY)

            #passing to the model feature extraction and classification
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

            if 5 in final_predict:
                ha_index = final_predict.index(5)
                print('ha: ',ha_index)
                after = ha_index+1
                before_p = ha_index-1
                print('before index', before_p)
                print('after index', after)
                before_neto = final_predict[before_p]
                print('before neto: ', before_neto)
                try:
                    if len(final_predict) > -1:
                        
                        after_char = final_predict[after]
                        before_neto = final_predict[before_p]
                        print('before neto: ', before_neto)
                        if after_char == 5:
                            final_predict.pop(ha_index)
                            print('napasok')
                            new_index = final_predict.index(5)
                            final_predict[new_index] = 3
                            
                        if after_char == 4:
                            final_predict.pop(ha_index)
                            new_index = final_predict.index(4)
                            final_predict[new_index] = 3
                            print('final5: ', final_predict)

                        if before_neto == 3:
                            print('nandito')
                            final_predict.pop(ha_index)
                            new_index = final_predict.index(3)
                            
                except:
                    pass
               
            joined.append(final_predict)
            data = str(final) + ':' +str((max(pred))*100)+'%'

    print("main_position",main_position)
    for (ui,uc) in enumerate(usort):
        x, y, w, h = cv2.boundingRect(uc)
        upper_contour=upper[y:y + h, x:x + w]
        
        #getting x position of every qualifiers
        UM = cv2.moments(uc)
        uX = int(UM["m10"] / UM["m00"])
        u_position.append(uX)
                        
        cv2.rectangle(upper,(x,y),( x + w, y + h ),(90,0,255),2)
           
        #resizing of qualifiers
        u_resize_contour = cv2.resize(upper_contour, (48,48), interpolation=cv2.INTER_AREA)
        u_resize_contour = cv2.cvtColor(u_resize_contour, cv2.COLOR_RGB2GRAY)
        u_img_reshape = u_resize_contour.reshape(1,48,48,1)
        u_img_reshape = u_img_reshape/255
        
        #passing the qualifiers to the model feature extraction and classification
        u_pred = qualifier_model.predict([u_img_reshape])[0]
        u_final = np.argmax(u_pred)
        valls = 18
        upper_predict.append(valls)
        joined.append(valls)
        print("upper",upper_predict)

    for (i,lc) in enumerate(lsort):
            
        x, y, w, h = cv2.boundingRect(lc)
        lower_contour=lower[y:y + h, x:x + w]
        #getting x position of every qualifiers
        UL = cv2.moments(lc)
        lX = int(UL["m10"] / UL["m00"])
        l_position.append(lX)
        cv2.rectangle(lower,(x,y),( x + w, y + h ),(90,0,255),2)
        
        #resizing of qualifiers
        l_resize_contour = cv2.resize(lower_contour, (48,48), interpolation=cv2.INTER_AREA)
        l_resize_contour = cv2.cvtColor(l_resize_contour, cv2.COLOR_RGB2GRAY)
        
        l_img_reshape = l_resize_contour.reshape(1,48,48,1)
        l_img_reshape = l_img_reshape/255
        
        #passing the qualifiers to the model for feature extraction and classification
        l_pred = qualifier_model.predict([l_img_reshape])[0]
        l_final = np.argmax(l_pred)

        #prediction equivalent
        if l_final == 0:
            print('cross')
            l_final = l_final+17

        if l_final == 1:
            l_final = l_final+18


        lower_predict.append(l_final)
        joined.append(l_final)
        print("lower",lower_predict)

    #combining main character, upper, and lower qualifier
    #and sort them based on their x position
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

    
    #Prediction equivalent
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
            output+='wa' 
        elif baybayin_char==16:
            output+='ya' 
        elif baybayin_char==17:
            output=output[:-1]
        elif baybayin_char==18:
            output=output[:-1] + "ei"
        elif baybayin_char==19:
            output=output[:-1] + "ou"
            

    return output
           
           



