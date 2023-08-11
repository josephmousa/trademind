import pandas as pd
import talib
from data_processor import AbstractDataProcessor

class SMASignalGenerator(AbstractDataProcessor):

    def __init__(self, data_reader, start_date, end_date, current_date, portfolio, short_period, long_period):
        self.data_reader = data_reader
        self.start_date = start_date
        self.end_date = end_date
        self.current_date = current_date
        self.portfolio = portfolio
        self.potential_buy_trades = []
        self.potential_sell_trades = []
        self.short_period = short_period
        self.long_period = long_period

    # Run signal generator with desired parameters to identify potential trades
    # These will be fed to TradeScorer
    def compute(self):
        # Reset both potential trades list 
        self.reset_potential_trades()
        # First check for sell signals
        if not self.portfolio.check_positions_empty():
            for df in self.portfolio.get_positions():
                symbol = df['Stock']
                new_df = self.data_reader.extract_with_symbol_and_dates(symbol, self.start_date, self.current_date)
                if not new_df.empty:
                    last_row = new_df.iloc[-1]
                    last_date = last_row['Date']
                    if last_date == self.current_date:
                
                        self.generate_sell_signals(new_df)
                    else:
                        continue
                else:
                    continue
                
        # Then check for buy signals
        for df in self.data_reader.get_data_frames():
            # If already holding this Symbol skip - some form of risk management
            if df['Stock'].isin(self.portfolio.get_list_of_symbols()).any():
                continue
            else:
                new_df = self.data_reader.extract_with_dates(df,self.start_date, self.current_date)
                if not new_df.empty:
                    last_row = new_df.iloc[-1]
                    last_date = last_row['Date']
                    if last_date == self.current_date:
                
                        self.generate_buy_signals(new_df)
                    else:
                        continue
                else:
                    continue
        
    def generate_buy_signals(self, df):
        short_sma = self.calculate_short_SMA(df)
        long_sma = self.calculate_long_SMA(df)
        df['Signal'] = 0
        #df['Short_SMA'] = short_sma
        #df['Long_SMA'] = long_sma
        df.loc[short_sma > long_sma, 'Signal'] = 1
        # If Symbol not in portfolio.positions
        if df.iloc[-1]['Signal'] == 1:
            row = df.iloc[-1]

            self.potential_buy_trades.append(row)
        
    def generate_sell_signals(self, df):
        short_sma = self.calculate_short_SMA(df)
        long_sma = self.calculate_long_SMA(df)
        df['Signal'] = 0
        df.loc[short_sma < long_sma, 'Signal'] = -1
        if df.iloc[-1]['Signal'] == -1:
            row = df.iloc[-1]

            self.potential_sell_trades.append(row)
    
    def calculate_short_SMA(self, df):
        short_sma = talib.SMA(df['Close'], timeperiod = self.short_period)
        return short_sma
    
    def calculate_long_SMA(self, df):
        long_sma = talib.SMA(df['Close'], timeperiod = self.long_period)
        return long_sma
