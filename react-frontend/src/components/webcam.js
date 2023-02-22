import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';

const WebcamCapture = () => {
  const webcamRef = React.useRef(null);
  const videoConstraints = {
    width: 200,
    height: 200,
    facingMode: 'user',
  };
  const [name, setName] = useState('Rahul');
  const [status, setStatus] = useState('Good');
  const [images, setImages] = useState([]);

  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImages(images.concat(imageSrc));
    console.log(images.length);
    if (images.length === 12) {
      console.log(images);
      axios
        .post('http://127.0.0.1:5000/api', { data: images, name: name })
        .then((res) => {
          console.log(res);
          setStatus(res.data);
          // console.log(res['data'])
        })
        .catch((error) => {
          console.log(`error = ${error}`);
        });
      setImages([]);
    }
  }, [webcamRef, images, name]);

  useEffect(() => {
    let interval = setInterval(() => {
      capture();
    }, 5000);
    return () => clearInterval(interval);
  }, [capture]);

  return (
    <div>
      <Webcam
        audio={false}
        height={200}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={200}
        videoConstraints={videoConstraints}
      />
      <div>{status}</div>
    </div>
  );
};

export default WebcamCapture;
