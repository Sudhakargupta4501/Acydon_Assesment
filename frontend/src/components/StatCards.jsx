import React from 'react';
import { Database, CheckCircle2, AlertTriangle, Layers, ArrowUpRight, Activity } from 'lucide-react';

export default function StatCards({ statusSummary }) {
  const totalJobs = statusSummary?.total_jobs ?? 0;
  const activeSources = statusSummary?.active_sources ?? 0;
  const lastRun = statusSummary?.last_run;
  const isHealthy = statusSummary?.healthy ?? true;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Total Jobs */}
      <div className="glass-card p-5 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Jobs Ingested</span>
          <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
            <Database className="w-5 h-5" />
          </div>
        </div>
        <div className="text-3xl font-extrabold text-white tracking-tight">{totalJobs.toLocaleString()}</div>
        <p className="text-xs text-slate-400 mt-2 flex items-center">
          <span className="text-emerald-400 font-medium inline-flex items-center mr-1">
            <ArrowUpRight className="w-3 h-3" /> Normalized
          </span>
          records in DB
        </p>
      </div>

      {/* Active Sources */}
      <div className="glass-card p-5 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Permitted Data Sources</span>
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
            <Layers className="w-5 h-5" />
          </div>
        </div>
        <div className="text-3xl font-extrabold text-white tracking-tight">{activeSources || 3}</div>
        <p className="text-xs text-slate-400 mt-2">
          RSS feeds, REST APIs, Sandbox Mock
        </p>
      </div>

      {/* Last Ingestion Result */}
      <div className="glass-card p-5 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Last Run Yield</span>
          <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg">
            <Activity className="w-5 h-5" />
          </div>
        </div>
        <div className="flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-emerald-400">{lastRun ? lastRun.records_inserted : 0}</span>
          <span className="text-xs text-slate-400">new inserted</span>
        </div>
        <div className="text-xs text-slate-400 mt-2 flex items-center space-x-2">
          <span className="text-amber-400 font-medium">{lastRun ? lastRun.records_skipped : 0} dupes</span>
          <span>•</span>
          <span className="text-rose-400 font-medium">{lastRun ? lastRun.records_failed : 0} invalid</span>
        </div>
      </div>

      {/* Pipeline Status */}
      <div className="glass-card p-5 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Pipeline Health</span>
          <div className={`p-2 rounded-lg ${isHealthy ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
            {isHealthy ? <CheckCircle2 className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
          </div>
        </div>
        <div className="text-xl font-bold text-white tracking-tight">
          {isHealthy ? '100% Operational' : 'Degraded Mode'}
        </div>
        <p className="text-xs text-slate-400 mt-2 truncate">
          {lastRun ? `Last run: ${new Date(lastRun.started_at).toLocaleTimeString()}` : 'Awaiting initial run'}
        </p>
      </div>
    </div>
  );
}
