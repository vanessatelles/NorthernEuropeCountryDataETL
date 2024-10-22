import aiohttp
import asyncio
import psycopg2
from sqlalchemy import create_engine 


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

    def __init__(self):

        self.data = {
            'nation_official_name': list(),
            'currency_name': list(),
            'population': list()
        }
    
    def data_to_dict(self, response):
        for country in response:
            currencies_key = list(country['currencies'].keys())[0]
            self.data['nation_official_name'].append(country['name']['official'])
            self.data['currency_name'].append(country['currencies'][currencies_key]['name'])
            self.data['population'].append(country['population'])

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
    print("first code")