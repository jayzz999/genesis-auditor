'use client';

import { useState, useEffect } from 'react';
import { Play, RefreshCw, CheckCircle, XCircle, Clock, AlertTriangle, Activity } from 'lucide-react';

interface JobExecution {
  id: string;
  title: string;
  status: 'running' | 'succeeded' | 'failed' | 'pending';
  startedAt: string;
  completedAt?: string;
  duration?: number;
  auditData: {
    domain: string;
    criticalCount: number;
    highCount: number;
    riskScore: number;
  };
}

export default function OpusMonitorDashboard() {
  const [jobs, setJobs] = useState<JobExecution[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDomain, setSelectedDomain] = useState('');
  const [eventType, setEventType] = useState('audit_completed');

  const fetchJobs = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/opus/jobs`);
      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    }
  };

  const triggerJob = async () => {
    if (!selectedDomain) {
      alert('Please enter a domain name');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/opus/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          domain: selectedDomain,
          eventType: eventType,
        }),
      });

      const data = await response.json();
      if (data.success) {
        alert(`Job triggered successfully! ID: ${data.jobExecutionId}`);
        fetchJobs();
        setSelectedDomain('');
      }
    } catch (error) {
      alert('Failed to trigger job');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'succeeded':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'running':
        return <Clock className="w-5 h-5 text-blue-500 animate-pulse" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getRiskBadgeColor = (score: number) => {
    if (score >= 80) return 'bg-red-100 text-red-800';
    if (score >= 60) return 'bg-orange-100 text-orange-800';
    if (score >= 40) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-slate-900">
              Opus Workflow Monitor
            </h1>
          </div>
          <p className="text-slate-600 ml-13">
            Real-time monitoring and triggering for Genesis Auditor Opus integration
          </p>
        </div>

        {/* Trigger Panel */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8 border border-slate-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Play className="w-5 h-5 text-blue-500" />
            Trigger New Audit Job
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Domain Name
              </label>
              <input
                type="text"
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                placeholder="example.com"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Event Type
              </label>
              <select
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="audit_completed">Audit Completed</option>
                <option value="critical_vulnerability_alert">Critical Alert</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={triggerJob}
                disabled={loading}
                className="w-full px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    Triggering...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    Trigger Job
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Jobs Table */}
        <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
          <div className="p-6 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-xl font-semibold">Recent Job Executions</h2>
            <button
              onClick={fetchJobs}
              className="px-4 py-2 text-sm text-slate-600 hover:text-slate-900 flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Domain
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Risk Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Findings
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Duration
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Completed
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {jobs.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                      No jobs yet. Trigger your first audit above!
                    </td>
                  </tr>
                ) : (
                  jobs.map((job) => (
                    <tr key={job.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(job.status)}
                          <span className="text-sm font-medium capitalize">
                            {job.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-medium">
                        {job.auditData.domain}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskBadgeColor(
                            job.auditData.riskScore
                          )}`}
                        >
                          {job.auditData.riskScore}/100
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                        <div className="flex gap-3">
                          <span className="flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3 text-red-500" />
                            {job.auditData.criticalCount} Critical
                          </span>
                          <span className="flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3 text-orange-500" />
                            {job.auditData.highCount} High
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                        {job.duration ? `${job.duration}s` : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                        {job.completedAt
                          ? new Date(job.completedAt).toLocaleString()
                          : '-'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <div className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="text-sm font-medium text-slate-600 mb-1">Total Jobs</div>
            <div className="text-3xl font-bold text-slate-900">{jobs.length}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="text-sm font-medium text-slate-600 mb-1">Succeeded</div>
            <div className="text-3xl font-bold text-green-600">
              {jobs.filter((j) => j.status === 'succeeded').length}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="text-sm font-medium text-slate-600 mb-1">Running</div>
            <div className="text-3xl font-bold text-blue-600">
              {jobs.filter((j) => j.status === 'running').length}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 border border-slate-200">
            <div className="text-sm font-medium text-slate-600 mb-1">Failed</div>
            <div className="text-3xl font-bold text-red-600">
              {jobs.filter((j) => j.status === 'failed').length}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
