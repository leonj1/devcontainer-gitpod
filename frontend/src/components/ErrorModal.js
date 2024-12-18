import React from 'react';
import { Modal, Button } from 'react-bootstrap';

export function ErrorModal({ error, onClose }) {
  const formatErrorDetails = () => {
    if (!error) return null;

    // Handle JSON validation errors
    if (error.error === "Invalid JSON format") {
      return (
        <div>
          <div className="mb-3">
            <strong className="text-danger">
              <i className="bi bi-exclamation-triangle-fill me-2"></i>
              {error.error}
            </strong>
          </div>
          <div className="mb-3">
            <div><strong>Problem:</strong> {error.message}</div>
            <div><strong>Location:</strong> Line {error.line_number}, Column {error.column}</div>
          </div>
          {error.context && (
            <div className="mb-3">
              <strong>Context:</strong>
              <pre className="bg-light p-2 mt-1 mb-0 border rounded" style={{ whiteSpace: 'pre-wrap' }}>
                {error.context}
              </pre>
            </div>
          )}
        </div>
      );
    }

    // Handle other types of errors
    return (
      <div>
        <div className="mb-3">
          <strong className="text-danger">
            <i className="bi bi-x-circle-fill me-2"></i>
            Error {error.status && `(${error.status})`}
          </strong>
        </div>
        <div className="mb-3">
          <div><strong>Error Message:</strong> {error.message}</div>
        </div>
        {error.details && (
          <div className="mb-3">
            <strong>Details:</strong>
            <pre className="bg-light p-2 mt-1 mb-0 border rounded" style={{ whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(error.details, null, 2)}
            </pre>
          </div>
        )}
      </div>
    );
  };

  if (!error) return null;

  return (
    <Modal show={true} onHide={onClose} centered>
      <Modal.Header className="bg-danger text-white">
        <Modal.Title>
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          Error {error.status && `(${error.status})`}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {formatErrorDetails()}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={onClose}>OK</Button>
      </Modal.Footer>
    </Modal>
  );
}
