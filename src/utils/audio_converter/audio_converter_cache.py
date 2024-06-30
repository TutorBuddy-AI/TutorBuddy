import logging
import os
import subprocess
import tempfile
from enum import Enum
from io import BytesIO
from typing import Dict, Any


class ConversionType(Enum):
    Mp3ToOgg = 1


class AudioConverterCache:
    def __init__(self, audio, mode=ConversionType.Mp3ToOgg):
        self.output_files = {}
        self.audio = audio
        self.mode = mode
        self.temp_files = []

    def convert_audio_to_ogg_fixed_files(self, filepaths: dict[str, str]) -> dict[Any, str]:
        temp_directory = tempfile.mkdtemp()
        converted_files = {}

        try:
            for variable_name, audio_bytes in self.audio.items():
                input_file = tempfile.NamedTemporaryFile(dir=temp_directory, delete=False)
                try:
                    # Создаем файлоподобный объект BytesIO из байтов аудио
                    input_file.write(audio_bytes.read())

                    output_file_path = filepaths[variable_name]
                    # Вызываем ffmpeg, передавая байты аудио через stdin
                    subprocess.run(
                        ['ffmpeg', '-y', '-loglevel', 'quiet', '-i', f'{input_file.name}', '-c:a', 'libopus', output_file_path],
                        check=True,
                        capture_output=False
                    )
                    converted_files[variable_name] = output_file_path
                    self.output_files[variable_name] = input_file

                except Exception as e:
                    logging.error(f"ERROR CONVERTER OGG: {e}")
                    raise
                finally:
                    input_file.close()
                    os.unlink(input_file.name)
            return converted_files
        except Exception as e:
            logging.error(f"ERROR CONVERTER OGG: {e}")
            raise

    def convert_audio_to_ogg(self) -> dict[Any, str]:
        temp_directory = tempfile.mkdtemp()
        converted_files = {}

        try:
            for variable_name, audio_bytes in self.audio.items():
                input_file = tempfile.NamedTemporaryFile(dir=temp_directory, delete=False)
                try:
                    # Создаем файлоподобный объект BytesIO из байтов аудио
                    input_file.write(audio_bytes.read())

                    output_file_path = os.path.join(temp_directory, f'{variable_name}.ogg')
                    # Вызываем ffmpeg, передавая байты аудио через stdin
                    subprocess.run(
                        ['ffmpeg', '-y', '-loglevel', 'quiet', '-i', f'{input_file.name}', '-c:a', 'libopus', output_file_path],
                        check=True,
                        capture_output=False
                    )
                    converted_files[variable_name] = output_file_path
                    self.output_files[variable_name] = input_file

                except Exception as e:
                    logging.error(f"ERROR CONVERTER OGG: {e}")
                    raise
                finally:
                    input_file.close()
                    os.unlink(input_file.name)
            return converted_files
        except Exception as e:
            logging.error(f"ERROR CONVERTER OGG: {e}")
            raise