import logging
import os
import subprocess
import tempfile
from enum import Enum
from io import BytesIO



class ConversionType(Enum):
    Mp3ToOgg = 1


class AudioConverterCash:
    def __init__(self, audio_files, mode=ConversionType.Mp3ToOgg):
        self.output_files = {}
        self.audio_files = audio_files
        self.mode = mode


    def convert_files_to_ogg(self):
        print("CALL CASH")
        output_directory = 'files/newsletter_voices'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        converted_files = []

        try:
            for variable_name, audio_bytes in self.audio_files.items():
                input_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
                try:
                    # Создаем файлоподобный объект BytesIO из байтов аудио
                    input_file.write(audio_bytes.read())

                    output_file_path = os.path.join(output_directory, f'{variable_name}.ogg')
                    # Вызываем ffmpeg, передавая байты аудио через stdin
                    subprocess.run(
                        ['ffmpeg', '-y', '-i', f'{input_file.name}', '-c:a', 'libopus', output_file_path],
                        check=True,
                        capture_output=False
                    )
                    converted_files.append(output_file_path)
                    self.output_files[variable_name] = input_file

                except Exception as e:
                    print(f'ERROR CONVERTER{e}')
                    logging.error(f"ERROR CONVERTER OGG: {e}")
                    raise
                finally:
                    input_file.close()
                    os.unlink(input_file.name)
            return converted_files
        except Exception as e:
            logging.error(f"ERROR CONVERTER OGG: {e}")
            raise
