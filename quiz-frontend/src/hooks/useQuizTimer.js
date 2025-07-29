// src/hooks/useQuizTimer.js
import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for managing a countdown timer.
 * @param {number} initialDuration - The starting duration of the timer in seconds.
 * @param {boolean} [startImmediately=true] - Whether the timer should start counting down right away.
 * @param {function} [onTimeUp] - Callback function to execute when the timer reaches 0.
 * @returns {object} An object containing:
 * - timeLeft: Current time remaining in seconds.
 * - formattedTime: Time remaining formatted as MM:SS.
 * - isRunning: Boolean indicating if the timer is currently running.
 * - startTimer: Function to start or resume the timer.
 * - pauseTimer: Function to pause the timer.
 * - resetTimer: Function to reset the timer to initial duration.
 */
export const useQuizTimer = (initialDuration, startImmediately = true, onTimeUp) => {
  const [timeLeft, setTimeLeft] = useState(initialDuration);
  const [isRunning, setIsRunning] = useState(startImmediately);
  const timerRef = useRef(null); // Ref to hold the interval ID
  const endTimeRef = useRef(0); // Ref to store the exact time when the timer should end

  // Calculate endTime when duration changes or timer starts
  useEffect(() => {
    if (isRunning && initialDuration > 0) {
      endTimeRef.current = Date.now() + timeLeft * 1000;
    }
  }, [isRunning, initialDuration, timeLeft]);


  useEffect(() => {
    if (!isRunning) {
      clearInterval(timerRef.current);
      return;
    }

    if (timeLeft <= 0) {
      clearInterval(timerRef.current);
      setIsRunning(false);
      onTimeUp && onTimeUp();
      return;
    }

    // Use a more robust interval that accounts for drift
    const tick = () => {
      const remaining = Math.max(0, Math.round((endTimeRef.current - Date.now()) / 1000));
      setTimeLeft(remaining);

      if (remaining <= 0) {
        clearInterval(timerRef.current);
        setIsRunning(false);
        onTimeUp && onTimeUp();
      }
    };

    timerRef.current = setInterval(tick, 1000); // Check every second

    return () => clearInterval(timerRef.current); // Cleanup on unmount or re-render
  }, [timeLeft, isRunning, onTimeUp]); // Removed initialDuration from deps

  // --- Timer controls ---
  const startTimer = useCallback(() => {
    if (!isRunning && timeLeft > 0) {
      endTimeRef.current = Date.now() + timeLeft * 1000; // Reset end time on start/resume
      setIsRunning(true);
    }
  }, [isRunning, timeLeft]);

  const pauseTimer = useCallback(() => {
    setIsRunning(false);
  }, []);

  const resetTimer = useCallback(() => {
    clearInterval(timerRef.current);
    setTimeLeft(initialDuration);
    setIsRunning(startImmediately);
    if (startImmediately) { // If resetting to start, immediately set end time
        endTimeRef.current = Date.now() + initialDuration * 1000;
    }
  }, [initialDuration, startImmediately]);

  // Format time for display (MM:SS)
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const pad = (num) => String(num).padStart(2, '0');
    return `${pad(minutes)}:${pad(remainingSeconds)}`;
  };

  return {
    timeLeft,
    formattedTime: formatTime(timeLeft),
    isRunning,
    startTimer,
    pauseTimer,
    resetTimer,
  };
};