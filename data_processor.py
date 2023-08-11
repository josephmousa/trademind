import pandas as pd
import os
import talib

from data_reader import DataReader

from abc import ABC, abstractmethod
class AbstractDataProcessor(ABC):

    # Run signal generator with desired parameters to identify potential trades
    # These will be fed to TradeScorer
    @abstractmethod
    def compute(self):
        pass
    
    @abstractmethod
    def generate_buy_signals():
        pass
    
    @abstractmethod
    def generate_sell_signals():
        pass
    
    
    # Utilities
    
    # Potential trades
    
    def reset_potential_trades(self):
        self.potential_buy_trades = []
        self.potential_sell_trades = []
    
    def get_potential_buy_trades(self):
        return self.potential_buy_trades
    
    def potential_buy_trades_is_empty(self):
        return len(self.get_potential_buy_trades()) == 0
    
    def get_potential_sell_trades(self):
        return self.potential_sell_trades
    
    def potential_sell_trades_is_empty(self):
        return len(self.get_potential_sell_trades()) == 0
    
    # Date managment

    def update_current_date(self):
        self.set_current_date(self.get_current_date() + pd.Timedelta(days=1))
    
    def get_current_date(self):
        return self.current_date

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def set_current_date(self, date):
        self.current_date = date