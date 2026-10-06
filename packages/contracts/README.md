# yemenjpt-contracts

Shared Pydantic schemas, event payloads, and envelope formats for YemenJPT.

## Install

```bash
pip install -e .
```

## Usage

```python
from yemenjpt_contracts import BaseEvent, IntelligenceEvent

event = IntelligenceEvent(
    event_id="evt_123",
    event_type="intelligence",
    source="osint",
    payload={"actor": "Houthi"},
)
```