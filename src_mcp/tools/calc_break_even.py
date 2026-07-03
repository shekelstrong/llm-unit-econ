"""calc_break_even: точка безубыточности."""


async def run(price_per_user_rub: int, llm_cost_per_user_rub: int, fixed_cost_rub: int) -> dict:
    """Считает break-even.

    Args:
        price_per_user_rub: Цена подписки.
        llm_cost_per_user_rub: LLM-расход на юзера.
        fixed_cost_rub: Постоянные расходы.

    Returns:
        Словарь с break-even.
    """
    margin_per_user = price_per_user_rub - llm_cost_per_user_rub

    if margin_per_user <= 0:
        return {
            "error": f"Цена ({price_per_user_rub}₽) <= LLM ({llm_cost_per_user_rub}₽) на юзера. Невозможно достичь прибыли.",
            "price_per_user_rub": price_per_user_rub,
            "llm_cost_per_user_rub": llm_cost_per_user_rub,
        }

    break_even_users = fixed_cost_rub / margin_per_user

    # С учётом роста
    scenarios = []
    for target_users in [10, 50, 100, 500, 1000]:
        revenue = target_users * price_per_user_rub
        llm = target_users * llm_cost_per_user_rub
        profit = revenue - llm - fixed_cost_rub
        scenarios.append({
            "users": target_users,
            "revenue_rub": revenue,
            "llm_cost_rub": llm,
            "net_profit_rub": profit,
            "profitable": profit > 0,
        })

    return {
        "price_per_user_rub": price_per_user_rub,
        "llm_cost_per_user_rub": llm_cost_per_user_rub,
        "fixed_cost_rub": fixed_cost_rub,
        "margin_per_user_rub": margin_per_user,
        "break_even_users": round(break_even_users, 1),
        "scenarios": scenarios,
    }
