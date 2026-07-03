"""calc_unit_margin: gross margin."""


async def run(monthly_revenue_rub: int, monthly_llm_cost_rub: int, monthly_fixed_cost_rub: int = 0) -> dict:
    """Считает маржу.

    Args:
        monthly_revenue_rub: Выручка.
        monthly_llm_cost_rub: LLM.
        monthly_fixed_cost_rub: VPS/Supabase/etc.

    Returns:
        Словарь с margin.
    """
    gross = monthly_revenue_rub - monthly_llm_cost_rub
    net = gross - monthly_fixed_cost_rub
    gross_margin = (gross / monthly_revenue_rub * 100) if monthly_revenue_rub else 0
    net_margin = (net / monthly_revenue_rub * 100) if monthly_revenue_rub else 0

    health = "excellent" if net_margin > 50 else "good" if net_margin > 25 else "warning" if net_margin > 0 else "critical"

    recs = []
    llm_pct = (monthly_llm_cost_rub / monthly_revenue_rub * 100) if monthly_revenue_rub else 0
    if llm_pct > 50:
        recs.append("⚠️ LLM > 50% выручки — нужен fallback на дешёвые модели или кэш")
    if net_margin < 30:
        recs.append("💰 Net margin < 30% — подними цену или сократи fixed costs")
    if net_margin > 60:
        recs.append("🟢 Отличная экономика — масштабируй!")

    return {
        "monthly_revenue_rub": monthly_revenue_rub,
        "monthly_llm_cost_rub": monthly_llm_cost_rub,
        "monthly_fixed_cost_rub": monthly_fixed_cost_rub,
        "gross_profit_rub": gross,
        "net_profit_rub": net,
        "gross_margin_pct": round(gross_margin, 1),
        "net_margin_pct": round(net_margin, 1),
        "llm_cost_pct": round(llm_pct, 1),
        "health": health,
        "recommendations": recs,
    }
