'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../../../lib/api';

export default function NewCasePage() {
  const router = useRouter();
  const [form, setForm] = useState({ title: '', description: '', research_question: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title.trim()) { setError('Title is required'); return; }
    setLoading(true); setError('');
    try {
      const c = await api.cases.create({
        title: form.title,
        description: form.description || undefined,
        research_question: form.research_question || undefined,
      });
      router.push(`/cases/${c.case_id}`);
    } catch {
      setError('Failed to create case. Is the API running at http://localhost:8000?');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl space-y-4">
      <div className="flex items-center gap-2 text-sm text-gray-400">
        <a href="/cases" className="hover:text-indigo-600">Cases</a>
        <span>/</span>
        <span className="text-gray-600">New Case</span>
      </div>
      <h1 className="text-xl font-bold text-gray-900">New Investigation Case</h1>
      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <div className="rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-600">{error}</div>}
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Title <span className="text-red-500">*</span></label>
          <input value={form.title} onChange={set('title')} className="input" placeholder="e.g. Yemen Currency Crisis Investigation" />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Research Question</label>
          <input value={form.research_question} onChange={set('research_question')} className="input"
            placeholder="What are the causes of the currency collapse?" />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
          <textarea value={form.description} onChange={set('description')} rows={3} className="input resize-none"
            placeholder="Brief case overview…" />
        </div>
        <div className="flex gap-3 pt-1">
          <button type="submit" disabled={loading} className="btn-primary">{loading ? 'Creating…' : 'Create Case'}</button>
          <button type="button" onClick={() => router.back()} className="btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  );
}