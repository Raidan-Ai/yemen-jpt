"""Agent registry."""
from __future__ import annotations
import sys, os, logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.services.event_bus import InProcessEventBus

def register_all_handlers(bus: InProcessEventBus) -> None:
    from .ingestion import IngestionAgent
    from .normalization import NormalizationAgent
    from .osint import OsintAgent
    from .news_intelligence import NewsIntelligenceAgent
    from .nlp_intelligence import NlpIntelligenceAgent
    from .verification import VerificationAgent
    from .knowledge_graph import KnowledgeGraphAgent
    from .journalist_interface import JournalistInterfaceAgent
    agents = [IngestionAgent(), NormalizationAgent(), OsintAgent(), NewsIntelligenceAgent(), NlpIntelligenceAgent(), VerificationAgent(), KnowledgeGraphAgent(), JournalistInterfaceAgent()]
    for a in agents:
        a.register(bus)
    logging.getLogger(__name__).info("Registered %d agents", len(agents))
