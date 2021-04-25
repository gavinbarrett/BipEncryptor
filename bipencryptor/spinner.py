import asyncio

async def alter_sym(sym):
	if sym == "-":
		return "\\"
	elif sym == "\\":
		return "|"
	elif sym == "|":
		return "/"
	elif sym == "/":
		return "-"

async def print_out(sym):
	print(f'Stretching key...{sym}', end="\r")

async def spinner():
	sym = "-"
	while True:
		await print_out(sym)
		sym = await alter_sym(sym)
