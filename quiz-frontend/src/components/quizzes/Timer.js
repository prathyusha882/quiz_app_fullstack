// src/components/quizzes/Timer.js
import React, { useState, useEffect, useRef } from 'react';
import './Timer.css';

/**
 * A countdown timer component.
 * @param {object} props - The component props.
 * @param {number} props.duration - The total duration of the timer in seconds.
 * @param {function} [props.onTimeUp] - Callback function when the timer reaches 0.
 * @param {boolean} [props.isRunning=true] - Controls whether the timer is running.
 */
const Timer = ({ duration, onTimeUp, isRunning = true }) => {
  const [timeLeft, setTimeLeft] = useState(duration);
  const timerId = useRef(null);

  useEffect(() => {
    if (!isRunning) {
      clearInterval(timerId.current);
      return;
    }

    if (timeLeft <= 0) {
      clearInterval(timerId.current);
      onTimeUp && onTimeUp();
      return;
    }

    timerId.current = setInterval(() => {
      setTimeLeft((prevTime) => prevTime - 1);
    }, 1000);

    return () => clearInterval(timerId.current);
  }, [timeLeft, onTimeUp, isRunning]);

  // Format time for display (MM:SS)
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const pad = (num) => String(num).padStart(2, '0');
    return `${pad(minutes)}:${pad(remainingSeconds)}`;
  };

  const timerClass = `timer-display ${timeLeft <= 60 && 'warning'} ${timeLeft <= 10 && 'critical'}`.trim();

  return (
    <div className={timerClass}>
      Time Left: <span className="time-value">{formatTime(timeLeft)}</span>
    </div>
  );
};

export default Timer;