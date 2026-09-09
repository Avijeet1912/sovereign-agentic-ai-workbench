import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="logo-mark">SA</div>
        <div>
          <h1>Sovereign Agentic AI Workbench</h1>
          <p>Local industrial intelligence - Phase 1 skeleton</p>
        </div>
      </header>

      <main className="app-main">
        <div className="hero-card">
          <div className="hero-badge">MVP PROTOTYPE</div>
          <h2>Ready for Phase 1</h2>
          <p>
            The backend API is running at <code>http://localhost:8000</code> and this
            React frontend is running at <code>http://localhost:5173</code>.
          </p>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-dot"></span>
              <span>Backend: <strong>running</strong></span>
            </div>
            <div className="status-item">
              <span className="status-dot"></span>
              <span>Frontend: <strong>running</strong></span>
            </div>
          </div>
          <div className="phase-note">
            <strong>Next phase:</strong> Phase 2 - SQLite database with synthetic industrial data
          </div>
        </div>
      </main>
    </div>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
