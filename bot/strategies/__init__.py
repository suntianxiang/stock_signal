from bot.strategies.right import CERSI, EMACross, DMICross
from bot.strategies.left import BollStoch, MACDCross


def strategy_factory(name):
    match name:
        case 'EMACross':
            return EMACross()
        case 'BollStoch':
            return BollStoch()
        case 'MACDCross':
            return MACDCross()
        case 'DMICross':
            return DMICross()
        case 'CERSI':
            return CERSI()
