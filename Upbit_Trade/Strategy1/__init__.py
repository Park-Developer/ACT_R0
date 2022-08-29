import pyupbit
import pandas
from Upbit_Trade import Trading_Config
import Upbit_Trade.upbit_tool
import Upbit_Trade.calc_tool
import math
import Upbit_Trade.config
import json
import os

# [ CONFIG VARIABLE ]
STRATEGY1_CONFIG_JSON_ADDRESS="./Strategy1/strategy1.json"

if os.getcwd()=="C:\\Users\\gnvid\\PycharmProjects\\ACT_R0\\Upbit_Trade": # UpbitTrade 패키지에서 실행하는 경우
    with open(os.getcwd()+"\\Strategy1\\strategy1.json", 'r', encoding="utf-8") as f:  # 이거 없애기
        STRATEGY1_CONFIG_DATA = json.load(f)
else:                                                                       # 다른 패키지에서 실행하는 경우
    with open(os.getcwd()+"\\Upbit_Trade\\Strategy1\\strategy1.json", 'r', encoding="utf-8") as f:  # 이거 없애기
        STRATEGY1_CONFIG_DATA = json.load(f)


# [ CLASS DEFINITION ]
class Strategy(Trading_Config):
    def __init__(self):
        super().__init__()

        # Config Part
        self.strategy_config = STRATEGY1_CONFIG_DATA

        # Introduction Part
        self.intro_part=self.strategy_config["INTRODUCTION_PART"]

        self.name=self.intro_part["name"]
        self.introduction = self.intro_part["introduction"]
        self.link=self.intro_part["link"]
        self.developer = self.intro_part["developer"]
        self.contributor=self.intro_part["contributor"]
        self.update_date = self.intro_part["update_date"]
        self.version = self.intro_part["version"]


        self.config_part = self.strategy_config["CONFIG_PART"]

        self.para_reference =self.config_part["para_reference"]

        # Mode Set
        if self.state == "run" or self.state=="Run":
            self.run_mode ="Run"
        elif self.state == "simulation" or self.state=="Simulation":
            self.run_mode = "Simulation"
        else:
            self.run_mode = "Idle"


    def get_strategyInfo(self): # ok
        intro_info={
                "name":self.name,
                "introduction":self.introduction,
                "developer":self.developer,
                "link":self.link,
                "contributor":self.contributor,
                "update_date":self.update_date
            }

        return intro_info


    def calc_ref_price(self): # ok
        if self.para_reference["dynamic_ref"]==True:
            pass

        if self.para_reference["dynamic_ref"]==False:
            try:
                self.ref_price = Upbit_Trade.calc_tool.calc_avg(self.trading_data["opening_price"])

            except KeyError as e:
                print(" calc_ref_price(self): ERROR!",e)


        return self.ref_price # default : None


    def calc_Bid_max_Price(self): # ok
        # Reference Price로부터 Bidding이 가능한 최댓값 계산
        self.bid_maxPrice = self.ref_price*float(100-self.para_reference["bid_price_condition1"])/100

        return self.bid_maxPrice


    def calc_Ask_min_Price(self): # ok
        # Reference Price로부터 Asking이 가능한 최댓값 계산
        self.ask_minPrice = self.ref_price * float(100 + self.para_reference["ask_price_condition1"]) / 100

        return self.ask_minPrice


    def check_bid_timing(self):
        # 매수 전략 : 현재 가격이 1시간 동안(Unit:1분)의 종가 평균보다 5% 낮으면 매수
        # (1) Dynamic Bidding Case
        if self.para_reference["dynamic_bid"]==True:
            pass

        # (2) Static Bidding Case
        if self.para_reference["dynamic_bid"]==False:
            # 현재 가격을 기준으로 bid_maxPrice보다 낮으면 매수

            '''
            BackTesting을 하는 경우 현재 코인의 가격을 실제값이 아닌 백테스팅 데이터로받음
            '''
            if self.coin_info.is_backtesting==True:
                self.coin_info.cur_price= self.backtest_data
            else:
                self.coin_info.cur_price=Upbit_Trade.upbit_tool.get_current_price(market=self.coin_info.market)

            self.coin_info.bid_maxPrice=self.calc_Bid_max_Price()

            if self.coin_info.cur_price <= self.coin_info.bid_maxPrice:
                return True
            else:
                return False


    def check_ask_timing(self):
        # 매도 전략 : 현재 가격이 1시간 동안(Unit:1분)의 종가 평균보다 5% 높으면 매도
        # (1) Dynamic Asking Case
        if self.para_reference["dynamic_ask"]==True:
            pass

        # (2) Static Asking Case
        if self.para_reference["dynamic_ask"] ==False:
            self.coin_info.cur_price=Upbit_Trade.upbit_tool.get_current_price(market=self.coin_info.market)
            self.coin_info.ask_minPrice=self.calc_Ask_min_Price()

            if self.coin_info.cur_price>= self.coin_info.ask_minPrice:
                return True
            else:
                return False
