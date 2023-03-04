import json
import logging
from flask import Flask, request
from flask_cors import CORS
import base64
import cv2
import numpy as np
import consul
import uuid
import socket
# from controllers import procReportController
# from dataaccess.entity.procReport import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ['www.smilebat.xyz', 'http://localhost:3000'],
                             "methods": ['GET,PUT,POST,DELETE'],
                             "allow_headers": ['authorization', 'Content-Type'],
                             "vary_header": ['Access-Control-Request-Method',
                                             'Origin',
                                             'Access-Control-Request-Headers'],
                             }})

# Format : sql://username:password@uri/db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://keycloak:password@38.242.132.44:5432/inquisitve'
# db.init_app(app)
# ma.init_app(app)

consul_client = consul.Consul(host="consul", port=8500)
# consul_client = consul.Consul(host="www.smilebat.xyz", port=8500)
service_id = f"sb-proc-{str(uuid.uuid4())}"
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('sb-proc')


def get_free_port():
    logger.info("Evaluating free ports")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def register_service_with_consul(host, port):
    logger.info('Registering to Consul with Hostname : ' + host)
    try:
        consul_client.agent.service.register(
            name="sb-proc",
            service_id=service_id,
            port=port,
            address=host,
            tags=[],
            check=consul.Check.http(url=f'http://{host}:{port}/health',
                                    interval='30s',
                                    timeout='5s')
        )
    except ConnectionError:
        logger.error('Consul Host is down')


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
    good = int(request.get_json()['good'])
    many = int(request.get_json()['many'])
    bad = int(request.get_json()['bad'])
    temp_good, temp_many, temp_bad = 0, 0, 0

    if image_list:
        # print(len(image_list))
        size = len(image_list)
        try:
            for image in image_list:
                # TODO : Handle empty image
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
                    temp_good += 1
                elif len(faces) > 1:
                    # return 'Multiple faces detected'
                    temp_many += 1
                else:
                    # return 'Alert: No face detected'
                    temp_bad += 1
                # if y > size/3 or z >3:
                #     return 'Faulty User\n' + f'good={x}, many={y}, bad={z}'
            # return f'good={good}, many={many}, bad={bad}'
            logger.info(f'good={good}, many={many}, bad={bad}')
            good += temp_good
            many += temp_many
            bad += temp_bad
            message = ''
            if temp_many != 0:
                message = 'Multiple faces detected'
            elif temp_bad > 2:
                message = 'Look on the screen'
            return json.dumps({'good': good,
                               'many': many,
                               'bad': bad,
                               'message': message})

        except Exception as ex:
            return f'Error :{ex}'


# procReportController.register(app, route_base='/proc')


if __name__ == '__main__':
    try:
        host = socket.gethostname()
        port = get_free_port()
        # port=8153
        register_service_with_consul(host, port)
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    except Exception as e:
        logging.error(f"Exception : {e}")
    finally:
        deregister_service_with_consul()
