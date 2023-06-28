import json
import time
import cbpro
import ta

# Charger les clés API à partir du fichier secret.json
with open('secret.json', 'r') as f:
    secrets = json.load(f)

API_KEY = secrets['API_KEY']
API_SECRET = secrets['API_SECRET']
API_PASSPHRASE = secrets['API_PASSPHRASE']

# Initialiser la connexion à l'API Coinbase Pro
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)

# Paramètres des Bandes de Bollinger
time_period = 20
num_std_devs = 2

while True:
    try:
        # Obtenir les données historiques du RNDR
        historical_data = auth_client.get_product_historic_rates('RNDR-USD', granularity=86400)
        close_prices = [float(data[4]) for data in historical_data]

        # Calculer les Bandes de Bollinger
        bollinger_bands = ta.volatility.BollingerBands(close=close_prices, window=time_period, window_dev=num_std_devs)

        # Obtenir le dernier prix du RNDR
        ticker = auth_client.get_product_ticker(product_id='RNDR-USD')
        last_price = float(ticker['price'])

        # Vérifier si le prix se rapproche des limites supérieures ou inférieures des Bandes de Bollinger
        if last_price > bollinger_bands.bollinger_hband_indicator().iloc[-1]:
            # Effectuer une action en cas de signal d'achat
            print("Signal d'achat détecté !")

        elif last_price < bollinger_bands.bollinger_lband_indicator().iloc[-1]:
            # Effectuer une action en cas de signal de vente
            print("Signal de vente détecté !")

        # Attendre un certain temps avant de vérifier à nouveau
        time.sleep(60)  # Attendre 1 minute avant la prochaine vérification

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        time.sleep(60)  # Attendre 1 minute en cas d'erreur pour éviter une boucle infinie de requêtes
