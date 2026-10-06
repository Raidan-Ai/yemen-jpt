'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api, Case } from '../../lib/api';
import { formatDate, statusColor } from '../../lib/utils';

export default function CasesPage() {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    api.cases.list().then(r => setCases(r.items)).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const filtered = filter ? cases.filter(c => c.status === filter) : cases;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">Cases</h1>
        <Link href="/cases/new" className="btn-primary">+ New Case</Link>
      </div>
      <div className="flex flex-wrap gap-2">
        {['', 'active', 'closed', 'archived'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            className={`badge cursor-pointer px-3 py-1 text-xs ${filter === s ? 'bg-indigo-100 text-indigo-700 font-semibold' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>
            {s || 'All'}
          </button>
        ))}
      </div>
      {loading ? <p className="text-gray-400">Loading…</p> : filtered.length === 0 ? (
        <div className="card py-16 text-center">
          <p className="text-gray-400">No cases found.</p>
          <Link href="/cases/new" className="btn-primary mt-4">Create First Case</Link>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(c => (
            <Link key={c.case_id} href={`/cases/${c.case_id}`}
              className="card flex items-center justify-between transition-colors hover:border-indigo-300 group">
              <div className="min-w-0 flex-1">
                <p className="truncate font-medium text-gray-900 group-hover:text-indigo-700">{c.title}</p>
                {c.research_question && <p className="truncate text-xs text-gray-500 mt-0.5 italic">{c.research_question}</p>}
                <p className="mt-1 text-xs text-gray-400">{formatDate(c.created_at)}</p>
              </div>
              <span className={`badge ml-4 shrink-0 ${statusColor(c.status)}`}>{c.status}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
