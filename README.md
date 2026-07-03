# llm-unit-econ

> MCP-сервер для расчёта юнит-экономики LLM-продукта: стоимость токенов, gross margin, break-even, сравнение провайдеров, генерация pricing.

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)

## 🎯 Что это

MCP-сервер с 5 инструментами для LLM-экономики:

- 💰 **calc_token_cost** — стоимость запроса (USD + RUB)
- 📊 **calc_unit_margin** — gross/net margin, LLM cost %
- 📈 **calc_break_even** — сколько юзеров для 0
- 🆚 **compare_providers** — 9 провайдеров с фильтром по use case
- 💳 **generate_pricing** — pricing table (markdown)

## 📦 Установка

```bash
git clone https://github.com/shekelstrong/llm-unit-econ.git
cd llm-unit-econ
pip install -r requirements.txt
```

## 🛠 MCP Tools

### calc_token_cost
```python
result = await calc_token_cost.run("anthropic/claude-3.5-sonnet", 1500, 500)
# → {total_usd: 0.012, total_rub: 1.14, cost_per_1k_requests: 12.0}
```

10 моделей: Claude 3.5 Sonnet/Haiku, GPT-4o/mini, Gemini 2.5 Pro/Flash, Llama 3.1, DeepSeek, YandexGPT, GigaChat.

### calc_unit_margin
```python
result = await calc_unit_margin.run(100000, 15000, 20000)
# → {gross_margin_pct: 85.0, net_margin_pct: 65.0, health: "excellent"}
```

### calc_break_even
```python
result = await calc_break_even.run(price_per_user_rub=1000, llm_cost_per_user_rub=200, fixed_cost_rub=20000)
# → {break_even_users: 25.0, scenarios: [...]}
```

### compare_providers
```python
result = await compare_providers.run("russian")  # или "budget", "quality", "fast"
# → {providers: [...], recommendation: {...}}
```

### generate_pricing
```python
result = await generate_pricing.run([
    {"name": "Starter", "price": 990, "requests_per_month": 1000, "features": ["email support"]},
    {"name": "Pro", "price": 4990, "requests_per_month": 10000, "features": ["priority support", "API"]},
], currency="RUB")
# → {table: "| Тариф | Цена | ...", tiers}
```

## 📁 Структура

```
llm-unit-econ/
├── README.md
├── LICENSE
├── SKILL.md
├── requirements.txt
├── src_mcp/
│   ├── server.py
│   └── tools/
│       ├── calc_token_cost.py
│       ├── calc_unit_margin.py
│       ├── calc_break_even.py
│       ├── compare_providers.py
│       └── generate_pricing.py
└── .github/workflows/ci.yml
```

## 💰 Сравнение провайдеров (input $ / 1M tokens)

| Провайдер | Input | Output | Quality | RU-friendly |
|---|---|---|---|---|
| Claude 3.5 Sonnet | $3.00 | $15.00 | 0.92 | ❌ |
| GPT-4o | $2.50 | $10.00 | 0.91 | ❌ |
| Gemini 2.5 Pro | $1.25 | $5.00 | 0.89 | ❌ |
| Gemini 2.5 Flash | $0.075 | $0.30 | 0.80 | ❌ |
| GPT-4o mini | $0.15 | $0.60 | 0.82 | ❌ |
| DeepSeek | $0.14 | $0.28 | 0.83 | ✅ |
| GigaChat Pro | $0.15 | $0.45 | 0.78 | ✅ |
| YandexGPT | $0.20 | $0.60 | 0.80 | ✅ |
| Claude 3 Haiku | $0.25 | $1.25 | 0.78 | ❌ |

## 📄 License

MIT © Vasiliy Nedopekin (shekelstrong)
