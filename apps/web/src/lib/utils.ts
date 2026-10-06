export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}

export function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return iso;
  }
}

export function confidenceColor(label: string): string {
  switch (label) {
    case 'high':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'medium':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'low':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
}

export function statusColor(status: string): string {
  switch (status) {
    case 'active':
      return 'text-blue-700 bg-blue-50';
    case 'closed':
      return 'text-gray-600 bg-gray-100';
    case 'archived':
      return 'text-gray-400 bg-gray-50';
    case 'pending':
      return 'text-yellow-600 bg-yellow-50';
    case 'completed':
      return 'text-green-600 bg-green-50';
    case 'failed':
      return 'text-red-600 bg-red-50';
    case 'running':
      return 'text-blue-600 bg-blue-50';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}