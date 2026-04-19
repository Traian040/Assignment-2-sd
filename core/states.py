from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    INGESTED = auto()
    ANALYZED = auto()
    VISUALS_READY = auto()
    AUDIO_TEXT_READY = auto()
    COMPLIANCE_READY = auto()
    PACKAGED = auto()
    COMPLETED = auto()

class Event(Enum):
    START = auto()
    INGEST_DONE = auto()
    ANALYSIS_DONE = auto()
    VISUALS_DONE = auto()
    AUDIO_TEXT_DONE = auto()
    COMPLIANCE_DONE = auto()
    PACKAGING_DONE = auto()