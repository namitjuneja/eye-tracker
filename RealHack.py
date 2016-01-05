import numpy as np
import cv2
from pykeyboard import PyKeyboard
 
 
if __name__ == '__main__':
    k = PyKeyboard()
    flag = 1
    
    cap = cv2.VideoCapture(0)                       #video record code
    facedata = "haarcascade_frontalface_default.xml" #process code
    eyedata = "haarcascade_eye.xml"
    cascade = cv2.CascadeClassifier(facedata)
    cascade2 = cv2.CascadeClassifier(eyedata)
    ret, frame = cap.read()
    ex1 = ex2 = ey1 = ey2 = ew1 = ew2 = eh1 = eh2 = 0
    
    while(ret):                                      #record code
        img = cv2.imread("123.jpg")
        img = frame
        print img.shape[:2]

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

            if len(eyes) != 0:
                ex1 = x + (w/2)
                ey1 = y + (h/2)

                # ex1 = eyes[0][0]
                # ey1 = eyes[0][1]
                # ew1 = eyes[0][2]
                # eh1 = eyes[0][3]

                if ex1-240>0:
                    k.tap_key('Right')
                    print "r"
                elif ex1-240<0:
                    k.tap_key('Left')
                    print "l"

                if ey1-320>0:
                    k.tap_key('Down')
                    print "d"
                elif ey1-320<0:
                    k.tap_key('Up')
                    print "u"

       
            # if len(eyes) != 0:
            #     if flag == 1:
            #         ex1 = eyes[0][0]
            #         ey1 = eyes[0][1]
            #         ew1 = eyes[0][2]
            #         eh1 = eyes[0][3]
            #         ex = ex1
            #         ey = ey1
            #         ew = ew1
            #         eh = eh1
            #         if ex1-ex2>0:
            #             k.tap_key('Right')
            #         elif ex1-ex2<0:
            #             k.tap_key('Left')

            #         if ey1-ey2>0:
            #             k.tap_key('Down')
            #         elif ey1-ey2<0:
            #             k.tap_key('Up')
            #         flag = 2
            #     else:
            #         ex2 = eyes[0][0]
            #         ey2 = eyes[0][1]
            #         ew2 = eyes[0][2]
            #         eh2 = eyes[0][3]
            #         ex = ex2
            #         ey = ey2
            #         ew = ew2
            #         eh = eh2
            #         flag = 1

               


        
        
        
                        
            
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
