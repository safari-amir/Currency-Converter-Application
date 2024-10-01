import requests
from cachetools import cached, TTLCache

# Caching the exchange rates for 12 hours (43200 seconds) to minimize the API calls
cache = TTLCache(maxsize=200, ttl=12*60*60)

@cached(cache)
def get_exchange_rate(base_currency, target_currency):
    """
    Fetch the latest exchange rate for the given base and target currencies.
    The exchange rate is cached for efficiency using TTL (Time-To-Live) caching.

    Args:
        base_currency (str): The currency from which to convert (e.g., 'USD').
        target_currency (str): The currency to which you want to convert (e.g., 'EUR').

    Returns:
        tuple: (conversion_rate (float), time_last_update_unix (int))
    """
    url = f'https://v6.exchangerate-api.com/v6/cccde48f4320dc1dad4fbef5/latest/{base_currency}'
    # Make the request to get the exchange rate
    response = requests.get(url)
    data = response.json()

    # Extract the conversion rate for the target currency
    conversion_rate = data['conversion_rates'][target_currency]
    
    return conversion_rate, data['time_last_update_unix']

def convert_currency(amount, exchange_rate):
    """
    Convert the amount from the base currency to the target currency using the given exchange rate.

    Args:
        amount (float): The amount to convert.
        exchange_rate (float): The exchange rate to use for conversion.

    Returns:
        float: The converted amount.
    """
    return amount * exchange_rate

if __name__ == '__main__':
    # Take user input for base currency, target currency, and the amount to convert
    base_currency = input('Enter base currency: ').upper()
    target_currency = input('Enter target currency: ').upper()
    exchange_rate, _ = get_exchange_rate(base_currency, target_currency)
    
    amount = input('Enter amount of base currency: ')
    
    # Output the conversion result
    print('Converted result:', convert_currency(float(amount), exchange_rate))