# Инструкция по деплою на Vercel

## Структура проекта для Vercel

Для правильной работы на Vercel структура должна быть следующей:

```
.
├── vercel.json          # Конфигурация Vercel
├── requirements.txt     # Python зависимости
├── api/
│   └── generate.py     # Python Serverless Function
└── src/                 # Статические файлы
    ├── index.html
    ├── script.js
    ├── style.css
    ├── img/
    └── fonts/
```

## Шаги деплоя

1. **Проверьте структуру файлов:**
   - `api/generate.py` должен быть в папке `api/` в корне проекта (не в `src/api/`)
   - `vercel.json` должен быть в корне проекта
   - `requirements.txt` должен быть в корне проекта

2. **Если файл находится в `src/api/generate.py`:**
   - Переместите его в `api/generate.py` (в корне проекта)
   - Или обновите `vercel.json` чтобы указать правильный путь

3. **Настройте домен:**
   - В Vercel Dashboard → Settings → Domains
   - Добавьте домен: `mainllac.vercel.app`
   - Убедитесь, что он установлен как Primary Domain

4. **Деплой:**
   ```bash
   vercel --prod
   ```
   Или через GitHub/GitLab интеграцию

## Проверка работы

После деплоя проверьте:
- `https://mainllac.vercel.app/` - главная страница
- `https://mainllac.vercel.app/api/generate?type=life&birth=2009-08-01&lifes=90` - API

## Возможные проблемы

1. **404 на API:** Проверьте, что файл `api/generate.py` находится в правильной папке
2. **Ошибка импорта:** Убедитесь, что `requirements.txt` содержит `Pillow`
3. **Домен не работает:** Проверьте настройки домена в Vercel Dashboard
