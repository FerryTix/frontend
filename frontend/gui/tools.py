def format_amount(amount: int) -> str:
    amount_str = str(amount).zfill(3)
    return f'{amount_str[:-2]},{amount_str[-2:]} €'
