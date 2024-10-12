import React, { useState, useEffect } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';

function App() {
  document.body.classList.add('bg-dark', 'text-light');
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [hasResponse, setHasResponse] = useState(false);

  useEffect(() => {
    setOutput('');
    setHasResponse(false);
  }, [input]);

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
      <h1 className="text-light">Devcontainer to Gitpod Converter</h1>
      <div className="converter-container">
        <div className="input-container">
          <h2 className="text-light">devcontainer.json</h2>
          <form onSubmit={handleConvert}>
            <textarea
              id="input"
              rows={20}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              required
              className="bg-dark text-light"
            ></textarea>
            <div className="button-container">
              <button type="submit" disabled={loading} className="btn btn-primary">
                {loading ? 'Converting...' : 'Convert'}
              </button>
            </div>
          </form>
        </div>
        {hasResponse && (
          <div className="output-container">
            <h2 className="text-light">Gitpod</h2>
            <div className="output-wrapper">
              <pre className="bg-dark text-light">{output}</pre>
              <CopyToClipboard text={output}>
                <button className="btn btn-outline-light copy-button">
                  Copy to Clipboard
                </button>
              </CopyToClipboard>
            </div>
          </div>
        )}
      </div>
      {showModal && (
        <dialog open className="bg-dark text-light">
          <article>
            <header>
              <h3>Error</h3>
            </header>
            <p>{error}</p>
            <footer>
              <button onClick={() => setShowModal(false)} className="btn btn-secondary">Close</button>
            </footer>
          </article>
        </dialog>
      )}
    </main>
  );
}

export default App;
