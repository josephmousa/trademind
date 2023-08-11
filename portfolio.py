import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Portfolio:

    def __init__(self, seed_capital, number_of_positions, current_date, data):
        self.seed_capital = seed_capital
        self.current_capital = seed_capital
        self.position_size = seed_capital / number_of_positions
        self.current_date = current_date
        self.positions = []
        self.trades_list = []
        self.data = data
        self.totals = []
        
    def liquidate(self):
        for df in self.get_positions():
            symbol = df['Stock']
            current_date = self.get_current_date()
            data_frames = self.data.get_data_frames()
            for d in data_frames:
                row = d[(d['Stock'] == symbol ) & (d['Date'] == current_date)]
                if not row.empty:
                    price_on_date = row['Close'].values[0]  # Retrieve the specific value
                    sale = df['Amount'] * price_on_date
                    self.increase_current_capital(sale)
        self.reset_positions()
    
    def get_current_portfolio_value(self):
        total = self.get_current_capital()
        
        for df in self.get_positions():
            symbol = df['Stock']
            current_date = self.get_current_date()
            data_frames = self.data.get_data_frames()
            for d in data_frames:
                row = d[(d['Stock'] == symbol ) & (d['Date'] == current_date)]
                if not row.empty:
                    price_on_date = row['Close'].values[0]  
                    money = df['Amount'] * price_on_date
                    total += money
            
        self.totals.append((total, self.get_current_date()))
        
    def plot_equity_curve(self):

        totals = self.totals
        # extract x & y values
        x = [i[1] for i in totals]
        y = [i[0] for i in totals]
        
        # Clean outliers
        q1 = np.percentile(y, 25)
        q3 = np.percentile(y, 75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_indices = np.where((y < lower_bound) | (y > upper_bound))[0]

        for idx in outlier_indices:
            y[idx] = y[idx - 1]
        
        # create line chart with matplotlib
        plt.plot(x, y, linestyle='-')
        plt.xlabel('Dates')
        plt.ylabel('Portfolio Value in $')
        plt.title('Equity curve for portfolio')
        plt.grid(True)
        plt.show()
                

    def get_seed_capital(self):
        return self.seed_capital
    
    def get_position_size(self):
        return self.position_size
    
    def get_current_capital(self):
        return self.current_capital
    
    def set_position_size(self, number_of_positions):
        self.position_size = self.get_seed_capital / number_of_positions
    
    def set_current_capital(self, amount):
        self.current_capital = self.get_current_capital() - amount
    
    def increase_current_capital(self, amount):
        self.current_capital = self.get_current_capital() + amount
        
    def set_current_date(self, date):
        self.current_date = date
    
    def get_current_date(self):
        return self.current_date
    
    def get_positions(self):
        return self.positions
    
    def reset_positions(self):
        self.positions = []
    
    def append_to_positions(self, df):
        self.get_positions().append(df)
    
    def check_positions_empty(self):
        return len(self.get_positions()) == 0
    
    def get_trades_list(self):
        return self.trades_list
    
    def append_to_trades_list(self, df):
        self.get_trades_list().append(df)
        
    def get_stock_amount_with_symbol(self, symbol):
        amount = 0
        for df in self.get_positions():
            if df['Stock'] == symbol:
                amount = df['Amount']
                break
        return amount
            
    
    def get_list_of_symbols(self):
        symbols = []
        for df in self.get_positions():
            symbols.append(df['Stock'])
        return symbols
    
    def remove_from_positions(self, symbol):
            self.positions = [df for df in self.positions if df["Stock"] != symbol]
