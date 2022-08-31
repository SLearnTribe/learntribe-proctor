import React, {useEffect, useState} from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';

const WebcamCapture = () => {
    const webcamRef = React.useRef(null);
    const videoConstraints = {
    width : 200,
    height : 200,
    facingMode: 'user'
    };
    const[name, setName] = useState('Rahul')
    const[status,setStatus]=useState('Good')

    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        // console.log(`imageSrc = ${imageSrc}`)
        axios.post('http://127.0.0.1:5000/api', {data : imageSrc,name : name})
            .then(res => {
                console.log(res)
                setStatus(res.data)
                // console.log(res['data'])
            })
            .catch(error => {
                console.log(`error = ${error}`)
        })
    },[webcamRef]);

    useEffect(()=>{
        let interval=setInterval(() => {
            capture()
        }, 1000);
        return () => clearInterval(interval);
    },[])
    
    return (
    <div>
    <Webcam
        audio = {false}
        height = {300}
        ref = {webcamRef}
        screenshotFormat = "image/jpeg"
        width = {350}
        videoConstraints = {videoConstraints}
    />
    <div>
        {status}
    </div>
    </div>
    );
};

export default WebcamCapture;