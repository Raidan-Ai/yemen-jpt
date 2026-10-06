'use client';
import { useEffect, useState } from 'react';
import { api, Mission } from '../../lib/api';
import { formatDate, statusColor } from '../../lib/utils';

export default function MissionsPage() {
  const [missions, setMissions] = useState<Mission[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    api.missions.list().then(r => setMissions(r.items)).catch(() => {}).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Missions</h1>
          <p className="mt-1 text-sm text-gray-500">Long-running intelligence pipeline executions</p>
        </div>
        <button onClick={load} className="btn-secondary text-xs">↻ Refresh</button>
      </div>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : missions.length === 0 ? (
        <div className="card py-16 text-center">
          <p className="text-gray-400">No missions yet.</p>
          <a href="/research" className="btn-primary mt-4">Start Research Pipeline</a>
        </div>
      ) : (
        <div className="space-y-2">
          {missions.map(m => (
            <div key={m.mission_id} className="card">
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-gray-800">{m.objective}</p>
                  <p className="mt-1 text-xs text-gray-400">{formatDate(m.created_at)}</p>
                  <p className="mt-0.5 font-mono text-xs text-gray-300">{m.mission_id}</p>
                </div>
                <span className={`badge shrink-0 ${statusColor(m.status)}`}>{m.status}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}