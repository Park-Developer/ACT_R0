import Upbit_Trade.config
import threading
import basic_tool
import pandas as pd
import Upbit_Trade.test_tool
import Upbit_Trade.upbit_tool

class Trading_Config(): # SUPER CLASS
    def __init__(self):
        # [1] Config Setting
        self.ticker_currency = Upbit_Trade.config.MARKET_CURRENCY_MATCHING
        self.commission = Upbit_Trade.config.COMMISSION
        self.minimum_trade_cost = Upbit_Trade.config.MINIMUM_TRADING_COST
        self.server_url = Upbit_Trade.config.SERVER_URL

        # [2] Backtest Mode 여부
        self.backtest_mode=False # Default : False

        # [3] Upbit API
        self.UPBIT_access_key=None
        self.UPBIT_secret_key=None

        # [4] User Setting
        self.market=None
        self.period=None
        self.strategy=None
        self.principal=None
        self.bid_unit=None
        self.bid_installment=None
        self.ask_unit=None
        self.ask_installment=None
        self.loss_limit=None
        self.alarm=None
        self.state=None

        # [5] Trading Data
        self.trading_data=[] # trading에 필요한 데이터

        self.KRW_balance=self.principal # 초기화 : 코인예산, 코인을 구매할 수 있는 KRW 잔고
        self.coin_balance=0 # 매수 수량

        self.cur_price=0 # 코인 현재 가격

        self.ref_price = 0 # 매수/매도가 결정을 위한 기준 가격
        self.bid_maxPrice=0 # 최대 매수가격
        self.ask_minPrice=0 # 최소 매도가격

        self.bid_installment_cnt=0 # 분할 매수 횟수
        self.ask_installment_cnt=0 # 분할 매도 횟수

        self.ref_tunning=1 # defalut : 1
        self.bid_tunning=1 # defalut : 1
        self.ask_tunning=1 # defalut : 1

        self.trading_log={}

        self.earning=None
        self.earning_rate=None
        self.today_tradingNum=None
        self.accum_tradingNum=None
        self.end_time=None # start_time은 user setting

        # [6] Test Data
        self.backtest_curPrice=[]
        self.backtest_curPrice_cnt=0

    def load_configData(self,upbit_apiInfo:dict,target_coinInfo:dict):
        # [3] Upbit API
        self.UPBIT_access_key=upbit_apiInfo["upbit_access_key"]
        self.UPBIT_secret_key=upbit_apiInfo["upbit_secret_key"]

        # [4] User Setting
        self.market=target_coinInfo["market"]  # required data
        self.period=target_coinInfo["period"]  # required data
        self.strategy=target_coinInfo["strategy"]  # required data
        self.principal=target_coinInfo["principal"]  # required data * Target Coin에 대한 원금 *
        self.bid_unit=target_coinInfo["bid_unit"] # 힌번에 bidding 가능한 최대 수량
        self.bid_installment=target_coinInfo["bid_installment"]
        self.ask_unit=target_coinInfo["ask_unit"] # 한번에 asking 가능한 최대 수량
        self.ask_installment=target_coinInfo["ask_installment"]
        self.target_earning=target_coinInfo["target_earning"]
        self.loss_limit=target_coinInfo["loss_limit"]
        self.alarm=target_coinInfo["alarm"]
        self.state=target_coinInfo["state"]
        self.start_time =target_coinInfo["start_time"]

    def backtest_modeON(self):
        self.backtest_mode = True

    def backtest_modeOFF(self):
        self.backtest_mode = False

    def reset_tradingData(self):
        # [5] Trading Data
        self.trading_data = {}  # trading에 필요한 데이터

        self.KRW_balance = self.principal  # 초기화 : 코인예산, 코인을 구매할 수 있는 KRW 잔고
        self.coin_balance = 0  # 매수 수량

        self.cur_price = 0  # 코인 현재 가격

        self.ref_price = 0  # 매수/매도가 결정을 위한 기준 가격
        self.bid_maxPrice = 0  # 최대 매수가격
        self.ask_minPrice = 0  # 최소 매도가격

        self.bid_installment_cnt = 0  # 분할 매수 횟수
        self.ask_installment_cnt = 0  # 분할 매도 횟수

        self.ref_tunning = 1  # defalut : 1
        self.bid_tunning = 1  # defalut : 1
        self.ask_tunning = 1  # defalut : 1

        self.trading_log = {}

        self.earning = None
        self.earning_rate = None
        self.today_tradingNum = None
        self.accum_tradingNum = None
        self.end_time = None  # start_time은 user setting

        # [6] Test Data
        self.backtest_curPrice = [] # backtesting 환경에서 사용하는 current price data
        self.backtest_curPrice_cnt = 0

    def get_currentPrice(self):
        # 실제 Trading하는 경우
        if self.backtest_mode==False:
            Upbit_Trade.upbit_tool.request_current_price(market=self.market) # 실시간 현재값 반환

        # Backtesting 모드인 경우
        if self.backtest_mode==True:
            pass

        '''
        def get_backTesting_curPrice(self):
            if self.backtest_curPrice == []:
                print("self,bacTest_curPrice Error!")
            else:
                self.backtest_curPrice_cnt += 1

                return self.backtest_curPrice[self.backtest_curPrice_cnt]
        '''

    def get_user_SettingData(self):
        user_setting_data={ # [4] User Setting
            "market":self.market,
            "period":self.period,
            "strategy":self.strategy,
            "principal":self.principal,
            "bid_unit":self.bid_unit,
            "bid_installment":self.bid_installment,
            "ask_unit":self.ask_unit,
            "ask_installment":self.ask_installment,
            "loss_limit":self.loss_limit,
            "alarm":self.alarm,
            "state":self.state
        }
        return user_setting_data

    def load_tradingData(self,trading_data:dict):
        self.trading_data = trading_data

    def get_tradingData(self):
        return self.trading_data

    def set_backTestData(self,testfile):
        test_data=test_tool.read_csvFile(testfile)

        return test_data




    def count_installment(self,order_type): # 분할 매수/매도를 하지 않는 경우 카운트 증가
        if order_type=="bid":
            if self.bid_installment!=0 or self.bid_installment!=1: # 분할매수하는 경우
                self.bid_installment_cnt+=1
        elif order_type=="ask":
            if self.ask_installment!=0 or self.ask_installment!=1: # 분할매수하는 경우
                self.ask_installment_cnt+=1

    def check_initial_principal(self):
        # 현재 보유하고 있는 현금(KRW) 조사
        KRW_balance = Upbit_Trade.upbit_tool.get_KRW_balance(access_key=self.coin_info.UPBIT_access_key,
                                                             secret_key=self.coin_info.UPBIT_secret_key)

        # 보유하고 있는 현금이 target coin용 예산보다 많은지 확인
        if KRW_balance>=self.principal:
            return True
        else:
            return False

    # 이거 수정 필
    def check_bid_available(self,KRW_balance,cur_price,bid_amount):
        # trading 예산 내 원화 잔고에서 매수 가능한지 확인
        if KRW_balance>=cur_price*bid_amount:
            return True
        else:
            return False

    def calc_bid_avail_quantity(self,bid_price):
        # 예산이 최소 구매 금액보다 작으면 매수 불가
        if self.KRW_balance<=self.minimum_trade_cost:
            return {}

        # 최대 구매가능 수량 확인
        max_bid_amount=self.KRW_balance//bid_price
        if max_bid_amount==0:
            return {}

        # 최소 구매가능 수량 확인
        if bid_price>=self.minimum_trade_cost:
            min_bid_amount=1
        else:
            available_amount=self.minimum_trade_cost//bid_price
            if available_amount*bid_price>=self.minimum_trade_cost:
                min_bid_amount=(available_amount*bid_price)
            else:
                min_bid_amount=(available_amount*bid_price)+1

        bid_avail_info={
            "max": max_bid_amount,
            "min":min_bid_amount
        }

        return bid_avail_info

    def get_bid_installment_number(self):
        # (1) Installment를 하지 않는 경우
        if (self.bid_installment == 1) or (self.bid_installment == 0):
            return 1

        # (2) Installment를 하는 경우
        else:
            return self.bid_installment-self.bid_installment_cnt

    def get_ask_installment_number(self):
        # (1) Installment를 하지 않는 경우
        if (self.ask_installment == 1) or (self.ask_installment == 0):
            return 1

        # (2) Installment를 하는 경우
        else:
            return self.ask_installment-self.ask_installment_cnt

    def calc_bid_order_amount(self,bid_price)->int:
        # bid 가능한 수량 계샨

        bid_avail_info=self.calc_bid_avail_quantity(bid_price)
        min_bid_avail = bid_avail_info["min"]
        max_bid_avail = bid_avail_info["max"]

        bid_amount=0 # 구매 수량
        if max_bid_avail==0:
            return bid_amount

        bid_divide_num=self.get_bid_installment_number()

        if max_bid_avail<=self.bid_unit: # bid_unit : 힌번에 bidding 가능한 최대 수량
            bid_amount=max_bid_avail//bid_divide_num
        else:
            bid_amount=self.bid_unit//bid_divide_num

        return bid_amount

    def calc_ask_order_amount(self):
        # ask 가능한 수량 계샨

        # 현재 보유하고 있는 코인개수 조회
        coin_balance=Upbit_Trade.upbit_tool.get_coin_balance(access_key=self.UPBIT_access_key,
                                                             secret_key=self.UPBIT_secret_key,
                                                             market=self.market)
        ask_amount = 0
        ask_divide_num = self.get_ask_installment_number()

        if coin_balance==0:
            return ask_amount

        if coin_balance<=self.ask_unit:
            ask_amount=coin_balance//ask_divide_num
        else:
            ask_amount=self.ask_unit//ask_divide_num

        return ask_amount


    def bid(self,check_bid_timing,calc_Bid_max_Price):
        if check_bid_timing() == True:
            bid_price = calc_Bid_max_Price()
            bid_order_amount = self.calc_bid_order_amount(bid_price=bid_price)


            if self.state=="run" or self.state=="Run":
                pass
            elif self.state=="simulation" or self.state=="Simulation":
                order_result=self.order_sim_bid(bid_order_amount,bid_price)

                return order_result
            else:
                print("bid() Error!!")


    def calc_ask_order_amount(self):
        pass

    def order_real_bid(self): # Real Run Mode
        pass

    def order_sim_bid(self, bid_amount,bid_price): # Simulation Mode

        order_result={
            "uuid": "cdd92199-2897-4e14-9448-f923320408ad",
            "side": "bid",
            "ord_type": "limit",
            "price": Upbit_Trade.upbit_tool.get_current_price(self.market),
            "avg_price": bid_price, # 	체결 가격의 평균가
            "state": "wait",
            "market": self.market,
            "created_at":basic_tool.get_current_kst_Time(),
            "volume": bid_amount, # 사용자가 입력한 주문 양
            "remaining_volume": "0.0", # 체결 후 남은 주문 양
            "reserved_fee": "0.0015",
            "remaining_fee": "0.0015",
            "paid_fee": "0.0",
            "locked": "1.0015",
            "executed_volume": bid_amount, # 체결된 양
            "trades_count": 0
        }

        self.KRW_balance=self.KRW_balance - (bid_price*bid_amount)
        self.coin_balance=self.coin_balance+bid_amount

        return order_result

    def order_real_ask(self): # Real Run Mode
        pass

    def order_sim_ask(self): # Simulation Mode
        pass





    def start_trading(self,timer_count):
        timer_count+=1

        # ------------------- TRADING SECTION -------------------
        self.sell_func()
        self.buy_func()
        # ------------------- TRADING SECTION -------------------

        trading_timer=threading.Timer(1,self.start_trading,args=[timer_count])

        trading_timer.start() # timer start

        if timer_count >= int(self.get_trading_period() / self.get_monitoring_term()):
            trading_timer.cancel() # timer stop

    def simulation_start(self):
        pass



if __name__=="__main__":
    test_cls=Trading_Config()

    access_key = "InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC"
    secret_key = "P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO"
    server_url = "https://api.upbit.com"

    upbit_apiInfo={
        "upbit_access_key":access_key,
        "upbit_secret_key":secret_key
    }

    target_coinInfo={
        "market":"KRW-WAVES",
        "period":"1Hour",
        "strategy":"Strategy1",
        "principal":"100000",
        "bid_unit":"50000",
        "bid_installment":"1",
        "ask_unit":"50000",
        "ask_installment":"1",
        "target_earning":"5%",
        "loss_limit":"-5%",
        "alarm":"None",
        "state":"Simulation",
        "balance":"1",
        "avg_buy_price":"6310",
        "cur_price":"8065.0",
        "earning":"0",
        "earning_rate":"0%",
        "today_tradingNum":"0",
        "accum_tradingNum":"0",
        "start_time":"2022-08-11-09-59-04",
        "end_time":"2022-08-11-10-59-04",
        "remain_time":"Days--1-Hours-23-Minutes-32"
    }

    test_cls.load_configData(upbit_apiInfo=upbit_apiInfo,
                            target_coinInfo=target_coinInfo)

    print(test_cls.get_user_SettingData())