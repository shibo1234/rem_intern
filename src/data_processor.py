import pandas as pd
import pandasql as psql

class DataProcessor:
    """
    DataProcessor class to process the data
    Add more methods to process the data, users can use these methods to query the data
    """
    def __init__(self, df):
        self.df = df

    def execute_query(self, query):
        """
        Execute the SQL query on the dataframe
        :param query:
        :return:
        """
        print(f"Executing query: {query}")
        print(psql.sqldf(query, {"df": self.df}))
        return psql.sqldf(query, {"df": self.df})


    # this is a high level API
    def find_top_k_earners_over_all_carriers(self, k, period):
        """
        Find the top k earners by commission period
        :param k: number of top earners
        :param period:  commission period
        :return:
        """
        self.df['Commission_Period'] = pd.to_datetime(self.df['Commission_Period'], errors='coerce')
        filtered_df = self.df[self.df['Commission_Period'].dt.strftime('%Y-%m') == period]

        top_earners = filtered_df.groupby('Earner_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]

        return top_earners


    def find_top_k_carriers(self, k):
        """
        Find the top k carriers based on their total commission
        :param k: number of top carriers
        :return:
        """
        top_carriers = self.df.groupby('Carrier_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]
        print(f'Top {k} carriers based on total commission:')
        print(top_carriers)
        return top_carriers

    def list_all_carriers(self):
        """
        List all carriers
        :return:
        """
        carriers = self.df['Carrier_Name'].unique()

        print(f'All carriers:')
        print(carriers)
        return carriers



    def find_top_k_plans(self, k):
        """
        Find the top k plans based on their total commission
        :param k: number of top plans
        :return:
        """
        top_plans = self.df.groupby('Plan_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]
        print(f'Top {k} plans based on total commission:')
        print(top_plans)
        return top_plans


if __name__ == "__main__":
    df = pd.read_csv('../database/normalized.csv')
    print(df.head())
    data_processor = DataProcessor(df)

    # result = data_processor.find_top_k_earners_over_all_carriers(10, '2024-06')

    # result = data_processor.find_top_k_carriers(10)
    # result = data_processor.list_all_carriers()
    # query = """
    #     SELECT Earner_Name, SUM(Commission_Amount) AS Total_Commission
    #     FROM df
    #     WHERE strftime('%Y-%m', Commission_Period) = '2024-06'
    #     GROUP BY Earner_Name
    #     ORDER BY Total_Commission DESC
    #     LIMIT 10;
    # """
    # result1 = data_processor.execute_query(query)
    #






