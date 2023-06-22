import cbpro
import numpy as np
import time
from config import API_KEY, API_SECRET, API_PASSPHRASE

public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)

# Paramètres du bot
PAIR = 'REN-USD'
BUY_AMOUNT = 100
SELL_AMOUNT = 100
SMALL_WINDOW = 50
BIG_WINDOW = 200

# Fonction pour calculer les moyennes mobiles
def calculate_rolling_average(data, window_size):
    weights = np.repeat(1.0, window_size) / window_size
    smas = np.convolve(data, weights, 'valid')
    return smas

# Fonction pour exécuter un ordre d'achat
def buy(currency_pair, amount):
    order = auth_client.place_market_order(product_id=currency_pair, side='buy', funds=amount)
    return order

# Fonction pour exécuter un ordre de vente
def sell(currency_pair, amount):
    order = auth_client.place_market_order(product_id=currency_pair, side='sell', size=amount)
    return order

# Boucle principale du bot
while True:
    # Récupération des données de prix les plus récentes
    ticker_data = public_client.get_product_ticker(product_id=PAIR)
    current_price = float(ticker_data['price'])
    
    # Récupération des données de prix historiques
    historical_data = public_client.get_product_historic_rates(product_id=PAIR, granularity=60)
    prices = np.array([float(d[4]) for d in historical_data])
    
    # Calcul des moyennes mobiles
    small_rolling_average = calculate_rolling_average(prices, SMALL_WINDOW)
    big_rolling_average = calculate_rolling_average(prices, BIG_WINDOW)
    
    # Détermination du signal de trading
    if small_rolling_average[-1] > big_rolling_average[-1] and small_rolling_average[-2] < big_rolling_average[-2]:
        # Acheter
        buy_order = buy(PAIR, BUY_AMOUNT)
        print('Achat effectué:', buy_order)
    elif small_rolling_average[-1] < big_rolling_average[-1] and small_rolling_average[-2] > big_rolling_average[-2]:
        # Vendre
        sell_order = sell(PAIR, SELL_AMOUNT)
        print('Vente effectuée:', sell_order)
    
    # Attendre un certain temps avant de rafraîchir les données
    time.sleep(30)
