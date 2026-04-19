import subprocess
import os
import json
from services.base import Processor
from core.states import Event


class VisualsService(Processor):
    def process(self, context):
        input_file = context.get("input_file")
        base_path = context.get("base_path")

        print("Step 3: Visuals - Starting processing pipeline...")

        #basically check for bs instagram reels jumpscares
        print(f"Task: Analyzing {input_file} complexity with ffprobe...")
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=bit_rate", "-of", "json", input_file
        ]

        # probe and extract bitrate
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        probe_data = json.loads(result.stdout)
        # if bitrate is not available, we default to 5Mbps
        source_bitrate = int(probe_data['streams'][0].get('bit_rate', 5000000))
        print(f"ffprobe: Detected source bitrate {source_bitrate // 1000}kbps.")

        # required extesnsions and resoulutions for each codec
        targets = [
            {"codec": "h264", "ext": "mp4", "encoder": "libx264",
             "res": {"4k": "3840:2160", "1080p": "1920:1080", "720p": "1280:720"}},
            {"codec": "vp9", "ext": "webm", "encoder": "libvpx-vp9",
             "res": {"4k": "3840:2160", "1080p": "1920:1080", "720p": "1280:720"}},
            {"codec": "hevc", "ext": "mkv", "encoder": "libx265",
             "res": {"4k": "3840:2160", "1080p": "1920:1080", "720p": "1280:720"}}
        ]

        for target in targets:
            codec_dir = os.path.join(base_path, "video", target['codec'])
            self.ensure_dir(codec_dir)

            for label, scale in target['res'].items():
                output_path = os.path.join(codec_dir, f"{label}_{target['codec']}.{target['ext']}")

                # bitratea adjustment based on the resolution
                target_bitrate = source_bitrate if "4k" in label else source_bitrate // 2 if "1080p" in label else source_bitrate // 4

                cmd = [
                    "ffmpeg", "-y", "-i", input_file,
                    "-vf", f"scale={scale}",
                    "-c:v", target['encoder'],
                    "-b:v", str(target_bitrate),
                    "-preset",
                    "ultrafast",
                    #"-t", "5",
                    #uncomment the above line to process just 5 seconds of the file duration, uncomment 2 lines above to process at normal speed

                    output_path
                ]
                print(f"Transcoding: {output_path} at {target_bitrate // 1000}kbps")
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        #sprite map and thumbnails
        print("Task: Gen filmstrip and thumbnails...")
        img_dir = os.path.join(base_path, "images")
        thumb_dir = os.path.join(img_dir, "thumbnails")
        self.ensure_dir(thumb_dir)

        # Sprite Map (Filmstrip)
        sprite_cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-vf", "fps=1,scale=160:-1,tile=5x1",
            os.path.join(img_dir, "sprite_map.jpg")
        ]
        subprocess.run(sprite_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Periodic Keyframes (Thumbnails)
        thumb_cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-vf", "fps=1/2,scale=320:-1",  # One thumbnail every 2 seconds [cite: 51]
            os.path.join(thumb_dir, "thumb_%03d.jpg")
        ]
        subprocess.run(thumb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("Step 3 Complete: All visual assets generated.")
        self.mediator.on_event(Event.VISUALS_DONE)