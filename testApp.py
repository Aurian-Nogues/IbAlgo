#//////////////////////////////////////////////////////////////////////////////////////////////////
import sys
#This will only work for windows and default install PATH, update as needed if moving to linux server
sys.path.insert(1, 'C:\TWS API\source\pythonclient')
#//////////////////////////////////////////////////////////////////////////////////////////////////

import datetime

import logging
import time
import os.path

from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract

#/////////////////////Setup logger//////////////////
def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)

#////////Overried callback functions here////////////////////////
class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')


#/////////////////Main program/////////////////////////
def main():
    SetupLogger()
    logging.debug("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.ERROR)

    app = TestApp()

    #/////Connect//////
    app.connect("127.0.0.1", 7497, clientId=0)
     print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))

    #define first contract and send request
    contract_1 = Contract()
    contract_1.symbol = "AAPL"
    contract_1.secType = "STK"
    contract_1.exchange = "SMART"
    contract_1.currency = "USD"
    contract_1.primaryExchange = "NASDAQ"

    app.reqMarketDataType(1) # switch to delayed-frozen data if live is not available
    #request market data snapshot, will be returned through tickPrice and tickSize events
    #4th arg = True means we request snapshot. If set to false will stream data until cancelled
    app.reqMktData(1, contract_1, "", True, False, [])

    #////////client run//////
    app.run()


    #TODO: request data for second contract

    #TODO: measure spread

    #TODO: trade if required

    #TODO measure spread

    #TODO: close if hitting liquidation tgt or stop loss
    


if __name__ == "__main__":
    main()