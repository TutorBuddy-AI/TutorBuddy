import logging
import subprocess
import tempfile
from enum import Enum
from io import BytesIO

from pydub import AudioSegment


class ConversionType(Enum):
    Mp3ToOgg = 1


class AudioConverter:
    def __init__(self, audio_bytes: BytesIO, mode=ConversionType.Mp3ToOgg):
        self.output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg')
        self.audio_bytes = audio_bytes
        self.mode = mode

    def __enter__(self):
        if self.mode is ConversionType.Mp3ToOgg:
            return self.convert_bytes_to_ogg()
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.output_file.close()

    def convert_bytes_to_ogg(self):
        input_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
        try:
            # Создаем файлоподобный объект BytesIO из байтов аудио
            input_file.write(self.audio_bytes.read())
            # Вызываем ffmpeg, передавая байты аудио через stdin
            subprocess.run(
                ['ffmpeg', '-y', '-i', f'{input_file.name}', '-c:a', 'libopus', f'{self.output_file.name}'],
                check=True
            )
            return self.output_file.name
        except Exception as e:
            logging.error(f"ERROR CONVERTER OGG: {e}")
            raise
        finally:
            input_file.close()
