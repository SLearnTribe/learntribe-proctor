from flask import Flask, request
from flask_cors import CORS
import json
import base64
import cv2
import numpy as np
import consul
import uuid
import socket

app = Flask(__name__)
CORS(app, resources={r"/proc": {"origins": ["http://www.smilebat.xyz", "http://localhost:3000"]}})
consul_client = consul.Consul(host="38.242.132.44", port=8500)
service_id = f"proctoring_{str(uuid.uuid4())}"


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def register_service_with_consul(port):
    consul_client.agent.service.register(
        name="sb-proc",
        service_id=service_id,
        address="localhost/proc",
        port=port,
        check=consul.Check.http("localhost/health", port, "30s")
    )


def deregister_service_with_consul():
    consul_client.agent.service.deregister(service_id)


@app.route("/health", methods=['GET'])
def health_check():
    health_check_is_successful = True
    if health_check_is_successful:
        return {"status": "ok"}, 200
    else:
        return {"status": "not ok"}, 500


@app.route('/proc', methods=['POST'])
def api():
    image_list = request.get_json()['data']
    x, y, z = 0, 0, 0

    if image_list:
        # print(len(image_list))
        try:
            for image in image_list:
                bs64 = image.split(',')[1]
                img = base64.b64decode(bs64);
                npimg = np.fromstring(img, dtype=np.uint8);
                frame = cv2.imdecode(npimg, 1)

                path = "./harrcasscade.xml"
                face_cascade = cv2.CascadeClassifier(path)
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
                faces = sorted(faces, key=lambda f: f[2] * f[3])
                if len(faces) == 1:
                    # return 'Noice'
                    x += 1
                elif len(faces) > 1:
                    # return 'Multiple faces detected'
                    y += 1
                else:
                    # return 'Alert: No face detected'
                    z += 1
                if y > 3 or z > 3:
                    return 'Faulty User\n' + f'good={x}, many={y}, bad={z}'
            return f'good={x}, many={y}, bad={z}'

        except Exception as ex:
            return f'Error :{ex}'


if __name__ == '__main__':
    try:
        port = get_free_port()
        print(f"RJ : {port}")
        register_service_with_consul(port)
        app.run(port=port, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Exception : {e}")
    finally:
        deregister_service_with_consul()
