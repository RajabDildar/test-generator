import { useState } from 'react'
import './App.css'

function App() {
  const [code, setCode] = useState('')
  const [useCase, setUseCase] = useState('')
  const [tests, setTests] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const generateTests = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('http://localhost:5000/api/generate-tests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, useCase }),
      })
      
      const data = await response.json()
      if (!response.ok) throw new Error(data.error)
      
      setTests(data.tests)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>AI Test Generator</h1>
      
      <div className="input-section">
        <h2>Code Input</h2>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your Python code here..."
          rows={10}
        />
      </div>

      <div className="input-section">
        <h2>Use Case Description</h2>
        <textarea
          value={useCase}
          onChange={(e) => setUseCase(e.target.value)}
          placeholder="Describe the intended functionality..."
          rows={5}
        />
      </div>

      <button 
        onClick={generateTests}
        disabled={loading || !code || !useCase}
      >
        {loading ? 'Generating...' : 'Generate Tests'}
      </button>

      {error && <div className="error">{error}</div>}

      {tests && (
        <div className="output-section">
          <h2>Generated Tests</h2>
          <pre>{tests}</pre>
        </div>
      )}
    </div>
  )
}

export default App
