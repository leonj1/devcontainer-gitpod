import React, { useState } from 'react';
import { Container, Form, Button, Card, Spinner, Modal } from 'react-bootstrap';
import axios from 'axios';
import { YAMLViewer } from 'react-yaml';

function App() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);

  const handleConvert = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/convert', JSON.parse(input));
      setOutput(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
      setShowModal(true);
    }
    setLoading(false);
  };

  return (
    <Container className="mt-5">
      <h1 className="mb-4">Devcontainer to Gitpod Converter</h1>
      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Input devcontainer.json:</Form.Label>
          <Form.Control
            as="textarea"
            rows={10}
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" onClick={handleConvert} disabled={loading}>
          {loading ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />{' '}
              Converting...
            </>
          ) : (
            'Convert'
          )}
        </Button>
      </Form>
      {output && (
        <Card className="mt-4">
          <Card.Body>
            <Card.Title>Gitpod YAML:</Card.Title>
            <YAMLViewer yaml={output} />
          </Card.Body>
        </Card>
      )}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>{error}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

export default App;
