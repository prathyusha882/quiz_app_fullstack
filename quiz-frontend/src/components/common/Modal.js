// src/components/common/Modal.js
import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import Button from './Button'; // Assuming Button component is in the same common folder
import './Modal.css';

/**
 * Reusable Modal component. Renders its content into a portal.
 * @param {object} props - The component props.
 * @param {boolean} props.isOpen - Controls the visibility of the modal.
 * @param {function} props.onClose - Function to call when the modal is closed.
 * @param {React.ReactNode} props.children - The content to be displayed inside the modal body.
 * @param {string} [props.title=''] - The title of the modal.
 */
const Modal = ({ isOpen, onClose, children, title = '' }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
      document.addEventListener('keydown', handleEscape);
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} ref={modalRef}>
        <div className="modal-header">
          {title && <h3 className="modal-title">{title}</h3>}
          <Button onClick={onClose} className="modal-close-button" variant="outline">
            &times;
          </Button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>,
    document.body // Append modal to the body
  );
};

export default Modal;