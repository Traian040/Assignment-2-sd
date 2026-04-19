from core.states import State, Event


class Orchestrator:
    def __init__(self, workflow):
        self.workflow = workflow
        self.processors = {}
        self.context = {"base_path": "movie_101"}

    def register_processor(self, event: Event, processor):
        self.processors[event] = processor

    def start_pipeline(self):
        print("--- Global Release Pipeline Started ---")
        if self.workflow.transition(Event.START):
            self._run_current_processor()

    def on_event(self, event: Event):
        if self.workflow.transition(event):
            self._run_current_processor()

    def _run_current_processor(self):
        state_to_event = {
            State.INGESTED: Event.INGEST_DONE,
            State.ANALYZED: Event.ANALYSIS_DONE,
            State.VISUALS_READY: Event.VISUALS_DONE,
            State.AUDIO_TEXT_READY: Event.AUDIO_TEXT_DONE,
            State.COMPLIANCE_READY: Event.COMPLIANCE_DONE,
            State.PACKAGED: Event.PACKAGING_DONE,
        }

        event = state_to_event.get(self.workflow.current_state)
        if event in self.processors:
            self.processors[event].process(self.context)
        elif self.workflow.current_state == State.COMPLETED:
            print("--- Pipeline Finalized ---")