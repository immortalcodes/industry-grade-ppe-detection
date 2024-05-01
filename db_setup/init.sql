-- Create the database
CREATE DATABASE IF NOT EXISTS ppe_detection;

-- Connect to the database
\c ppe_detection;

CREATE TABLE IF NOT EXISTS continous_track (
    id SERIAL PRIMARY KEY,
    feed_instance VARCHAR(100) NOT NULL,
    timestamp VARCHAR(100),
    position VARCHAR(100),
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS ppe_detection_results (
    id SERIAL PRIMARY KEY,
    deep_track_id INT REFERENCES continous_track(id),
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    helmet_detected BOOLEAN,
    vest_detected BOOLEAN,
);