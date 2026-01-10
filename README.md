# TripPlannerLite

## TripPlannerLite — MVP

TripPlannerLite — это Telegram-бот для генерации кратких туристических маршрутов на основе города, дат и типа отдыха.

### Возможности MVP
- Парсинг свободного текстового ввода пользователя
- Валидация дат и параметров поездки
- Подтягивание реальных POI из OpenStreetMap
- Учет прогноза погоды при выборе активностей
- Генерация маршрута по дням (утро / день / вечер)
- Человекочитаемый вывод через LLM
- Telegram-интерфейс

### Архитектура
Telegram Bot → Parser → Itinerary Generator → Weather → LLM → Telegram

### Технологии
- Python 3.11
- FastAPI
- python-telegram-bot
- OpenStreetMap (Nominatim, Overpass)
- Open-Meteo
- OpenAI API
- GitHub + VS Code

### Статус
MVP готов к демонстрации и защите.
