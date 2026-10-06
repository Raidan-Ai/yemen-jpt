'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { api, Case, YEvent, Entity, Evidence, Report } from '../../../../lib/api';
import { formatDate, confidenceColor, statusColor } from '../../../../lib/utils';

type Tab = 'overview' | 'timeline' | 'evidence' | 'entities' | 'reports';

export default function CaseWorkspacePage() {
  const { id } = useParams<{ id: string }>();
  const [c, setCase] = useState<Case | null>(null);
  const [tab, setTab] = useState<Tab>('overview');
  const [timeline, setTimeline] = useState<YEvent[]>([]);
  const [entities, setEntities] = useState<Entity[]>([]);
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [research, setResearch] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [missionId, setMissionId] = useState('');
  const [error, setError] = useState('');

  const load = () => {
    setLoading(true);
    Promise.allSettled([
      api.cases.get(id).then(setCase),
      api.cases.timeline(id).then(r => setTimeline(r.events)),
      api.cases.entities(id).then(r => setEntities(r.entities)),
      api.cases.evidence(id).then(r => setEvidence(r.evidence)),
      api.reports.list(id).then(r => setReports(r.items)),
    ]).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [id]);

  const handleResearch = async () => {
    if (!research.trim()) return;
    setSubmitting(true); setError('');
    try {
      const r = await api.research.submit({ question: research, case_id: id });
      setMissionId(r.mission_id);
      setResearch('');
      setTimeout(load, 3000);
    } catch {
      setError('Failed to submit. Is the API running?');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="py-16 text-center text-gray-400">Loading case…</div>;
  if (!c) return <div className="py-16 text-center text-red-500">Case not found.</div>;

  const tabs: { key: Tab; label: string; count?: number }[] = [
    { key: 'overview', label: 'Overview' },
    { key: 'timeline', label: 'Timeline', count: timeline.length },
    { key: 'evidence', label: 'Evidence', count: evidence.length },
    { key: 'entities', label: 'Entities', count: entities.length },
    { key: 'reports', label: 'Reports', count: reports.length },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="mb-1 flex items-center gap-1.5 text-sm text-gray-400">
            <Link href="/cases" className="hover:text-indigo-600">Cases</Link>
            <span>/</span>
            <span className="truncate text-gray-600 max-w-xs">{c.title}</span>
          </div>
          <h1 className="text-xl font-bold text-gray-900">{c.title}</h1>
          {c.research_question && <p className="mt-1 text-sm italic text-gray-500">Q: {c.research_question}</p>}
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className={`badge ${statusColor(c.status)}`}>{c.status}</span>
          <button onClick={load} className="btn-secondary text-xs">↻ Refresh</button>
        </div>
      </div>

      <div className="card flex gap-3">
        <input value={research} onChange={e => setResearch(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !submitting && handleResearch()}
          className="input flex-1" placeholder="Submit investigation question or paste source URL…" />
        <button onClick={handleResearch} disabled={submitting || !research.trim()} className="btn-primary shrink-0">
          {submitting ? 'Running…' : 'Investigate'}
        </button>
      </div>
      {error && <p className="rounded bg-red-50 border border-red-200 px-3 py-2 text-xs text-red-600">{error}</p>}
      {missionId && (
        <p className="rounded bg-green-50 border border-green-200 px-3 py-2 text-xs text-green-700">
          ✓ Mission <code className="font-mono">{missionId}</code> started — agents processing…
        </p>
      )}

      <div className="flex gap-0 border-b border-gray-200">
        {tabs.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`border-b-2 px-4 py-2 text-sm font-medium transition-colors ${tab === t.key ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}>
            {t.label}
            {t.count !== undefined && <span className="ml-1 text-xs text-gray-400">({t.count})</span>}
          </button>
        ))}
      </div>

      {tab === 'overview' && (
        <div className="space-y-4">
          <div className="card grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[['Events', timeline.length, 'text-blue-600'], ['Entities', entities.length, 'text-purple-600'], ['Evidence', evidence.length, 'text-orange-600'], ['Reports', reports.length, 'text-green-600']].map(([l, v, color]) => (
              <div key={String(l)} className="text-center">
                <p className={`text-3xl font-bold ${color}`}>{v}</p>
                <p className="mt-1 text-xs text-gray-500">{l}</p>
              </div>
            ))}
          </div>
          {c.description && <div className="card"><p className="text-sm text-gray-700">{c.description}</p></div>}
          <div className="card text-xs text-gray-400 space-y-1">
            <p>Created: {formatDate(c.created_at)}</p>
            <p>Updated: {formatDate(c.updated_at)}</p>
            <p>ID: <code className="font-mono">{c.case_id}</code></p>
          </div>
        </div>
      )}

      {tab === 'timeline' && (
        timeline.length === 0 ? <p className="text-sm text-gray-400">No events yet. Submit an investigation to start the pipeline.</p> : (
          <ul className="relative space-y-3 border-l-2 border-gray-200 pl-4">
            {timeline.map(ev => (
              <li key={ev.event_id} className="relative">
                <span className="absolute -left-[9px] top-2 h-3 w-3 rounded-full border-2 border-white bg-indigo-500" />
                <div className="card ml-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-indigo-600">{ev.event_type}</span>
                    <span className="text-xs text-gray-400">{formatDate(ev.occurred_at)}</span>
                  </div>
                  {ev.confidence && (
                    <span className={`badge mt-1 border ${confidenceColor(ev.confidence.label)}`}>
                      {ev.confidence.label} ({(ev.confidence.score * 100).toFixed(0)}%)
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )
      )}

      {tab === 'evidence' && (
        evidence.length === 0 ? <p className="text-sm text-gray-400">No evidence yet.</p> : (
          <div className="space-y-2">
            {evidence.map(ev => (
              <div key={ev.evidence_id} className="card space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="badge bg-blue-50 text-blue-600">{ev.type}</span>
                  <span className="font-mono text-xs text-gray-400">{ev.source_id}</span>
                </div>
                {ev.excerpt && <p className="line-clamp-3 text-sm text-gray-700">{ev.excerpt}</p>}
                {ev.locator && <a href={ev.locator} target="_blank" rel="noopener noreferrer" className="break-all text-xs text-indigo-500 hover:underline">{ev.locator}</a>}
              </div>
            ))}
          </div>
        )
      )}

      {tab === 'entities' && (
        entities.length === 0 ? <p className="text-sm text-gray-400">No entities extracted yet.</p> : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {entities.map(en => (
              <div key={en.entity_id} className="card">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-800">{en.name}</span>
                  <span className="badge bg-purple-50 text-purple-600">{en.type}</span>
                </div>
                <p className="mt-1 text-xs text-gray-400">Confidence: {(en.confidence * 100).toFixed(0)}%</p>
                {en.properties?.note && <p className="mt-1 text-xs italic text-gray-500">{String(en.properties.note)}</p>}
              </div>
            ))}
          </div>
        )
      )}

      {tab === 'reports' && (
        reports.length === 0 ? <p className="text-sm text-gray-400">No reports yet. Run an investigation to generate a brief.</p> : (
          <div className="space-y-4">
            {reports.map(r => (
              <div key={r.report_id} className="card space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium text-gray-800">{r.title}</h3>
                  <span className={`badge border ${confidenceColor(r.confidence.label)}`}>{r.confidence.label}</span>
                </div>
                <p className="whitespace-pre-wrap text-sm text-gray-700">{r.content}</p>
                {r.editorial_note && (
                  <div className="rounded-lg bg-yellow-50 border border-yellow-200 px-3 py-2 text-xs text-yellow-700">
                    ⚠ {r.editorial_note}
                  </div>
                )}
                <p className="text-xs text-gray-400">{formatDate(r.generated_at)}</p>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
}