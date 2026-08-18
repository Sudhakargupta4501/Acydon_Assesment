import React from 'react';
import { X, MapPin, Briefcase, Calendar, ExternalLink, ShieldCheck, DollarSign, Tag } from 'lucide-react';

export default function JobDetailModal({ job, onClose }) {
  if (!job) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/80 backdrop-blur-sm overflow-y-auto animate-fade-in">
      <div className="glass-card w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden border border-slate-700 shadow-2xl relative">
        {/* Modal Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between bg-slate-900/90">
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider text-blue-400">{job.company}</span>
              {job.remote && (
                <span className="px-2 py-0.5 text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  Remote
                </span>
              )}
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">{job.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-slate-300 text-sm">
          {/* Metadata Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 flex items-center mb-1">
                <MapPin className="w-3.5 h-3.5 mr-1 text-blue-400" /> Location
              </span>
              <span className="font-medium text-white truncate">{job.location || 'Remote'}</span>
            </div>

            <div className="flex flex-col">
              <span className="text-xs text-slate-400 flex items-center mb-1">
                <Briefcase className="w-3.5 h-3.5 mr-1 text-indigo-400" /> Type
              </span>
              <span className="font-medium text-white">{job.employment_type || 'Full-time'}</span>
            </div>

            <div className="flex flex-col">
              <span className="text-xs text-slate-400 flex items-center mb-1">
                <DollarSign className="w-3.5 h-3.5 mr-1 text-emerald-400" /> Salary
              </span>
              <span className="font-medium text-emerald-400">{job.salary || 'Not Specified'}</span>
            </div>

            <div className="flex flex-col">
              <span className="text-xs text-slate-400 flex items-center mb-1">
                <Calendar className="w-3.5 h-3.5 mr-1 text-amber-400" /> Posted
              </span>
              <span className="font-medium text-white">
                {job.posted_at ? new Date(job.posted_at).toLocaleDateString() : 'Recent'}
              </span>
            </div>
          </div>

          {/* Source Attribution */}
          <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-900/60 px-3 py-2 rounded-lg border border-slate-800">
            <ShieldCheck className="w-4 h-4 text-blue-400" />
            <span>Ingested from public source: <strong className="text-slate-200">{job.source}</strong></span>
          </div>

          {/* Required Skills */}
          {job.skills && job.skills.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center">
                <Tag className="w-3.5 h-3.5 mr-1 text-blue-400" /> Required Skills & Keywords
              </h4>
              <div className="flex flex-wrap gap-2">
                {job.skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 bg-blue-950/60 text-blue-300 border border-blue-800/60 rounded-lg text-xs font-medium">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Job Description */}
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Job Description</h4>
            <div
              className="prose prose-invert max-w-none text-slate-300 leading-relaxed bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 overflow-x-auto"
              dangerouslySetInnerHTML={{ __html: job.description || '<p>No detailed description provided by source feed.</p>' }}
            />
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/90 flex items-center justify-between">
          <div className="text-xs text-slate-400">
            Internal ID: <code className="font-mono text-slate-400">{job.id.substring(0, 8)}...</code>
          </div>
          <a
            href={job.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl shadow-lg shadow-blue-600/30 transition-all text-sm"
          >
            <span>Open Original Listing</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
}
