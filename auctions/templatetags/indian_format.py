from django import template

register = template.Library()

def indian_currency(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value
    s = str(int(value))
    if len(s) > 3:
        last3 = s[-3:]
        rest = s[:-3]
        # Group by 2 from the right
        rest = ','.join([rest[max(i-2,0):i] for i in range(len(rest), 0, -2)][::-1]).lstrip(',')
        formatted = rest + ',' + last3
    else:
        formatted = s
    decimals = f"{value:.2f}".split('.')[-1]
    return f"{formatted}.{decimals}"

register.filter('indian_currency', indian_currency) 