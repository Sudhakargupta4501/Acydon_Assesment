import React from 'react';
import { MapPin, Briefcase, Clock, ExternalLink, ShieldCheck, ChevronRight, Sparkles } from 'lucide-react';

export default function JobCard({ job, onSelect }) {
  const getCompanyInitial = (name) => {
    return name ? name.trim().charAt(0).toUpperCase() : 'J';
  };

  const formatRelativeTime = (dateStr) => {
    if (!dateStr) return 'Recently';
    const date = new Date(dateStr);
    const now = new Date();
    const diffHours = Math.floor((now - date) / (1000 * 60 * 60));

    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 30) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div
      onClick={() => onSelect(job)}
      className="glass-card p-5 hover:border-blue-500/50 hover:bg-slate-900/95 transition-all cursor-pointer group flex flex-col justify-between"
    >
      <div>
        {/* Header: Avatar, Company, Remote Tag */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 flex items-center justify-center font-bold text-lg text-blue-400 group-hover:scale-105 group-hover:border-blue-500/40 transition-all">
              {getCompanyInitial(job.company)}
            </div>
            <div>
              <h4 className="text-xs font-semibold text-slate-400 tracking-wide uppercase">{job.company}</h4>
              <h3 className="font-semibold text-base text-white group-hover:text-blue-400 transition-colors line-clamp-1">
                {job.title}
              </h3>
            </div>
          </div>

          {job.remote && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shrink-0">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
              Remote
            </span>
          )}
        </div>

        {/* Metadata Pills */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <span className="inline-flex items-center text-xs text-slate-300 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700/60">
            <MapPin className="w-3 h-3 mr-1 text-slate-400" />
            {job.location || 'Worldwide'}
          </span>
          <span className="inline-flex items-center text-xs text-slate-300 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700/60">
            <Briefcase className="w-3 h-3 mr-1 text-slate-400" />
            {job.employment_type || 'Full-time'}
          </span>
          {job.salary && job.salary !== 'Not Specified' && (
            <span className="inline-flex items-center text-xs text-emerald-300 bg-emerald-950/40 px-2.5 py-1 rounded-md border border-emerald-800/50">
              {job.salary}
            </span>
          )}
        </div>

        {/* Skills preview tags */}
        {job.skills && job.skills.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {job.skills.slice(0, 4).map((skill, idx) => (
              <span key={idx} className="text-[11px] px-2 py-0.5 rounded-md bg-blue-950/40 text-blue-300 border border-blue-800/40">
                {skill}
              </span>
            ))}
            {job.skills.length > 4 && (
              <span className="text-[11px] px-2 py-0.5 rounded-md bg-slate-800/50 text-slate-400">
                +{job.skills.length - 4} more
              </span>
            )}
          </div>
        )}
      </div>

      {/* Footer: Source & Posted Date */}
      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
        <span className="flex items-center text-slate-400 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 mr-1 text-blue-400" />
          {job.source}
        </span>
        <div className="flex items-center text-slate-400 group-hover:text-blue-400 transition-colors">
          <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" />
          <span>{formatRelativeTime(job.posted_at)}</span>
          <ChevronRight className="w-4 h-4 ml-1 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all" />
        </div>
      </div>
    </div>
  );
}
