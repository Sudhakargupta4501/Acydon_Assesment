import React from 'react';
import { Activity, CheckCircle, AlertTriangle, XCircle, Clock, Database, Layers } from 'lucide-react';

export default function IngestionRunHistory({ runs, total, page, limit, onPageChange }) {
  const formatTime = (isoString) => {
    if (!isoString) return 'Running...';
    return new Date(isoString).toLocaleString();
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'success':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle className="w-3 h-3 mr-1" /> Success
          </span>
        );
      case 'partial_success':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-3 h-3 mr-1" /> Partial
          </span>
        );
      case 'failed':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <XCircle className="w-3 h-3 mr-1" /> Failed
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 animate-pulse">
            <Clock className="w-3 h-3 mr-1" /> Running...
          </span>
        );
    }
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div>
          <h3 className="font-bold text-lg text-white flex items-center">
            <Activity className="w-5 h-5 mr-2 text-blue-400" /> Ingestion Audit History
          </h3>
          <p className="text-xs text-slate-400">Complete execution history of data ingestion runs and performance metrics.</p>
        </div>
        <span className="text-xs text-slate-400">Total Runs: <strong className="text-white">{total}</strong></span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
            <tr>
              <th className="py-3 px-4">Run ID</th>
              <th className="py-3 px-4">Source</th>
              <th className="py-3 px-4">Started At</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-right">Fetched</th>
              <th className="py-3 px-4 text-right">Inserted</th>
              <th className="py-3 px-4 text-right">Skipped (Dupes)</th>
              <th className="py-3 px-4 text-right">Failed</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {runs.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-8 text-center text-slate-500">
                  No ingestion runs recorded yet. Click 'Run Ingestion' to start.
                </td>
              </tr>
            ) : (
              runs.map((run) => (
                <tr key={run.id} className="hover:bg-slate-900/60 transition-colors">
                  <td className="py-3 px-4 font-mono text-slate-400">{run.id.substring(0, 8)}...</td>
                  <td className="py-3 px-4 font-medium text-white">{run.source}</td>
                  <td className="py-3 px-4 text-slate-400">{formatTime(run.started_at)}</td>
                  <td className="py-3 px-4">{getStatusBadge(run.status)}</td>
                  <td className="py-3 px-4 text-right font-medium text-slate-200">{run.records_fetched}</td>
                  <td className="py-3 px-4 text-right font-semibold text-emerald-400">{run.records_inserted}</td>
                  <td className="py-3 px-4 text-right text-amber-400">{run.records_skipped}</td>
                  <td className="py-3 px-4 text-right text-rose-400">{run.records_failed}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
