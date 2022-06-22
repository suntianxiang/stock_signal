from bot.strategies.right import PriceReverse
from bot.strategies.left import BollStoch


def strategy_fatory(name):
    match name:
        case 'PriceReverse':
            return PriceReverse()
        case 'BollStoch':
            return BollStoch()
