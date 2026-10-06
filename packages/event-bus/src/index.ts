import { EventEmitter } from 'eventemitter3';

export type EventHandler<T = unknown> = (payload: T) => void;

export interface EventBus<T extends string> {
  on<K extends T>(event: K, handler: EventHandler): void;
  off<K extends T>(event: K, handler: EventHandler): void;
  emit<K extends T>(event: K, payload: unknown): void;
}

export function createEventBus<T extends string>(): EventBus<T> {
  const bus = new EventEmitter<Record<T, unknown>>();
  return {
    on: (event, handler) => bus.on(event as string, handler as EventHandler),
    off: (event, handler) => bus.off(event as string, handler as EventHandler),
    emit: (event, payload) => bus.emit(event as string, payload),
  };
}
