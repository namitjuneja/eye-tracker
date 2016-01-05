import numpy as np
import cv2
from pymouse import PyMouse

 
 
if __name__ == '__main__':
    m = PyMouse()
    
    cap = cv2.VideoCapture(0)                        #video record code
    facedata = "haarcascade_frontalface_default.xml" #process code
    eyedata = "haarcascade_eye.xml"
    cascade = cv2.CascadeClassifier(facedata)
    cascade2 = cv2.CascadeClassifier(eyedata)
    ret, frame = cap.read()
    
    while(ret):                                      #record code
        img = cv2.imread("123.jpg")
        img = frame

        minisize = (img.shape[1],img.shape[0])       #video code
        miniframe = cv2.resize(img, minisize)
 
        faces = cascade.detectMultiScale(miniframe)
        ex = ey = eh = ew = 0
        #print "faces_len, face[0]_len", type(faces), type(faces[0])
        
        for f in faces:
        
            x, y, w, h = [ v for v in f ]
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
 
            sub_face = img[y:y+h, x:x+w]
            cv2.imshow('sub_face',sub_face)
            cv2.waitKey(1)
            
            face_file_name = "faces/face_" + str(y) + ".jpg"
            
            sub_gray = cv2.cvtColor(sub_face, cv2.COLOR_BGR2GRAY)
            eyes = cascade2.detectMultiScale(sub_gray, minSize = (sub_face.shape[0]/6,sub_face.shape[0]/6))
            ael_x = ael_y = []
            
            for (ex, ey, ew, eh) in eyes:
                #cv2.rectangle(sub_gray, (ex,ey), ((ex+ew), (ey+eh)), (255, 0, 0))
                cv2.rectangle(img, ((x+ex),(y+ey)), ((x+ex+ew), (y+ey+eh)), (0,255,0))

                sub_eye = sub_gray[ey:ey+eh , ex:ex+ew]
                sub_eye_color = sub_face[ey:ey+eh , ex:ex+ew]
                #cv2.imshow("sub_eye_color", sub_eye_color)

                #PUPIL RENDERING CODE BEGINS

                sub_eye = 255 - sub_eye                                                             #INVERTING_COLOURS
                
                ret,sub_eye2 = cv2.threshold(sub_eye, 150, 255, cv2.THRESH_BINARY)                  #THRESHOLDING

                cv2.imshow('threshold',sub_eye2)
                cv2.waitKey(1)

                contours,heirarchy=cv2.findContours(sub_eye2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #FIND_CONTOURS
                #print "cont,hierch", contours, heirarchy
                
                cv2.drawContours(sub_eye2,contours,-1,(255,255,255),2)                              #FILLING_CONTOURS
                cv2.imshow('contour',sub_eye2)
                cv2.imshow('original',sub_eye_color)
                cv2.waitKey(1)
                

                #contours,hierarchy = cv2.findContours(sub_eye2, 1, 2)
                for i in contours:
                    area = cv2.contourArea(i)
                    #print "cONTOUR_AREA", area
                    rect=cv2.boundingRect(i)
                    #print "RECT_CO-ORDINATES", rect
                    radius = rect[2]/2
                    if (area>=10 and area <=40):# and abs(1-(rect[2]/rect[3]))<=0.2 and abs(1-(area/3.14159*(radius**2)))<=0.2):
                        cv2.circle(img,(x+ex+rect[0]+radius,y+ey+rect[1]+radius),radius,(255,0,0),2)
                        ael_x.append(x+ex+rect[0]+radius)
                        ael_y.append(y+ey+rect[1]+radius)

            if (len(ael_x) != 0 and len(ael_y) != 0):            
                mouse_x = sum(ael_x)/len(ael_x)
                mouse_y = sum(ael_y)/len(ael_y)
                m.move(mouse_x,mouse_y)
                print "mouse_x", mouse_x, "\tmouse_y", mouse_y
                        
            
        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        
    cap.release()
    cv2.destroyAllWindows()
    

    #while(True):
        #key = cv2.waitKey(20)
        #if key in [27, ord('Q'), ord('q')]:
            #break
