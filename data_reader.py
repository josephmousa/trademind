import pandas as pd
import os


class DataReader:

    """
    A class for reading CSV files from a directory and storing them as pandas data frames.

    This class provides functionality to read multiple CSV files from a specified directory,
    convert them into data frames using pandas, and store the resulting data frames in a list for later usage.

    """
    
    def __init__(self, data_dir, predictions_dir):
        self.data_dir = data_dir
        self.data_frames = []
        self.predicted_returns = predictions_dir
    
    def read_symbol(self, symbol):
        df = pd.read_csv(f"{self.get_data_dir()}/{symbol}.csv")
    
        return df
    
    def read_csv_files(self):
        csv_files = [x for x in os.listdir(self.get_data_dir()) if x.endswith('csv')]
        for file in csv_files:
            file_name = file[:-4]
            df = self.read_symbol(file_name)
            df['Stock'] = file_name
            stock_column = df.pop(df.columns[-1])
            df.insert(0, stock_column.name, stock_column)
            self.data_frames.append(df)

    def extract_with_dates(self, df, start_date, end_date):
        df['Date'] = pd.to_datetime(df['Date'])

        new_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        return new_df
    

    def extract_df_with_symbol(self, symbol):
        for df in self.get_data_frames():
            if df["Stock"].iloc[0] == symbol:
                return df
            
    def extract_with_symbol_and_dates(self, symbol, start_date, end_date):
        new_df = self.extract_df_with_symbol(symbol)
        new_df_with_dates = self.extract_with_dates(new_df, start_date, end_date)
        return new_df_with_dates

    # Getters and Setters

    def get_data_dir(self):
        return self.data_dir
    
    def get_data_frames(self):
        return self.data_frames
    
    def set_data_dir(self, path):
        self.data_dir = path
        
    def get_predicted_returns_as_df(self):
        df = pd.read_csv(self.predicted_returns)
        sorted_df = df.sort_values(by='Predicted returns', ascending = False)
        return sorted_df