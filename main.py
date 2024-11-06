import os
import aiohttp
import asyncio
import psycopg2
import pandas as pd
from sqlalchemy import create_engine 

DB_NAME = os.getenv('DBNAME','postgres')
DB_USER = os.getenv('DBUSER','postgres')
DB_PASSWORD = os.getenv('DBPASSWORD','admin')
DB_HOST = os.getenv('DBHOST','172.17.0.2')
DB_PORT = os.getenv('DBPORT','5432')

async def fetch_data_from_api():
    """
    Async function to call the API and fetch data from the endpoint.
    
    Returns:
        dict: Data received from the API as a JSON dictionary.
    """

    async with aiohttp.ClientSession() as session:

        api_url = 'https://restcountries.com/v3.1/subregion/Northern Europe?fields=name,currencies,population'
        async with session.get(api_url) as resp:
            response = await resp.json()
            return response

class CountryData():
    """
    This class is designed to manage raw data from the API endpoint.
    It processes and formats the data before loading it into the database.
    """
    def __init__(self):
        """
        Initialize an instance of CountrData with a dict.
        The dict has three keys, each associated with an emptylist.
        """
        self.data = {
            'nation_official_name': list(),
            'currency_name': list(),
            'population': list()
        }
    
    def data_to_dict(self, response):
        """
        Method to manage and process the raw data into a standardized dict.

        Args:            
            response (dict): Data from the API.
        """
        for country in response:
            currencies_key = list(country['currencies'].keys())[0]
            self.data['nation_official_name'].append(country['name']['official'])
            self.data['currency_name'].append(country['currencies'][currencies_key]['name'])
            self.data['population'].append(country['population'])

    def get_dataframe(self):
 
        df = pd.DataFrame(self.data)
        
        return df
    
    def load_to_sql(self, dataframe, table_name, conn):

        dataframe.to_sql(table_name, conn, if_exists='replace', index = False)

        return

def prepare_database(table_name):

    db = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    conn = db.connect()

    conn1 =  psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT)
    
    conn1.autocommit = True
    
    c = conn1.cursor()
    
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} 
                (nation_official_name VARCHAR ( 50 ) PRIMARY KEY,
                currency_name VARCHAR ( 50 ) NOT NULL,
                population INT NOT NULL);''')
    
    conn1.commit()
    conn1.close()

    return conn

if __name__ == '__main__':
    api_response = asyncio.run(fetch_data_from_api())
    conn = prepare_database('db')
    all_data = CountryData()
    all_data.data_to_dict(api_response)
    df = all_data.get_dataframe()
    all_data.load_to_sql(df,'db', conn)