import aiohttp
import asyncio

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

if __name__ == '__main__':
    print("first code")