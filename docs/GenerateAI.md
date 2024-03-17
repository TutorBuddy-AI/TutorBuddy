## GenerateAI

Для использования данного класса требуется наличие корректных данных OPENAI_API и PROXY из конфигурационного файла.


**Описание:** Класс `GenerateAI` предназначен для взаимодействия с OpenAI API и выполнения запросов на генерацию текста и преобразование речи в текст.

**Принимает:**
- `request_url` (строка): Пример `https://api.openai.com/v1/chat/completions`

**Методы:**
### `send_request(payload: Any) -> Any`
Отправляет запрос на генерацию текста к OpenAI API

**Параметры и аргументы:**
- `payload` (любой): Данные для генерации текста.

**Пример использования:**

```python
await GenerateAI(request_url="https://api.openai.com/v1/chat/completions").request_gpt(payload={"prompt": "Hello"})
```
**Возвращаемое значение:** Любой


### `send_request_speech_to_text(audio_bytes: io.BytesIO, model: str) -> str` 
Отправляет запрос на преобразование речи в текст к OpenAI API.

**Параметры и аргументы:** 
- `audio_bytes` (io.BytesIO): Байтовый поток аудио данных.
- `model` (строка): Модель для преобразования речи.

**Пример использования:**

```python
await GenerateAI(request_url="https://api.openai.com/v1/chat/completions").generator.send_form(audio_bytes=audio_data,
                                                                                               model="model")
```
**Возвращаемое значение:** Текст, полученный в результате преобразования речи в текст.

