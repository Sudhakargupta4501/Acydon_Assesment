import React, { useState, useEffect } from 'react';
import StatCards from '../components/StatCards';
import SystemStatusCard from '../components/SystemStatusCard';
import JobFilter from '../components/JobFilter';
import JobCard from '../components/JobCard';
import JobDetailModal from '../components/JobDetailModal';
import Pagination from '../components/Pagination';
import { api } from '../services/api';
import { Briefcase, AlertCircle, RefreshCw } from 'lucide-react';

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [statusSummary, setStatusSummary] = useState(null);
  const [healthData, setHealthData] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
    q: '',
    remote: null,
    employment_type: '',
    source: '',
    page: 1,
    limit: 12
  });

  const loadData = async (showLoading = true) => {
    if (showLoading) setIsLoading(true);
    setError(null);

    try {
      // Fetch Jobs, Status, and Health in parallel
      const [jobsData, statusRes, healthRes] = await Promise.allSettled([
        api.getJobs(filters),
        api.getIngestionStatus(),
        api.getHealth()
      ]);

      if (jobsData.status === 'fulfilled') {
        setJobs(jobsData.value.jobs || []);
        setTotal(jobsData.value.total || 0);
        setPages(jobsData.value.pages || 1);
      } else {
        setError('Failed to load job listings from API server.');
      }

      if (statusRes.status === 'fulfilled') {
        setStatusSummary(statusRes.value);
      }

      if (healthRes.status === 'fulfilled') {
        setHealthData(healthRes.value);
      }
    } catch (err) {
      console.error(err);
      setError('Connection to backend API failed. Is the FastAPI server running?');
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [filters]);

  const handleResetFilters = () => {
    setIsRefreshing(true);
    setFilters({
      q: '',
      remote: null,
      employment_type: '',
      source: '',
      page: 1,
      limit: 12
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Metrics Ribbon */}
      <StatCards statusSummary={statusSummary} />

      {/* Health Diagnostic Card */}
      <SystemStatusCard healthData={healthData} />

      {/* Filter Component */}
      <JobFilter
        filters={filters}
        setFilters={setFilters}
        onReset={handleResetFilters}
        isRefreshing={isRefreshing}
      />

      {/* Error Notice */}
      {error && (
        <div className="p-4 mb-6 glass-card border-rose-500/50 bg-rose-950/20 text-rose-300 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            <span className="text-sm font-medium">{error}</span>
          </div>
          <button
            onClick={() => loadData()}
            className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-lg shadow-md transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Job Grid / List Section */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, idx) => (
            <div key={idx} className="glass-card p-5 animate-pulse h-48 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="h-4 bg-slate-800 rounded w-1/3"></div>
                <div className="h-6 bg-slate-800 rounded w-3/4"></div>
                <div className="flex space-x-2">
                  <div className="h-4 bg-slate-800 rounded w-16"></div>
                  <div className="h-4 bg-slate-800 rounded w-16"></div>
                </div>
              </div>
              <div className="h-4 bg-slate-800 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : jobs.length === 0 ? (
        <div className="glass-card p-12 text-center my-8">
          <div className="w-16 h-16 bg-slate-900 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-slate-800 text-slate-400">
            <Briefcase className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-white mb-1">No Jobs Found</h3>
          <p className="text-slate-400 text-sm max-w-md mx-auto mb-6">
            We couldn't find any job listings matching your current filter criteria. Try adjusting your search query or trigger a fresh ingestion run.
          </p>
          <button
            onClick={handleResetFilters}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-xl transition-all"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reset All Filters</span>
          </button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {jobs.map((job) => (
              <JobCard key={job.id} job={job} onSelect={setSelectedJob} />
            ))}
          </div>

          <Pagination
            page={filters.page}
            pages={pages}
            total={total}
            limit={filters.limit}
            onPageChange={(newPage) => setFilters(prev => ({ ...prev, page: newPage }))}
          />
        </>
      )}

      {/* Detail View Modal */}
      {selectedJob && (
        <JobDetailModal job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </div>
  );
}
