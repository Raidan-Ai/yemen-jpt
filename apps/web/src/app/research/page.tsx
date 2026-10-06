'use client';
import { useState } from 'react';
import { api } from '../../lib/api';

export default function ResearchPage() {
  const [mode, setMode] = useState<'research' | 'factcheck'>('research');
  const [question, setQuestion] = useState('');
  const [caseId, setCaseId] = useState('');
  const [result, setResult] = useState<{ mission_id: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) { setError('Enter a question or claim'); return; }
    setLoading(true); setError(''); setResult(null);
    try {
      const r = mode === 'research'
        ? await api.research.submit({ question, case_id: caseId || undefined })
        : await api.research.factCheck({ claim: question, case_id: caseId || undefined });
      setResult(r);
      setQuestion('');
    } catch {
      setError('Failed to submit. Is the API running at http://localhost:8000?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl space-y-5">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Research & Intelligence</h1>
        <p className="mt-1 text-sm text-gray-500">Submit a question or claim to run the full intelligence pipeline.</p>
      </div>

      <div className="flex gap-2">
        {(['research', 'factcheck'] as const).map(m => (
          <button key={m} onClick={() => setMode(m)}
            className={`badge cursor-pointer px-4 py-1.5 text-sm font-medium ${mode === m ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>
            {m === 'research' ? '🔍 Research' : '✓ Fact Check'}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <div className="rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-600">{error}</div>}

        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            {mode === 'research' ? 'Research Question' : 'Claim to Verify'}
          </label>
          <textarea value={question} onChange={e => setQuestion(e.target.value)} rows={4} className="input resize-none"
            placeholder={mode === 'research'
              ? 'What caused the Yemen currency collapse in 2019?'
              : 'The Houthi forces captured Aden in March 2015.'} />
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Case ID <span className="text-gray-400">(optional)</span></label>
          <input value={caseId} onChange={e => setCaseId(e.target.value)} className="input"
            placeholder="Attach to existing case (UUID)" />
        </div>

        <button type="submit" disabled={loading || !question.trim()} className="btn-primary w-full justify-center py-2">
          {loading ? 'Submitting…' : mode === 'research' ? 'Start Research Pipeline' : 'Verify Claim'}
        </button>
      </form>

      {result && (
        <div className="card space-y-2 border-green-200 bg-green-50">
          <p className="font-medium text-green-700">✓ Mission created successfully</p>
          <p className="text-xs text-green-600 font-mono">{result.mission_id}</p>
          <p className="text-xs text-gray-600">
            The intelligence pipeline is running. Check /missions for status, or your case for results.
          </p>
          <div className="mt-1 rounded-lg bg-yellow-50 border border-yellow-200 px-3 py-2 text-xs text-yellow-700">
            ⚠ All results are AI-assisted. Human editorial review required before publication.
            All mock results are labeled [SYNTHETIC] and are not real intelligence.
          </div>
        </div>
      )}

      <div className="card text-xs text-gray-400 space-y-1">
        <p className="font-medium text-gray-500">Pipeline steps:</p>
        <p>source.submit → Ingestion → Normalization → OSINT → News Intelligence → NLP → Verification → Knowledge Graph → Investigation Brief</p>
      </div>
    </div>
  );
}