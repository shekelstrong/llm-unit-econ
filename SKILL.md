---
name: llm-unit-econ
description: Юнит-экономика LLM-продукта. Стоимость токенов (10 моделей), gross/net margin, break-even по юзерам, сравнение провайдеров (Claude/GPT/Gemini/DeepSeek/YandexGPT/GigaChat), генерация pricing table.
---

# LLM Unit Economics

MCP-сервер для расчёта экономики LLM-продукта.

## Когда использовать

- Запускаешь LLM-продукт, считаешь экономику
- Сравниваешь провайдеров (Claude vs GPT vs Gemini vs DeepSeek)
- Определяешь цену подписки
- Считаешь break-even для инвестора
- Делаешь pricing page

## 5 tools

```
запрос → calc_token_cost (USD + RUB)
        ↓
продукт → calc_unit_margin (gross/net)
        ↓
модель → calc_break_even (X юзеров)
        ↓
выбор → compare_providers (9 провайдеров)
        ↓
прайс → generate_pricing (markdown table)
```

## Алгоритм

### 1. calc_token_cost
- 10 моделей с актуальными ценами (USD / 1M tokens)
- Возвращает: cost_input, cost_output, total_usd, total_rub (×95)
- cost_per_1k_requests (если 1000 таких запросов)

### 2. calc_unit_margin
- gross_profit = revenue - LLM
- net_profit = gross - fixed
- gross_margin % / net_margin % / LLM cost %
- Health: excellent / good / warning / critical
- Рекомендации: если LLM > 50% — fallback, кэш, gemini-flash

### 3. calc_break_even
- margin_per_user = price - LLM cost
- break_even_users = fixed / margin
- 5 сценариев: 10 / 50 / 100 / 500 / 1000 юзеров

### 4. compare_providers
9 провайдеров с метриками: cost, latency, quality, context, RU-friendly.
Фильтр по use_case: general / russian / budget / quality / fast.

### 5. generate_pricing
Markdown таблица из tiers.

## Pitfalls

| Ошибка | Последствие | Как избежать |
|---|---|---|
| Не учитывать output tokens | 5x недооценка расходов | Output обычно 3-5x дороже input |
| Курс доллара захардкожен | При падении рубля margin падает | Используй API ЦБ |
| Без fallback chain | Падение Claude = downtime | Добавь Gemini Flash как fallback |
| Один провайдер | Vendor lock | Минимум 2 провайдера + fallback |
| Claude 3.5 для всего | Дорого | Кэш для повторяющихся запросов |
| Без кэша | Одни и те же вопросы = расход | Redis кэш на 24h |

## Сравнение провайдеров (июль 2026)

| Провайдер | $/1M input | $/1M output | Quality | RU-friendly |
|---|---|---|---|---|
| Claude 3.5 Sonnet | 3.0 | 15.0 | 0.92 | ❌ |
| GPT-4o | 2.5 | 10.0 | 0.91 | ❌ |
| Gemini 2.5 Pro | 1.25 | 5.0 | 0.89 | ❌ |
| Gemini 2.5 Flash | 0.075 | 0.3 | 0.80 | ❌ |
| DeepSeek | 0.14 | 0.28 | 0.83 | ✅ |
| GigaChat Pro | 0.15 | 0.45 | 0.78 | ✅ |
| YandexGPT | 0.20 | 0.60 | 0.80 | ✅ |

**Рекомендация для РФ:** Claude для качественных задач, DeepSeek/GigaChat для бюджета, YandexGPT для compliance.

## Источники

3 скилла: b2b-llm-unit-economics, b2b-pricing-rounding-and-precision, llm-inference-ops.
