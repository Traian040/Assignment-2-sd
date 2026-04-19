from core.states import State, Event


class Workflow:
    def __init__(self):
        self.current_state = State.IDLE

    def transition(self, event: Event) -> bool:
        transitions = {
            (State.IDLE, Event.START): State.INGESTED,
            (State.INGESTED, Event.INGEST_DONE): State.ANALYZED,
            (State.ANALYZED, Event.ANALYSIS_DONE): State.VISUALS_READY,
            (State.VISUALS_READY, Event.VISUALS_DONE): State.AUDIO_TEXT_READY,
            (State.AUDIO_TEXT_READY, Event.AUDIO_TEXT_DONE): State.COMPLIANCE_READY,
            (State.COMPLIANCE_READY, Event.COMPLIANCE_DONE): State.PACKAGED,
            (State.PACKAGED, Event.PACKAGING_DONE): State.COMPLETED,
        }

        next_state = transitions.get((self.current_state, event))
        if next_state:
            print(f"Workflow: {self.current_state.name} -> {next_state.name}")
            self.current_state = next_state
            return True
        return False