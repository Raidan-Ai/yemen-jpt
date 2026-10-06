"""Knowledge Graph Agent — build Yemen Reality Graph."""
from __future__ import annotations
import uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

_graph_nodes: dict[str, dict] = {}
_graph_edges: list[dict] = []

class KnowledgeGraphAgent(BaseAgent):
    agent_id = "knowledge_graph_agent"
    purpose = "Build Yemen Reality Graph"
    input_event_types = ["nlp.extracted", "verification.completed"]
    output_event_types = ["graph.updated"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        nodes_added, edges_added = [], []
        for entity in p.get("entities", []):
            nid = entity.get("entity_id", str(uuid.uuid4()))
            _graph_nodes[nid] = {"node_id": nid, "type": entity.get("type", "Unknown"), "name": entity.get("name", ""), "confidence": entity.get("confidence", 0.3), "case_id": event.case_id, "source_event_id": event.event_id, "created_at": datetime.now(timezone.utc).isoformat(), "properties": entity}
            nodes_added.append(nid)
            if event.case_id:
                from ..routes.cases import add_entity_to_case
                add_entity_to_case(event.case_id, _graph_nodes[nid])
        for rel in p.get("relationships", []):
            src = self._resolve(rel.get("source", ""))
            tgt = self._resolve(rel.get("target", ""))
            if src and tgt:
                eid = str(uuid.uuid4())
                _graph_edges.append({"edge_id": eid, "source_entity_id": src, "target_entity_id": tgt, "type": rel.get("type", "RELATED_TO"), "confidence": 0.3})
                edges_added.append(eid)
        out = CanonicalEvent(event_type="graph.updated", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"nodes_added": nodes_added, "edges_added": edges_added, "total_nodes": len(_graph_nodes), "total_edges": len(_graph_edges)}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.5, label="medium"))
        await get_event_bus().publish(out)

    def _resolve(self, name: str) -> str | None:
        for nid, n in _graph_nodes.items():
            if n.get("name", "").lower() == name.lower():
                return nid
        return None

def get_graph_state() -> dict:
    return {"nodes": list(_graph_nodes.values()), "edges": _graph_edges, "total_nodes": len(_graph_nodes), "total_edges": len(_graph_edges)}
