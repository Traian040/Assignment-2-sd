import os
import whisper
from services.base import Processor
from core.states import Event


class AudioTextService(Processor):
    def process(self, context):
        input_file = context.get("input_file")
        print(f"Step 4: Audio/Text - Starting transcription for {input_file}...")
        #setup directories
        text_dir = os.path.join(context['base_path'], "text")
        audio_dir = os.path.join(context['base_path'], "audio")
        self.ensure_dir(text_dir)
        self.ensure_dir(audio_dir)

        #load the model
        model = whisper.load_model("base")
        print("Whisper: STT file...")
        result = model.transcribe(input_file, fp16=False)
        transcript_text = result["text"]

        with open(os.path.join(text_dir, "source_transcript.txt"), "w", encoding="utf-8") as f:
            f.write(transcript_text)

        #romanian translation
        print("Task: Generating romanian translation...")
        with open(os.path.join(text_dir, "ro_translation.txt"), "w", encoding="utf-8") as f:
            f.write(f"[RO STUB]: {transcript_text[:100]}...")

        print("Task: Creating AI voiceover stub...")
        open(os.path.join(audio_dir, "ro_dub_synthetic.aac"), 'a').close()#create empty file

        print("Step 4 Complete")
        self.mediator.on_event(Event.AUDIO_TEXT_DONE)#mark finished