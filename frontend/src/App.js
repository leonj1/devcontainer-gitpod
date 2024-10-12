import React, { useState, useEffect } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';

const codingFonts = [
  'Consolas',
  'Courier New',
  'Fira Code',
  'Inconsolata',
  'JetBrains Mono',
  'Menlo',
  'Monaco',
  'Source Code Pro',
  'Ubuntu Mono',
];

function App() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [hasResponse, setHasResponse] = useState(false);
  const [selectedFont, setSelectedFont] = useState('Consolas');

  useEffect(() => {
    setOutput('');
    setHasResponse(false);
  }, [input]);

  const handleFontChange = (e) => {
    setSelectedFont(e.target.value);
  };

  const handleConvert = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await fetch('https://devcontainer-api.joseserver.com/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: input,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.text();
      setOutput(data);
      setHasResponse(true);
    } catch (err) {
      setError(err.message || 'An error occurred');
      setShowModal(true);
    }
    setLoading(false);
  };

  return (
    <main className="container">
      <h1 className="text-light mb-4">Devcontainer to Gitpod Converter</h1>
      <div className="mb-3">
        <label htmlFor="font-select" className="form-label">Select Font: </label>
        <select
          id="font-select"
          value={selectedFont}
          onChange={handleFontChange}
          className="form-select bg-dark text-light"
        >
          {codingFonts.map((font) => (
            <option key={font} value={font}>
              {font}
            </option>
          ))}
        </select>
      </div>
      <div className="row">
        <div className="col-md-6 mb-3">
          <h2 className="text-light">devcontainer.json</h2>
          <form onSubmit={handleConvert}>
            <textarea
              id="input"
              rows={20}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              required
              className="form-control bg-dark text-light mb-3"
              style={{ fontFamily: selectedFont }}
            ></textarea>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Converting...' : 'Convert'}
            </button>
          </form>
        </div>
        {hasResponse && (
          <div className="col-md-6">
            <h2 className="text-light">Gitpod</h2>
            <pre className="bg-dark text-light p-3 rounded" style={{ fontFamily: selectedFont }}>{output}</pre>
            <CopyToClipboard text={output}>
              <button className="btn btn-outline-light mt-2">
                Copy to Clipboard
              </button>
            </CopyToClipboard>
          </div>
        )}
      </div>
      {showModal && (
        <div className="modal d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Error</h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)} aria-label="Close"></button>
              </div>
              <div className="modal-body">
                <p>{error}</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Close</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

export default App;
