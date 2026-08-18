import React from 'react';
import { Search, Filter, X, RefreshCw, Briefcase, MapPin, Globe } from 'lucide-react';

export default function JobFilter({ filters, setFilters, onReset, isRefreshing }) {
  const handleChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value, page: 1 }));
  };

  return (
    <div className="glass-card p-4 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
        {/* Search Input */}
        <div className="md:col-span-5 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Search by title, skills, company, or location..."
            value={filters.q || ''}
            onChange={(e) => handleChange('q', e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-lg pl-10 pr-9 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
          />
          {filters.q && (
            <button
              onClick={() => handleChange('q', '')}
              className="absolute right-3 top-3 text-slate-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Work Mode Filter (Remote / On-site) */}
        <div className="md:col-span-2 relative">
          <select
            value={filters.remote === null || filters.remote === undefined ? '' : String(filters.remote)}
            onChange={(e) => {
              const val = e.target.value;
              handleChange('remote', val === '' ? null : val === 'true');
            }}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors cursor-pointer"
          >
            <option value="">Work Mode: All</option>
            <option value="true">Remote Only</option>
            <option value="false">On-site / Hybrid</option>
          </select>
        </div>

        {/* Employment Type Filter */}
        <div className="md:col-span-2 relative">
          <select
            value={filters.employment_type || ''}
            onChange={(e) => handleChange('employment_type', e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors cursor-pointer"
          >
            <option value="">Employment: All</option>
            <option value="Full-time">Full-time</option>
            <option value="Contract">Contract</option>
            <option value="Part-time">Part-time</option>
            <option value="Internship">Internship</option>
          </select>
        </div>

        {/* Source Filter */}
        <div className="md:col-span-2 relative">
          <select
            value={filters.source || ''}
            onChange={(e) => handleChange('source', e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors cursor-pointer"
          >
            <option value="">Source: All</option>
            <option value="WeWorkRemotely RSS">WeWorkRemotely RSS</option>
            <option value="Arbeitnow Public API">Arbeitnow API</option>
            <option value="Sandbox Mock Source">Sandbox Mock</option>
          </select>
        </div>

        {/* Reset Button */}
        <div className="md:col-span-1 flex justify-end">
          <button
            onClick={onReset}
            title="Reset Filters"
            className="w-full h-full flex items-center justify-center p-2.5 bg-slate-800/80 hover:bg-slate-700 text-slate-300 rounded-lg border border-slate-700 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
    </div>
  );
}
