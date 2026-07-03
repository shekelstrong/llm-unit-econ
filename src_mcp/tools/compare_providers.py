"""compare_providers: сравнение провайдеров LLM."""


# База провайдеров
PROVIDERS = [
    {"name": "anthropic/claude-3.5-sonnet", "cost_in": 3.0, "cost_out": 15.0, "latency_ms": 1500, "quality": 0.92, "context": 200000, "ru_friendly": False},
    {"name": "anthropic/claude-3-haiku", "cost_in": 0.25, "cost_out": 1.25, "latency_ms": 800, "quality": 0.78, "context": 200000, "ru_friendly": False},
    {"name": "openai/gpt-4o", "cost_in": 2.5, "cost_out": 10.0, "latency_ms": 1200, "quality": 0.91, "context": 128000, "ru_friendly": False},
    {"name": "openai/gpt-4o-mini", "cost_in": 0.15, "cost_out": 0.6, "latency_ms": 700, "quality": 0.82, "context": 128000, "ru_friendly": False},
    {"name": "google/gemini-2.5-pro", "cost_in": 1.25, "cost_out": 5.0, "latency_ms": 1400, "quality": 0.89, "context": 1000000, "ru_friendly": False},
    {"name": "google/gemini-2.5-flash", "cost_in": 0.075, "cost_out": 0.3, "latency_ms": 600, "quality": 0.80, "context": 1000000, "ru_friendly": False},
    {"name": "deepseek/deepseek-chat", "cost_in": 0.14, "cost_out": 0.28, "latency_ms": 900, "quality": 0.83, "context": 32000, "ru_friendly": True},
    {"name": "yandex/yandexgpt", "cost_in": 0.20, "cost_out": 0.60, "latency_ms": 1100, "quality": 0.80, "context": 8000, "ru_friendly": True},
    {"name": "gigachat/gigachat-pro", "cost_in": 0.15, "cost_out": 0.45, "latency_ms": 1000, "quality": 0.78, "context": 32000, "ru_friendly": True},
]


async def run(use_case: str = "general") -> dict:
    """Сравнивает провайдеров.

    Args:
        use_case: general / russian / budget / quality.

    Returns:
        Словарь с рейтингом.
    """
    # Фильтрация по use case
    if use_case == "russian":
        providers = [p for p in PROVIDERS if p["ru_friendly"]]
    else:
        providers = list(PROVIDERS)

    # Сортировка по use case
    if use_case == "budget":
        providers.sort(key=lambda p: p["cost_in"] + p["cost_out"])
    elif use_case == "quality":
        providers.sort(key=lambda p: -p["quality"])
    elif use_case == "fast":
        providers.sort(key=lambda p: p["latency_ms"])
    elif use_case == "ru_friendly":
        providers.sort(key=lambda p: -(p["quality"] / ((p["cost_in"] + p["cost_out"]) + 1)))
    else:  # general
        providers.sort(key=lambda p: -(p["quality"] / ((p["cost_in"] + p["cost_out"]) / 10 + p["latency_ms"] / 1000)))

    return {
        "use_case": use_case,
        "providers": providers,
        "recommendation": providers[0] if providers else None,
    }
