import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { FontControls } from './components/FontControls';
import { ErrorModal } from './components/ErrorModal';
import { apiStrategy } from './services/api';

const codingFonts = [
  'Courier New',
  'Consolas',
  'Fira Code',
  'Inconsolata',
  'JetBrains Mono',
  'Menlo',
  'Monaco',
  'Source Code Pro',
  'Ubuntu Mono',
];

const fontSizes = [
  '12px', '14px', '16px', '18px', '20px', '22px', '24px'
];

const defaultConfig = {
  image: "mcr.microsoft.com/devcontainers/typescript-node",
  customizations: {
    vscode: {
      extensions: ["streetsidesoftware.code-spell-checker"]
    }
  },
  forwardPorts: [3000],
  containerEnv: {
      MY_CONTAINER_VAR: "some-value-here",
      MY_CONTAINER_VAR2: "${localEnv:SOME_LOCAL_VAR}"
  },
  remoteEnv: {
      PATH: "${containerEnv:PATH}:/some/other/path",
      MY_REMOTE_VARIABLE: "some-other-value-here",
      MY_REMOTE_VARIABLE2: "${localEnv:SOME_LOCAL_VAR}"
  }
};

function App() {
  const [input, setInput] = useState(JSON.stringify(defaultConfig, null, 2));
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasResponse, setHasResponse] = useState(false);
  const [selectedFont, setSelectedFont] = useState('Courier New');
  const [selectedFontSize, setSelectedFontSize] = useState('12px');

  useEffect(() => {
    setOutput('');
    setHasResponse(false);
  }, [input]);

  useEffect(() => {
    let val = JSON.stringify(defaultConfig, null, 2);
    setInput(val);
    console.log(val);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-bs-theme', 'dark');
  }, []);

  const handleConvert = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await apiStrategy.convert(input);
      setOutput(data);
      setHasResponse(true);
    } catch (err) {
      setError(err); // Pass the entire error object
    }

    setLoading(false);
  };

  return (
    <main className="bg-dark text-light min-vh-100">
      <div className="container py-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1 className="text-light">Devcontainer to Gitpod Converter</h1>
          <a 
            href="https://github.com/leonj1/devcontainer-gitpod" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="btn btn-outline-light"
          >
            GitHub
          </a>
        </div>

        <FontControls
          selectedFont={selectedFont}
          selectedFontSize={selectedFontSize}
          onFontChange={(e) => setSelectedFont(e.target.value)}
          onFontSizeChange={(e) => setSelectedFontSize(e.target.value)}
          fonts={codingFonts}
          fontSizes={fontSizes}
        />

        <div className="row">
          <div className="col-md-6 mb-3">
            <h2 className="text-light">devcontainer.json</h2>
            <form onSubmit={handleConvert}>
              <textarea
                id="input"
                rows={30}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                required
                className="form-control bg-dark text-light mb-3"
                style={{
                  fontFamily: selectedFont,
                  fontSize: selectedFontSize,
                  height: 'calc(100vh - 300px)'
                }}
              />
              <button type="submit" disabled={loading} className="btn btn-primary">
                {loading ? 'Converting...' : 'Convert'}
              </button>
            </form>
          </div>

          {hasResponse && (
            <div className="col-md-6">
              <h2 className="text-light">Gitpod</h2>
              <pre
                className="bg-dark text-light p-3 rounded"
                style={{
                  fontFamily: selectedFont,
                  fontSize: selectedFontSize,
                  height: 'calc(100vh - 300px)',
                  overflowY: 'auto'
                }}
              >
                {output}
              </pre>
              <CopyToClipboard text={output}>
                <button className="btn btn-outline-light mt-2">
                  Copy to Clipboard
                </button>
              </CopyToClipboard>
            </div>
          )}
        </div>

        {error && (
          <ErrorModal
            show={!!error}
            error={error}
            onClose={() => setError(null)}
          />
        )}
      </div>
    </main>
  );
}

export default App;
