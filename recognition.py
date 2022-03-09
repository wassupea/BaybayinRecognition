
import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

model = load_model('./baybayin_model1.h5') 

def preprocess_segment(img):
    print ('-------RUNNING BAYBAYIN_GUI.py -------')

    image = cv2.imread('./written_chars/sulat.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #ImageGrab.grab().crop((x,y,x1,y1)).save(image_name)

    baybayin_chars = []
    segmented = []
    

    #create a binary threshold image

    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)



    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # draw all contours
    with_contours = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
    
   
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
    
        cv2.rectangle(with_contours,(x,y), (x+w,y+h), (0,255,0), 1)
        cropped_contour=with_contours[y:y + h, x:x + w]

        resize_contour = cv2.resize(cropped_contour, (64, 64), interpolation=cv2.INTER_AREA)
        
        resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_BGR2GRAY)
  
        img_reshape = resize_contour.reshape(1,64,64,1)
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
                output ='ha'
            elif baybayin_char==6:
                output ='ka'
            elif baybayin_char==7:
                output ='kuw'
            elif baybayin_char==8:
                output ='la'
            elif baybayin_char==9:
                output ='ma'
            elif baybayin_char==10:
                output ='na'
            elif baybayin_char==11:
                output ='nga'
            elif baybayin_char==12:
                output ='o/u'
            elif baybayin_char==13:
                output ='pa'
            elif baybayin_char==14:
                output='sa'
            elif baybayin_char==15:
                output='ta' 
            elif baybayin_char==16:
                output='tul'
            elif baybayin_char==17:
                output='wa' # or i
            elif baybayin_char==18:
                output='ya' # or u
            print (output)

    return baybayin_chars