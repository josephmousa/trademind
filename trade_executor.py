from data_processor import AbstractDataProcessor
from portfolio import Portfolio

class TradeExecutor:

    def __init__(self, portfolio, scorer):
        self.portfolio = portfolio
        self.scorer = scorer

    def execute_buy(self):
        if self.get_portfolio().get_current_capital() > 0 and len(self.scorer.buy_order) > 0:
            trade = self.scorer.buy_order[0]
            print(trade)
            trade_price = trade['Close']
            position_size = self.portfolio.get_position_size()
            current_capital = self.portfolio.get_current_capital()
            
            
            if position_size < current_capital:
                amount_of_stock = position_size / trade_price
                cost = position_size
            else:
                amount_of_stock = current_capital / trade_price
                cost = current_capital
            
            new_df = trade
            new_df['Amount'] = amount_of_stock
            self.get_portfolio().append_to_positions(new_df)
            self.get_portfolio().append_to_trades_list(new_df)
            self.get_portfolio().set_current_capital(cost)
            #print()
            #print(self.get_portfolio().get_positions()
            
            
    
    def execute_sell(self):
        if len(self.scorer.sell_order) > 0:
            trade = self.scorer.sell_order[0]
            self.get_portfolio().append_to_trades_list(trade)
            trade_price = trade['Close']
            symbol = trade['Stock']
            stock_amount = self.get_portfolio().get_stock_amount_with_symbol(symbol)
            money = trade_price * stock_amount
            self.get_portfolio().increase_current_capital(money)
            
            # remove position from portfolio
            self.get_portfolio().remove_from_positions(symbol)
    
                

    def get_portfolio(self):
        return self.portfolio
    
    def get_data_processor(self):
        return self.data_processor