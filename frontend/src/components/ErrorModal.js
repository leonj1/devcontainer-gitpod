import React from 'react';

export function ErrorModal({ error, onClose }) {
  if (!error) return null;

  return (
    <div className="modal d-block" tabIndex="-1" role="dialog">
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Error</h5>
            <button 
              type="button" 
              className="btn-close" 
              onClick={onClose} 
              aria-label="Close"
            />
          </div>
          <div className="modal-body">
            <p>{error}</p>
          </div>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
