'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api, Case, Mission } from '../lib/api';
import { formatDate, statusColor } from '../lib/utils';

export default function DashboardPage() {
  const [cases, setCases] = useState<Case[]>([]);
  const [missions, setMissions] = useState<Mission[]>([]);
  const [health, setHealth] = useState<{ status: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      api.health().then(setHealth).catch(() => {}),
      api.cases.list().then(r => setCases(r.items.slice(0, 6))).catch(() => {}),
      api.missions.list().then(r => setMissions(r.items.slice(0, 5))).catch(() => {}),
    ]).finally(() => setLoading(false));
  }, []);

  const apiOnline = health?.status === 'ok';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Investigation Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">YemenJPT — Evidence-first, provenance-preserving intelligence</p>
        </div>
        <span className={`badge border ${apiOnline ? 'text-green-700 bg-green-50 border-green-200' : 'text-red-600 bg-red-50 border-red-200'}`}>
          {apiOnline ? '● API Online' : '● API Offline'}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {[
          { label: 'Active Cases', value: cases.filter(c => c.status === 'active').length, color: 'text-blue-600' },
          { label: 'Total Cases', value: cases.length, color: 'text-gray-700' },
          { label: 'Pending Missions', value: missions.filter(m => m.status === 'pending').length, color: 'text-yellow-600' },
          { label: 'Completed', value: missions.filter(m => m.status === 'completed').length, color: 'text-green-600' },
        ].map(s => (
          <div key={s.label} className="card text-center">
            <p className={`text-3xl font-bold ${s.color}`}>{loading ? '…' : s.value}</p>
            <p className="mt-1 text-xs text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-gray-900">Recent Cases</h2>
            <Link href="/cases" className="text-xs text-indigo-600 hover:underline">View all →</Link>
          </div>
          {loading ? <p className="text-sm text-gray-400">Loading…</p> : cases.length === 0 ? (
            <div className="py-8 text-center">
              <p className="text-sm text-gray-400">No cases yet</p>
              <Link href="/cases/new" className="btn-primary mt-3 text-xs">Create First Case</Link>
            </div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {cases.map(c => (
                <li key={c.case_id}>
                  <Link href={`/cases/${c.case_id}`} className="flex items-center justify-between py-2.5 group">
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-gray-800 group-hover:text-indigo-700">{c.title}</p>
                      <p className="text-xs text-gray-400">{formatDate(c.created_at)}</p>
                    </div>
                    <span className={`badge ml-3 shrink-0 ${statusColor(c.status)}`}>{c.status}</span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-gray-900">Recent Missions</h2>
            <Link href="/missions" className="text-xs text-indigo-600 hover:underline">View all →</Link>
          </div>
          {loading ? <p className="text-sm text-gray-400">Loading…</p> : missions.length === 0 ? (
            <div className="py-8 text-center">
              <p className="text-sm text-gray-400">No missions yet</p>
              <Link href="/research" className="btn-primary mt-3 text-xs">Start Research</Link>
            </div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {missions.map(m => (
                <li key={m.mission_id} className="flex items-center justify-between py-2.5">
                  <p className="flex-1 truncate text-sm text-gray-700">{m.objective}</p>
                  <span className={`badge ml-3 shrink-0 ${statusColor(m.status)}`}>{m.status}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="card">
        <h2 className="mb-3 font-semibold text-gray-900">Quick Actions</h2>
        <div className="flex flex-wrap gap-3">
          <Link href="/cases/new" className="btn-primary">+ New Case</Link>
          <Link href="/research" className="btn-secondary">Research Pipeline</Link>
          <Link href="/research?mode=factcheck" className="btn-secondary">Fact Check</Link>
          <Link href="/missions" className="btn-secondary">View Missions</Link>
        </div>
      </div>

      <div className="rounded-lg bg-blue-50 border border-blue-200 px-4 py-3 text-xs text-blue-700">
        <strong>Pipeline:</strong> Source → Ingestion → Normalization → OSINT → News → NLP → Verification → Knowledge Graph → Investigation Brief
        &nbsp;|&nbsp; <strong>Model:</strong> {apiOnline ? 'mock (deterministic)' : 'offline'}
      </div>
    </div>
  );
}