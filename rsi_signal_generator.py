import pandas as pd
import talib
from data_processor import AbstractDataProcessor

class RSISignalGenerator(AbstractDataProcessor):
    
    def __init__(self, data_reader, start_date, end_date, current_date, portfolio, period):
        self.data_reader = data_reader
        self.start_date = start_date
        self.end_date = end_date
        self.current_date = current_date
        self.portfolio = portfolio
        self.potential_buy_trades = []
        self.potential_sell_trades = []
        self.period = period
    
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
        rsi = self.calculate_RSI(df)
        df['Signal'] = 0
        df.loc[rsi < 30, 'Signal'] = 1
        
        if df.iloc[-1]['Signal'] == 1:
            row = df.iloc[-1]

            self.potential_buy_trades.append(row)
            
    def generate_sell_signals(self, df):
        rsi = self.calculate_RSI(df)
        df['Signal'] = 0
        df.loc[rsi > 70, 'Signal'] = -1
        
        if df.iloc[-1]['Signal'] == -1:
            row = df.iloc[-1]

            self.potential_sell_trades.append(row)

    def calculate_RSI(self, df):
        rsi = talib.RSI(df['Close'], timeperiod = self.period)
        return rsi
    