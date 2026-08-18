import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import IngestionPage from './pages/IngestionPage';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await api.getIngestionStatus();
        setSystemStatus(data);
      } catch (err) {
        console.error('Failed to fetch system status:', err);
      }
    };
    fetchStatus();
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        systemStatus={systemStatus}
      />

      <main className="flex-1">
        {activeTab === 'dashboard' ? (
          <Dashboard />
        ) : (
          <IngestionPage />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            <strong className="text-slate-400">JobFlow Ingestion Platform</strong> — Acdyon Technologies Frontend Challenge Part 1
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-slate-400">Permitted Public Sources</span>
            <span>•</span>
            <span className="text-slate-400">Pydantic & SHA-256 Deduplicated</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
