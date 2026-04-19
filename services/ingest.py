import os
from services.base import Processor
from core.states import Event
import hashlib
import json
class IngestService(Processor):
    def process(self, context):
        input_file = context.get("input_file")

        print(f"Step 1: Ingest - Initializing for {input_file}...")

        if not os.path.exists(input_file):
            print(f"Ingest step error: File '{input_file}' not found!")
            return # stop the pipeline if the file is missing

        with open(input_file, 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
        with open('checksums.json', 'r') as file:
            data = json.load(file)

        print("Task: Running format validator...")

        if not input_file.lower().endswith(('.mp4', '.mkv', '.mov')):
            print("Ingest step error: File format does not match studio accepted formats!")
            return
        print(f"Ingest: File format of '{input_file}' matches studio accepted formats.")
        print("Task: Performing integrity checksums...")

        check = False
        for item in data:
            if item['filename'] == os.path.basename(input_file):
                if item['md5'] == md5_returned:
                    print(f"Ingest: Checksum for '{input_file}' is successful.")
                    check = True
                    break
                else:
                    print("Ingest step error: Checksum failed!")
                    return
                    #found the file in the checksum list, but the checksums don't match
        if not check:
            print("Ingest step error: Checksum failed!")
            return

        self.ensure_dir(context['base_path'])

        print(f"Step 1 Complete: {input_file} is ready for processing.")
        self.mediator.on_event(Event.INGEST_DONE)