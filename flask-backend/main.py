from time import sleep
import cv2
import numpy as np
import os 
from knn import KNN
import base64

capture = cv2.VideoCapture(0)
path="./harrcasscade.xml"
face_cascade=cv2.CascadeClassifier(path)
dirpath = "./data"
face_data=[]
labels=[]
names={}
class_id=0
face_section =np.zeros((100,100),dtype='uint8')

for file in os.listdir(dirpath):
    if file.endswith(".npy"):
        data_item = np.load(dirpath+'/'+file)
        names[class_id] = file[:-4]
        face_data.append(data_item)
        target = class_id * np.ones((data_item.shape[0],))
        class_id += 1
        labels.append(target)


face_dataset = np.concatenate(face_data,axis = 0)
face_labels = np.concatenate(labels,axis = 0).reshape((-1,1))
while True:
    ret , frame = capture.read()
    

    # print(frame)
    # sleep(5000)
    if ret == False:
        print("Camera not opened")
        continue
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
    faces = sorted(faces,key = lambda f:f[2]*f[3])
    for face in faces[-1:]:
        x,y,w,h = face
        
        offset = 10
        face_section = gray_frame[y-offset:y+h+offset,x-offset:w+x+offset]
        face_section = cv2.resize(face_section,(100,100))
        pred = KNN(face_dataset,face_labels,face_section.flatten(),3)
        pred_name = names[int(pred)]
        cv2.putText(frame,pred_name,(x,y-30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),10)
    if(len(faces)!=0):
        print('found ',class_id)
        class_id+=1    
    cv2.imshow("camera", frame)
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()