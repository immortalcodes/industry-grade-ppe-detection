// CameraFeed.js
import React, { useEffect, useRef } from 'react';

const CameraFeed = ({ camId }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const getVideoStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (error) {
        console.error('Error accessing camera stream:', error);
      }
    };

    getVideoStream();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return <video ref={videoRef} autoPlay playsInline muted />;
};
