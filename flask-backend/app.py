from flask import Flask, request
from flask_cors import CORS
import json
import base64
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()

    if data:

        bs64=data['data'].split(',')[1]
        print(data['name'])

        try:
            img = base64.b64decode(bs64); 
            npimg = np.fromstring(img, dtype=np.uint8); 
            frame = cv2.imdecode(npimg, 1)

            path="./harrcasscade.xml"
            face_cascade=cv2.CascadeClassifier(path)
            # class_id=0
            # face_section =np.zeros((100,100),dtype='uint8')
            # ret , frame = capture.read()
            # frame=data['data']
            # if ret == False:
            #     return "Camera not opened"
            gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
            faces = sorted(faces,key = lambda f:f[2]*f[3])
            # for face in faces[-1:]:
            #     x,y,w,h = face
            #     offset = 10
            #     face_section = gray_frame[y-offset:y+h+offset,x-offset:w+x+offset]
            #     face_section = cv2.resize(face_section,(100,100))
            #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),10)
            if(len(faces)==1):
                return 'Noice'
            elif(len(faces)>1):
                return 'Multiple faces detected'
            else:
                return 'Alert: No face detected' 
        except:
            return 'Error'
    # cv2.imshow("camera", frame)
    # capture.release()
    # cv2.destroyAllWindows()

	# data = request.get_json()
	# resp = 'Nobody'
	# directory = './stranger'
	# if data:
	# 	if os.path.exists(directory):
	# 		shutil.rmtree(directory)

	# 	if not os.path.exists(directory):
	# 		try:
	# 			os.mkdir(directory)
	# 			time.sleep(1)
	# 			result = data['data']
	# 			b = bytes(result, 'utf-8')
	# 			image = b[b.find(b'/9'):]
	# 			im = Image.open(io.BytesIO(base64.b64decode(image)))
	# 			im.save(directory+'/stranger.jpeg')

	# 			if rahul.recognize_faces() == 'Rahul':
	# 				resp = 'Rahul'
	# 			else:
	# 				resp = 'Nobody'
	# 		except:
	# 			pass
	# return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)