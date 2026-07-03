"""generate_pricing: генерация pricing table."""


async def run(tiers: list, currency: str = "RUB") -> dict:
    """Генерирует pricing.

    Args:
        tiers: [{name, price, requests_per_month, features}].
        currency: RUB / USD.

    Returns:
        Markdown таблица + JSON.
    """
    if not tiers:
        return {"error": "tiers required"}

    sym = "₽" if currency == "RUB" else "$"

    md_lines = ["| Тариф | Цена | Запросов/мес | Фичи |", "|---|---|---|---|"]
    for t in tiers:
        md_lines.append(f"| **{t['name']}** | {t['price']} {sym} | {t.get('requests_per_month', '∞')} | {', '.join(t.get('features', []))} |")

    return {
        "format": "markdown",
        "currency": currency,
        "table": "\n".join(md_lines),
        "tiers": tiers,
    }
