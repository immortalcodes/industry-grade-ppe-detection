import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './ZonePage.css';

const videoSources = {
  1: '/Users/ankitsoni/Desktop/CSDProject/PPE application/src/reference.mov',
  2: 'src/reference.mov',
  3: 'src/reference.mov',
  4: '/Users/ankitsoni/Desktop/CSDProject/PPE application/src/A01_20240222113000.mp4'
};

const CameraFeed = ({ camId }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const videoElement = videoRef.current;
    if (videoElement) {
      videoElement.src = videoSources[camId];
      videoElement.load();
      videoElement.onerror = () => {
        console.error(`Error loading video from ${videoSources[camId]}`);
      };
    }
  }, [camId]);

  return (
    <video
      className="video"
      ref={videoRef}
      autoPlay
      loop
      playsInline
      muted
      controls
      onError={(e) => console.log('Error playing video:', e)}
    >
      Your browser does not support the video tag.
    </video>
  );
};


const ZonePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const cams = [1, 2, 3, 4]; // Assuming you have 4 camera feeds
  const [alerts, setAlerts] = useState([]);

  const goToCamera = (camId) => {
    navigate(`/zone/${id}/camera/${camId}`);
  };

  return (
    <div className="zone-page">
      <h1 className="zone-title">Zone {id}</h1>
      <div className="camera-container">
        <div className="camera-grid">
          {cams.map((camId) => (
            <div key={camId} className="camera-feed-container" onClick={() => goToCamera(camId)}>
              <CameraFeed camId={camId} />
              <label className="camera-label">Cam {camId}</label>
            </div>
          ))}
        </div>
        <div className="alert-box">
          <h2>Alert Box</h2>
          {alerts.map((alert, index) => (
            <p key={index}>{alert.message}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ZonePage;
