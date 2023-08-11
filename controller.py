import pandas as pd
import os


class Controller:
    
    def __init__(self, data_reader, portfolio, signal_generator, scorer, executor, start_date, end_date):
        self.data_reader = data_reader
        self.portfolio = portfolio
        self.signal_generator = signal_generator
        self.scorer = scorer
        self.executor = executor
        self.start_date = start_date
        self.end_date = end_date
        self.current_date = start_date
    
    def simulate(self):
        while True:
    
            # Signal Generation
            self.signal_generator.compute()

            # Stop
            if self.current_date == self.end_date:
                self.portfolio.liquidate()
                current = self.portfolio.get_current_capital()
                print(f"Started with $ {self.portfolio.get_seed_capital()} and finished with $ {current}")
                performance = ((current - self.portfolio.get_seed_capital()) / self.portfolio.get_seed_capital()) * 100
                print(f"Porfolio performance from {self.start_date} to {self.end_date} was: {performance}%" )
                break
            else:
                # Execute
                print("================================")
                print(self.current_date)
                self.portfolio.get_current_portfolio_value()
                self.scorer.prediction_scorer()
                self.executor.execute_buy()
                self.executor.execute_sell()
                self.current_date = self.update_current_date(self.current_date)
                self.signal_generator.set_current_date(self.current_date)
                self.portfolio.set_current_date(self.current_date)
                print("================================")
    
    def update_current_date(self, date):
        date = date + pd.Timedelta(days=1)
        return date
        