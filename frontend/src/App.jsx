import { Activity, Database, Network, RefreshCw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { StatCard } from './components/StatCard.jsx';
import { getEvents, getProcesses, reconstructProcesses } from './services/api.js';

export function App() {
  const [events, setEvents] = useState([]);
  const [processes, setProcesses] = useState([]);
  const [loading, setLoading] = useState(false);

  async function loadDashboard() {
    setLoading(true);
    try {
      const [eventsData, processesData] = await Promise.all([getEvents(), getProcesses()]);
      setEvents(eventsData);
      setProcesses(processesData);
    } finally {
      setLoading(false);
    }
  }

  async function handleReconstruct() {
    setLoading(true);
    try {
      await reconstructProcesses();
      await loadDashboard();
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Adaptive Process Intelligence Engine</p>
          <h1>APIE</h1>
        </div>
        <button className="primary-button" onClick={handleReconstruct} disabled={loading} title="Reconstruir processos">
          <RefreshCw size={18} />
          Reconstruir
        </button>
      </header>

      <section className="stats-grid">
        <StatCard icon={Activity} label="Eventos capturados" value={events.length} />
        <StatCard icon={Network} label="Processos descobertos" value={processes.length} />
        <StatCard icon={Database} label="Fonte" value="PostgreSQL" />
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Eventos recentes</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Aplicacao</th>
                  <th>Atividade</th>
                  <th>Quando</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => (
                  <tr key={event.id}>
                    <td>{event.event_type}</td>
                    <td>{event.process_name || '-'}</td>
                    <td>{event.activity || event.window_title || '-'}</td>
                    <td>{new Date(event.occurred_at).toLocaleString('pt-BR')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="panel">
          <h2>Processos reconstruidos</h2>
          <div className="process-list">
            {processes.map((process) => (
              <article className="process-item" key={process.id}>
                <div>
                  <strong>{process.name}</strong>
                  <span>{process.steps.length} etapas</span>
                </div>
                <meter min="0" max="1" value={process.confidence_score} />
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
