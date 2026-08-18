import React, { useState, useEffect } from 'react';
import IngestionRunHistory from '../components/IngestionRunHistory';
import { api } from '../services/api';
import { Play, Activity, ShieldCheck, Database, Layers, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export default function IngestionPage() {
  const [selectedSource, setSelectedSource] = useState('rss');
  const [customUrl, setCustomUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [error, setError] = useState(null);

  const [runs, setRuns] = useState([]);
  const [totalRuns, setTotalRuns] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [isLoadingRuns, setIsLoadingRuns] = useState(true);

  const loadRuns = async () => {
    setIsLoadingRuns(true);
    try {
      const data = await api.getIngestionRuns(page, limit);
      setRuns(data.runs || []);
      setTotalRuns(data.total || 0);
    } catch (err) {
      console.error('Failed to load ingestion runs:', err);
    } finally {
      setIsLoadingRuns(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, [page]);

  const handleTriggerIngestion = async () => {
    setIsProcessing(true);
    setError(null);
    setLastResult(null);

    try {
      const result = await api.triggerIngestion(selectedSource, customUrl || null);
      setLastResult(result);
      loadRuns();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to trigger ingestion pipeline.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="glass-card p-6 border-blue-500/30 bg-gradient-to-r from-slate-900 via-blue-950/20 to-slate-900 relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <Activity className="w-5 h-5 text-blue-400" />
              <h2 className="text-xl font-bold text-white tracking-tight">ETL Data Ingestion Pipeline</h2>
            </div>
            <p className="text-sm text-slate-300 max-w-2xl">
              Execute standardized, resilient data ingestion from permitted public job boards or test sandbox modes. Every run normalizes fields, validates Pydantic schemas, and suppresses duplicate listings.
            </p>
          </div>
          <div className="flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <ShieldCheck className="w-4 h-4" />
            <span>Permitted & Compliant</span>
          </div>
        </div>
      </div>

      {/* Trigger Control Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Control Inputs */}
        <div className="lg:col-span-2 glass-card p-6 space-y-5">
          <h3 className="font-bold text-lg text-white border-b border-slate-800 pb-3 flex items-center">
            <Layers className="w-5 h-5 mr-2 text-blue-400" /> Select Data Source Adapter
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* RSS Source */}
            <label className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
              selectedSource === 'rss' ? 'bg-blue-600/10 border-blue-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-white">Public Job RSS Feed</span>
                <input
                  type="radio"
                  name="source"
                  value="rss"
                  checked={selectedSource === 'rss'}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="accent-blue-500"
                />
              </div>
              <p className="text-xs text-slate-400">Fetches live job listings from WeWorkRemotely RSS feed.</p>
            </label>

            {/* REST API Source */}
            <label className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
              selectedSource === 'api' ? 'bg-blue-600/10 border-blue-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-white">Public REST API</span>
                <input
                  type="radio"
                  name="source"
                  value="api"
                  checked={selectedSource === 'api'}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="accent-blue-500"
                />
              </div>
              <p className="text-xs text-slate-400">Consumes Arbeitnow public JSON job board API.</p>
            </label>

            {/* Mock Clean */}
            <label className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
              selectedSource === 'mock' ? 'bg-blue-600/10 border-blue-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-white">Sandbox Mock (Standard)</span>
                <input
                  type="radio"
                  name="source"
                  value="mock"
                  checked={selectedSource === 'mock'}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="accent-blue-500"
                />
              </div>
              <p className="text-xs text-slate-400">Clean deterministic batch for instant testing.</p>
            </label>

            {/* Mock Chaos Duplicates */}
            <label className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
              selectedSource === 'mock_duplicates' ? 'bg-blue-600/10 border-blue-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-white">Sandbox Chaos (Duplicates)</span>
                <input
                  type="radio"
                  name="source"
                  value="mock_duplicates"
                  checked={selectedSource === 'mock_duplicates'}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="accent-blue-500"
                />
              </div>
              <p className="text-xs text-slate-400">Tests SHA-256 fingerprint deduplication.</p>
            </label>
          </div>

          {/* Optional Custom Feed URL */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Custom Feed / Endpoint URL (Optional)
            </label>
            <input
              type="text"
              placeholder="https://example.com/feed.rss"
              value={customUrl}
              onChange={(e) => setCustomUrl(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          {/* Trigger Button */}
          <div className="pt-2">
            <button
              onClick={handleTriggerIngestion}
              disabled={isProcessing}
              className="w-full flex items-center justify-center space-x-2 py-3 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  <span>Executing Pipeline (Fetch → Validate → Deduplicate → Store)...</span>
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 fill-current" />
                  <span>Trigger Ingestion Pipeline</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right 1 Col: Live Execution Result */}
        <div className="glass-card p-6 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-lg text-white border-b border-slate-800 pb-3 mb-4 flex items-center">
              <Database className="w-5 h-5 mr-2 text-emerald-400" /> Pipeline Execution Metrics
            </h3>

            {isProcessing ? (
              <div className="space-y-4 py-6 text-center">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                <div className="space-y-1">
                  <p className="text-sm font-semibold text-white">Running ETL Stages...</p>
                  <p className="text-xs text-slate-400">Fetching, Normalizing, Validating Pydantic schemas, Deduplicating hashes</p>
                </div>
              </div>
            ) : lastResult ? (
              <div className="space-y-4 animate-fade-in">
                <div className="flex items-center justify-between p-3 bg-slate-950/80 rounded-xl border border-slate-800">
                  <span className="text-xs text-slate-400">Status</span>
                  <span className="font-bold text-sm text-emerald-400 capitalize">{lastResult.status}</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-center">
                  <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800">
                    <div className="text-xl font-extrabold text-white">{lastResult.records_fetched}</div>
                    <div className="text-[10px] text-slate-400 uppercase">Fetched</div>
                  </div>
                  <div className="p-3 bg-emerald-950/40 rounded-lg border border-emerald-800/40">
                    <div className="text-xl font-extrabold text-emerald-400">{lastResult.records_inserted}</div>
                    <div className="text-[10px] text-emerald-300 uppercase">Inserted</div>
                  </div>
                  <div className="p-3 bg-amber-950/40 rounded-lg border border-amber-800/40">
                    <div className="text-xl font-extrabold text-amber-400">{lastResult.records_skipped}</div>
                    <div className="text-[10px] text-amber-300 uppercase">Dupes Skipped</div>
                  </div>
                  <div className="p-3 bg-rose-950/40 rounded-lg border border-rose-800/40">
                    <div className="text-xl font-extrabold text-rose-400">{lastResult.records_failed}</div>
                    <div className="text-[10px] text-rose-300 uppercase">Invalid Skipped</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-slate-500 text-xs">
                Select a data source adapter and click 'Trigger Ingestion Pipeline' to run a live ingestion pass.
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 p-3 bg-rose-950/40 border border-rose-800 text-rose-300 text-xs rounded-lg flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}
        </div>
      </div>

      {/* Ingestion Run Audit Table */}
      <IngestionRunHistory
        runs={runs}
        total={totalRuns}
        page={page}
        limit={limit}
        onPageChange={setPage}
      />
    </div>
  );
}
