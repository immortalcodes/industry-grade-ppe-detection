import './HomePage.css';
import React, { useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const VideoFeed = ({ zoneId }) => {
  const videoRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const enableStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing the device camera", err);
      }
    };

    enableStream();

    // Cleanup function to stop the video stream
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Function to navigate to the zone page
  const goToZone = () => {
    navigate(`/zone/${zoneId}`);
  };

  return (
    <div className="video-feed-wrapper" onClick={goToZone}>
      <video ref={videoRef} autoPlay playsInline muted />
      <p className="zone-label">Zone {zoneId}</p>
    </div>
  );
};

const HomePage = () => {
  const zones = [1, 2, 3, 4]; // List of zones

  return (
    <div className="homepage">
      <h1>PPE Detection System</h1>
      <div className="video-grid">
        {zones.map(zoneId => (
          <VideoFeed key={zoneId} zoneId={zoneId} />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
