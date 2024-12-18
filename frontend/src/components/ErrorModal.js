import React from 'react';

export function ErrorModal({ error, onClose }) {
  if (!error) return null;

  return (
    <div className="modal d-block" tabIndex="-1" role="dialog">
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header bg-danger text-white">
            <h5 className="modal-title">
              <i className="bi bi-exclamation-triangle-fill me-2"></i>
              Error {error.status && `(${error.status})`}
            </h5>
            <button 
              type="button" 
              className="btn-close btn-close-white" 
              onClick={onClose} 
              aria-label="Close"
            />
          </div>
          <div className="modal-body">
            <div className="d-flex align-items-center mb-3">
              <i className="bi bi-x-circle-fill text-danger fs-1 me-3"></i>
              <div>
                <h6 className="mb-1">Error Message:</h6>
                <p className="mb-0">{error.message}</p>
              </div>
            </div>
            {error.details && (
              <div className="mt-3">
                <h6>Details:</h6>
                <pre className="bg-light p-2 rounded">
                  {JSON.stringify(error.details, null, 2)}
                </pre>
              </div>
            )}
          </div>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-primary" 
              onClick={onClose}
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
