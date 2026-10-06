# yemenjpt-event-bus

TypeScript event bus abstraction for YemenJPT.

## Install

```bash
npm install
```

## Usage

```ts
import { createEventBus } from './src';

const bus = createEventBus<'message' | 'alert'>();
bus.on('message', (payload) => console.log(payload));
bus.emit('message', { text: 'hello' });
```