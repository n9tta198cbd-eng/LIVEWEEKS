# Исправление ошибки 404 NOT_FOUND на Vercel

## Проблема
Vercel возвращает 404 при обращении к `/api/generate`.

## Решения

### 1. Упрощенная конфигурация vercel.json
Vercel автоматически создает маршруты для файлов в папке `api/`. 
Файл `api/generate.py` автоматически становится доступным по адресу `/api/generate`.

Убрал `routes` из `vercel.json`, оставил только `rewrites` для статических файлов.

### 2. Проверьте структуру проекта
Убедитесь, что структура такая:
```
.
├── api/
│   └── generate.py  ← должен быть здесь
├── requirements.txt
├── vercel.json
└── src/
    └── ...
```

### 3. Проверьте URL
После деплоя API должен быть доступен по адресу:
- `https://mainllac.vercel.app/api/generate?type=life&birth=2009-08-01&lifes=90`

**Важно:** URL должен быть `/api/generate`, а не `/api/generate.py`

### 4. Передеплойте проект
После изменений в `vercel.json`:
1. Задеплойте заново: `vercel --prod` или через Git push
2. Дождитесь завершения деплоя
3. Проверьте URL

### 5. Проверьте логи
В Vercel Dashboard → Deployments → выберите деплой → Functions
Должна быть функция `api/generate.py`

## Если все еще не работает

Попробуйте добавить обработку OPTIONS для CORS:
```python
def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    self.end_headers()
```
