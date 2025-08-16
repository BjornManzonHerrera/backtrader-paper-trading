
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt


class MyStrategy(bt.Strategy):
    params = dict(
        # Add your strategy parameters here
    )

    def __init__(self):
        # Add your indicators and other logic here
        pass

    def next(self):
        # Implement your trading logic here
        pass

def runstrategy():
    args = parse_args()

    cerebro = bt.Cerebro()

    # Add your strategy
    cerebro.addstrategy(MyStrategy)

    # Set up the broker
    if args.broker == 'ib':
        store = bt.stores.IBStore(
            host=args.host,
            port=args.port,
            clientId=args.clientId
        )
        broker = store.getbroker()
        cerebro.setbroker(broker)
        data = store.getdata(dataname=args.data0)
    elif args.broker == 'oanda':
        store = bt.stores.OandaStore(
            token=args.token,
            account=args.account,
            practice=not args.live
        )
        broker = store.getbroker()
        cerebro.setbroker(broker)
        data = store.getdata(dataname=args.data0)
    else:
        # Add other brokers here
        raise ValueError('Broker not supported')

    cerebro.adddata(data)

    # Run the strategy
    cerebro.run()


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Paper Trading with backtrader')

    parser.add_argument('--broker', default='ib',
                        choices=['ib', 'oanda'],
                        help='Broker to use')

    # Add arguments for your chosen broker
    # Interactive Brokers arguments
    parser.add_argument('--host', default='127.0.0.1',
                        help='Host for the Interactive Brokers TWS Connection')
    parser.add_argument('--port', default=7496, type=int,
                        help='Port for the Interactive Brokers TWS Connection')
    parser.add_argument('--clientId', default=None, type=int,
                        help='Client Id to connect to TWS (default: random)')

    # Oanda arguments
    parser.add_argument('--token', default=None,
                        help='Access token to use')
    parser.add_argument('--account', default=None,
                        help='Account identifier to use')
    parser.add_argument('--live', action='store_true',
                        help='Go to live server rather than practice')

    parser.add_argument('--data0', default=None,
                        required=True, action='store',
                        help='data into the system')

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    runstrategy()
