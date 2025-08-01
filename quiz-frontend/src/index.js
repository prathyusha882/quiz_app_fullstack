// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css'; // Import global styles
// If using Tailwind, you might also import './styles/tailwind.css';
import App from './App';

console.log('index.js: Application starting...');

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Web-vitals removed to prevent WebSocket connection errors in development