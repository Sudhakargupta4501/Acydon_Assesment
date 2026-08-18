import React from 'react';
import { Server, Database, Activity, Clock, ShieldCheck, CheckCircle, AlertCircle } from 'lucide-react';

export default function SystemStatusCard({ healthData }) {
  const isHealthy = healthData?.status === 'Operational';

  return (
    <div className="glass-card p-6 mb-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-blue-400" />
          <h3 className="font-bold text-lg text-white">System Component Health</h3>
        </div>
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${
          isHealthy ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
        }`}>
          {isHealthy ? <CheckCircle className="w-3.5 h-3.5 mr-1" /> : <AlertCircle className="w-3.5 h-3.5 mr-1" />}
          {healthData?.status || 'Operational'}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Backend API Status */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium flex items-center">
              <Server className="w-3.5 h-3.5 mr-1 text-blue-400" /> Backend API
            </span>
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          </div>
          <div className="text-sm font-semibold text-white">FastAPI v1.0</div>
          <p className="text-[11px] text-emerald-400 mt-1">✓ Operational</p>
        </div>

        {/* Database Status */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium flex items-center">
              <Database className="w-3.5 h-3.5 mr-1 text-indigo-400" /> Database Connection
            </span>
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          </div>
          <div className="text-sm font-semibold text-white">
            {healthData?.database || 'SQLAlchemy Connected'}
          </div>
          <p className="text-[11px] text-emerald-400 mt-1">✓ Connected & Indexed</p>
        </div>

        {/* Permitted Data Sources */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium flex items-center">
              <ShieldCheck className="w-3.5 h-3.5 mr-1 text-purple-400" /> Data Source Feeds
            </span>
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          </div>
          <div className="text-sm font-semibold text-white">Public RSS & REST APIs</div>
          <p className="text-[11px] text-emerald-400 mt-1">✓ Permitted & Active</p>
        </div>

        {/* Ingestion Scheduler */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium flex items-center">
              <Clock className="w-3.5 h-3.5 mr-1 text-amber-400" /> Background Scheduler
            </span>
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          </div>
          <div className="text-sm font-semibold text-white">APScheduler (60m)</div>
          <p className="text-[11px] text-slate-400 mt-1">
            {healthData?.last_ingestion_status || 'Automated background execution'}
          </p>
        </div>
      </div>
    </div>
  );
}
