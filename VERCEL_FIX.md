# Исправление ошибки ModuleNotFoundError: No module named 'PIL'

## Проблема
Vercel не может найти модуль Pillow при импорте в `api/generate.py`.

## Решение

### Вариант 1: Убедитесь, что requirements.txt в корне проекта
Vercel автоматически устанавливает зависимости из `requirements.txt`, если он находится в **корне проекта**.

Структура должна быть:
```
.
├── requirements.txt  ← должен быть здесь
├── vercel.json
├── api/
│   └── generate.py
└── src/
    └── ...
```

### Вариант 2: Проверьте содержимое requirements.txt
Убедитесь, что файл содержит:
```
Pillow>=9.0.0
```

### Вариант 3: Передеплойте проект
После добавления/изменения `requirements.txt`:
1. Удалите старый деплой в Vercel Dashboard
2. Задеплойте заново через `vercel --prod` или через Git push

### Вариант 4: Проверьте логи сборки
В Vercel Dashboard → Deployments → выберите деплой → посмотрите Build Logs
Должна быть строка типа: `Installing dependencies from requirements.txt`

### Вариант 5: Используйте более новую версию Python
Попробуйте изменить runtime на python3.12 в vercel.json:
```json
{
  "functions": {
    "api/generate.py": {
      "runtime": "python3.12"
    }
  }
}
```

## Проверка
После деплоя проверьте:
- `https://mainllac.vercel.app/api/generate?type=life&birth=2009-08-01&lifes=90`
- Должно вернуть изображение PNG, а не ошибку
