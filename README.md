# PumpSwap

PumpSwap is a Python module for interacting with Solana's Pump.fun tokens.
Automatically build instructions for your transaction, or simply use built-in functions to make Pump.fun swaps.

More information here: https://github.com/FLOCK4H/pump_swap

## Usage

Example script:

```

from pump_swap import PumpSwap, usd_to_lamports, lamports_to_tokens, usd_to_microlamports
from decimal import Decimal
import asyncio, aiohttp, json

PRIV_KEY = ""
WALLET = ""
STAKED_API = "" # e.g. staked helius

# Create a PumpSwap object
async def main():
    session = aiohttp.ClientSession()
    priv_key = PRIV_KEY # str
    rpc_endpoint = STAKED_API # str
    debug = True

    pump_swap = PumpSwap(session=session, priv_key=priv_key, rpc_endpoint=rpc_endpoint, debug=debug)
    solana_price = pump_swap.get_solana_price_usd()
    solana_price = Decimal(solana_price)

    mint_address = "2MWw9bXmevKxuof49uRFb59dAaFAtAydsrXzR4jNpump"
    bonding_curve, ass_bonding_curve = await pump_swap.get_bonding_curve_pda(mint_address)
    token_price = Decimal("0.0000000280") # Token price can be calculated using vsr/vtr formula.

    amount = input("Enter the amount of USD to spend: ")
    sol_to_spend = await usd_to_lamports(int(amount.strip()), solana_price)
    sol_to_tokens = await lamports_to_tokens(sol_to_spend, token_price)

    should_simulate = False
    fee = await usd_to_microlamports(0.1, solana_price, 50_000) # 0.1$ per 50k compute units

    buy_sig = await pump_swap.pump_buy(
        mint_address=mint_address,
        bonding_curve_pda=bonding_curve,
        sol_amount=sol_to_spend,
        token_amount=sol_to_tokens,
        sim=should_simulate,
        priority_micro_lamports=fee,
        slippage=1.5 # e.g. 50% slippage
    )

    # Here we get signature of the transaction
    result_json = buy_sig.to_json()
    transaction_id = json.loads(result_json).get('result')
    print("Buy: ", transaction_id)
    # Then we can use it to verify if we got success
    verify = await pump_swap.getTransaction(transaction_id, session)
    print(f"{json.dumps(verify, indent=2)}")

    await asyncio.sleep(5)

    sell_sig = await pump_swap.pump_sell(
        mint_address=mint_address,
        bonding_curve_pda=bonding_curve,
        token_amount=sol_to_tokens,
        sim=should_simulate,
        priority_micro_lamports=fee,
    )

    result_json = sell_sig.to_json()
    transaction_id = json.loads(result_json).get('result')
    print("Sell: ", transaction_id)

    verify = await pump_swap.getTransaction(transaction_id, session)
    print(f"{json.dumps(verify, indent=2)}")

    # Close all instances when done
    await pump_swap.close()

if __name__ == "__main__":
    asyncio.run(main())

```

## Features
- Create, sign, and send Solana transactions for Pump.fun tokens.
- Fetch wallet balances and Solana price in USD.
- Automatically derive bonding curve and associated token addresses.
- Utility functions for converting USD to lamports and tokens.

## Installation
Install via pip:

```bash

pip install pump_swap

```