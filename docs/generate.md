# Документация к сервисам src/utils/generate

## TranslateGenerate

**Описание:** Класс `TranslateGenerate` предназначен для перевода английского текста на родной язык пользователя.

**Принимает:**
- `tg_id` (строка): Телеграм-идентификатор пользователя.
- `en_string` (строка): Текст на английском, который требуется перевести на родной язык.

**Методы:**
### `translate() -> str` 
При вызове возвращает переведенный английский текст на родной язык пользователя.

**Пример использования:**
```python
await TranslateGenerate(tg_id="tg_id", en_string="Hello world").translate()
```

**Возвращаемое значение:** Cтрока


## CommunicationGenerate

**Описание:** Класс CommunicationGenerate предназначен для взаимодействия с сервисом OpenAI с целью генерации текста на основе истории сообщений пользователя.

**Принимает:**

-  `tg_id` (строка): Идентификатор пользователя в Telegram.
- `prompt` (строка): Начальное сообщение (подсказка) для генерации текста.
- `user_message_history` (GetUserMessageHistory): Объект, представляющий историю сообщений пользователя.

**Методы:**

### `generate_message() -> str`
Вызывается для получения сгенерированного текста на основе истории сообщений пользователя.

### `get_combine_data() -> json`
Вызывается для получения словаря данных (json) для передачи в запрос OpenAI.

### `get_user_message_history_with_service_text_request_and_prompt() -> GetUserMessageHistory`
Вызывается для обновления объекта истории сообщений пользователя, включая системное сообщение с информацией о пользователе и промт.

**Пример использования:**
```python
await CommunicationGenerate(tg_id="tg_id", prompt="Hello world", user_message_history=user_history).generate_message()
```

**Возвращаемое значение:** Строка 