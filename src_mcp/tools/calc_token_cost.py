"""calc_token_cost: стоимость токенов."""


# Цены за 1M tokens (USD), обновлено июль 2026
PRICES = {
    "anthropic/claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
    "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
    "openai/gpt-4o": {"input": 2.5, "output": 10.0},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "google/gemini-2.5-pro": {"input": 1.25, "output": 5.0},
    "google/gemini-2.5-flash": {"input": 0.075, "output": 0.3},
    "meta-llama/llama-3.1-70b-instruct": {"input": 0.59, "output": 0.79},
    "deepseek/deepseek-chat": {"input": 0.14, "output": 0.28},
    "yandex/yandexgpt": {"input": 0.20, "output": 0.60},
    "gigachat/gigachat-pro": {"input": 0.15, "output": 0.45},
}


async def run(model: str, input_tokens: int, output_tokens: int) -> dict:
    """Считает стоимость.

    Args:
        model: Модель.
        input_tokens: Кол-во input токенов.
        output_tokens: Кол-во output токенов.

    Returns:
        Словарь со стоимостью.
    """
    prices = PRICES.get(model)
    if not prices:
        return {"error": f"Unknown model: {model}", "available": list(PRICES.keys())}

    cost_in = (input_tokens / 1_000_000) * prices["input"]
    cost_out = (output_tokens / 1_000_000) * prices["output"]
    total = cost_in + cost_out

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost_input_usd": round(cost_in, 6),
        "cost_output_usd": round(cost_out, 6),
        "total_usd": round(total, 6),
        "total_rub": round(total * 95),  # ~95₽/$
        "price_per_1m": prices,
        "cost_per_1k_requests": round(total * 1000, 2) if total > 0 else 0,  # если 1k таких запросов
    }
