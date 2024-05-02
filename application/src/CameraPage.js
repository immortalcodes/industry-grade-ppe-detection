import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './CameraPage.css';

const CameraFeed = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const enableStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing the device camera", err);
      }
    };

    enableStream();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%', maxHeight: '100%' }} />;
};

const CameraPage = () => {
  const { zoneId, cameraId } = useParams();
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState([]); // Initialize with empty array or fetch from an API

  // Mock function to fetch alerts - replace with actual API call as needed
  useEffect(() => {
    // Fetch or subscribe to alerts here
    // Update state with fetched alerts
    const mockAlerts = [
      { message: 'No PPE detected' },
      // ... more alerts
    ];
    setAlerts(mockAlerts);
  }, []);

  return (
    <div className="camera-page">
      <h1 className="camera-title">Cam {cameraId} - Zone {zoneId}</h1>
      <div className="camera-container"> 
       <CameraFeed />
      </div>
      <div className="alert-container">
        <h2>Alert Box</h2>
        {alerts.map((alert, index) => (
          <div key={index} className="alert-message">
            {alert.message}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CameraPage;
