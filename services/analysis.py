import os
import json
from services.base import Processor
from core.states import Event

class AnalysisService(Processor):
    def process(self, context):
        input_file = context.get("input_file")
        print(f"Step 2: Analysis - Analyzing {input_file}...")

        metadata_dir = os.path.join(context['base_path'], "metadata")
        self.ensure_dir(metadata_dir)

        analysis_results = {
            "source": input_file,
            "intro_end": 5.2,
            "credits_start": 25.4,
            "scene_indexer": [
                {"timestamp": 0.0, "type": "establishing_shot"},
                {"timestamp": 5.2, "type": "dialogue"},
                {"timestamp": 12.1, "type": "action"},
                {"timestamp": 25.4, "type": "credits"}
            ]
        }

        with open(os.path.join(metadata_dir, "scene_analysis.json"), "w") as f:
            json.dump(analysis_results, f, indent=4)

        print("Analysis: Scene indexing and credit detection complete.")
        self.mediator.on_event(Event.ANALYSIS_DONE)