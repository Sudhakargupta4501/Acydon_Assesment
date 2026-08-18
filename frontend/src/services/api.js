import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

const client = axios.create({
  baseURL: `${API_BASE}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const api = {
  // Jobs API
  async getJobs(params = {}) {
    const response = await client.get('/jobs', { params });
    return response.data;
  },

  async getJobById(id) {
    const response = await client.get(`/jobs/${id}`);
    return response.data;
  },

  // Ingestion Pipeline API
  async triggerIngestion(sourceType = null, sourceUrl = null) {
    const params = {};
    if (sourceType) params.source_type = sourceType;
    if (sourceUrl) params.source_url = sourceUrl;
    const response = await client.post('/ingestion/run', null, { params });
    return response.data;
  },

  async getIngestionStatus() {
    const response = await client.get('/ingestion/status');
    return response.data;
  },

  async getIngestionRuns(page = 1, limit = 10) {
    const response = await client.get('/ingestion/runs', { params: { page, limit } });
    return response.data;
  },

  // Health API
  async getHealth() {
    const response = await client.get('/health');
    return response.data;
  }
};
