export interface EventEnvelope {
  event_id: string;
  event_type: string;
  timestamp: string;
  source: string;
  payload: unknown;
  metadata?: Record<string, unknown>;
}
