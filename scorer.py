import random

class Scorer:
    
    def __init__(self, data_reader, signal_generator):
        self.data_reader = data_reader
        self.signal_generator = signal_generator
        self.buy_order = []
        self.sell_order = []
        
    def random_scorer(self):
        self.reset_orders()
        if not self.signal_generator.get_potential_buy_trades():
            pass
        else:
            buy = random.choice(self.signal_generator.get_potential_buy_trades())
            self.buy_order.append(buy)
        
        if not self.signal_generator.get_potential_sell_trades():
            pass
        else:
            sell = random.choice(self.signal_generator.get_potential_sell_trades())
            self.sell_order.append(sell)
            
        print(self.buy_order)
        
    def prediction_scorer(self):
        self.reset_orders()
        
        predicted_returns = self.data_reader.get_predicted_returns_as_df()
        
        if not self.signal_generator.get_potential_buy_trades():
            pass
        else:
            buys = self.signal_generator.get_potential_buy_trades()
            for df in buys:
                stock = df['Stock']
                row = predicted_returns[predicted_returns['Stock'] == stock]
                pred = row['Predicted returns'].iloc[0]
                df['Predicted returns'] = pred
                self.buy_order.append(df)
            
            sorted_dfs = sorted(self.buy_order, key=lambda df: df['Predicted returns'])

            self.buy_order = [sorted_dfs[-1]]
        
        if not self.signal_generator.get_potential_sell_trades():
            pass
        else:
            # concatenating the list of potential buys to a single dataframe
            sells = self.signal_generator.get_potential_sell_trades()
            for df in sells:
                stock = df['Stock']
                row = predicted_returns[predicted_returns['Stock'] == stock]
                pred = row['Predicted returns'].iloc[0]
                df['Predicted returns'] = pred
                self.sell_order.append(df)
            
            sorted_dfs = sorted(self.sell_order, key=lambda df: df['Predicted returns'])

            self.sell_order = [sorted_dfs[0]]
        
    def reset_orders(self):
        self.buy_order = []
        self.sell_order = []
    
    def buy_order_empty(self):
        if len(self.buy_order) == 0:
            return True
        return False