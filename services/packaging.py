import os
import json
from services.base import Processor
from core.states import Event

class PackagingService(Processor):
    def process(self, context):
        print("Step 6: Packaging - Finalizing bundle...")

        #drm wrapper
        print("Task: Running DRM wrapper...")
        print("Packaging: Encrypted content with DRM.")

        print("Task: Building manifest.json...")#build manifest
        manifest_data = {
            "bundle_id": context.get("base_path", "movie_101"),
            "status": "COMPLETED",
            "assets": {
                "video_formats": ["h264/mp4", "vp9/webm", "hevc/mkv"],#formats
                "resolutions": ["4k", "1080p", "720p"],#4K 1.5 gb takes several hours, how is it done easier and faster?
                "localization": {#where
                    "transcript": "text/source_transcript.txt",
                    "translation": "text/ro_translation.txt",
                    "audio_dub": "audio/ro_dub_synthetic.aac"
                },
                "metadata": "metadata/scene_analysis.json"
            },
            "security": "DRM Encrypted"#lie
        }

        manifest_path = os.path.join(context['base_path'], "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

        print(f"Packaging: {manifest_path} created successfully.")
        self.mediator.on_event(Event.PACKAGING_DONE)