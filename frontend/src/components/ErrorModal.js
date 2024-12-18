import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ErrorModal = ({ show, onClose, error }) => {
  const formatErrorMessage = (error) => {
    if (!error) return 'An unknown error occurred';
    
    if (typeof error === 'string') return error;
    
    let message = error.message || 'An unknown error occurred';
    
    // Format JSON validation errors with context
    if (error.error === 'Invalid JSON format' && error.context) {
      message = `${error.message}\n\nContext:\n${error.context}`;
    }
    
    return message;
  };

  return (
    <Modal show={show} onHide={onClose} className="dark-theme">
      <Modal.Header>
        <Modal.Title className="text-danger">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          Error
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <pre className="error-message mb-0">
          {formatErrorMessage(error)}
        </pre>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="outline-light" onClick={onClose}>
          OK
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ErrorModal;
