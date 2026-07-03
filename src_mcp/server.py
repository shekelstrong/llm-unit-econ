"""LLM Unit Economics MCP Server."""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src_mcp.tools import calc_token_cost, calc_unit_margin, calc_break_even, compare_providers, generate_pricing


app = Server("llm-unit-econ")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calc_token_cost",
            description="Стоимость запроса: input/output tokens × price per 1M tokens. Возвращает USD и RUB.",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "input_tokens": {"type": "integer"},
                    "output_tokens": {"type": "integer"},
                },
                "required": ["model", "input_tokens", "output_tokens"],
            },
        ),
        Tool(
            name="calc_unit_margin",
            description="Gross margin: revenue - LLM costs. ROI на LLM-внедрение.",
            inputSchema={
                "type": "object",
                "properties": {
                    "monthly_revenue_rub": {"type": "integer"},
                    "monthly_llm_cost_rub": {"type": "integer"},
                    "monthly_fixed_cost_rub": {"type": "integer", "default": 0},
                },
                "required": ["monthly_revenue_rub", "monthly_llm_cost_rub"],
            },
        ),
        Tool(
            name="calc_break_even",
            description="Break-even: сколько юзеров нужно чтобы выйти в 0.",
            inputSchema={
                "type": "object",
                "properties": {
                    "price_per_user_rub": {"type": "integer"},
                    "llm_cost_per_user_rub": {"type": "integer"},
                    "fixed_cost_rub": {"type": "integer"},
                },
                "required": ["price_per_user_rub", "llm_cost_per_user_rub", "fixed_cost_rub"],
            },
        ),
        Tool(
            name="compare_providers",
            description="Сравнение провайдеров: cost per 1M tokens, latency, quality.",
            inputSchema={
                "type": "object",
                "properties": {
                    "use_case": {"type": "string", "default": "general"},
                },
            },
        ),
        Tool(
            name="generate_pricing",
            description="Генерация pricing table для landing page (3 тарифа с LLM-cost breakdown).",
            inputSchema={
                "type": "object",
                "properties": {
                    "tiers": {"type": "array", "items": {"type": "object"}},
                    "currency": {"type": "string", "default": "RUB"},
                },
                "required": ["tiers"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    import json
    tools_map = {
        "calc_token_cost": calc_token_cost,
        "calc_unit_margin": calc_unit_margin,
        "calc_break_even": calc_break_even,
        "compare_providers": compare_providers,
        "generate_pricing": generate_pricing,
    }
    try:
        result = await tools_map[name].run(**arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {type(e).__name__}: {e}")]


async def main():
    async with stdio_server() as (rs, ws):
        await app.run(rs, ws, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
