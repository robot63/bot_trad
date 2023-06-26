import cbpro
import time

import json

# Chemin vers le fichier de configuration
config_file = '/path/to/config.json'

# Charger les clés d'API à partir du fichier de configuration
with open(config_file) as f:
    config = json.load(f)
    API_KEY = config['api_key']
    API_SECRET = config['api_secret']
    API_PASSPHRASE = config['api_passphrase']

# Initialisation du client Coinbase
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)


# Fonction pour placer un ordre d'achat
def place_buy_order(product_id, amount, price):
    response = auth_client.place_limit_order(
        product_id=product_id,
        side='buy',
        price=price,
        size=amount
    )
    return response

# Fonction pour placer un ordre de vente
def place_sell_order(product_id, amount, price):
    response = auth_client.place_limit_order(
        product_id=product_id,
        side='sell',
        price=price,
        size=amount
    )
    return response

# Fonction pour récupérer le solde disponible
def get_available_balance(currency):
    accounts = auth_client.get_accounts()
    for account in accounts:
        if account['currency'] == currency:
            return float(account['available'])

    return 0.0

# Fonction principale du bot de trading
def run_trading_bot():
    product_id = 'RNDR-USD'  # Paire de trading RNDR-USD
    trade_amount = 10.0  # Montant de chaque transaction
    buy_price = 0.5  # Prix d'achat
    sell_price = 1.0  # Prix de vente

    while True:
        # Vérifier le solde disponible
        available_balance = get_available_balance('USD')

        # Vérifier si suffisamment de fonds sont disponibles pour placer un ordre d'achat
        if available_balance >= trade_amount * buy_price:
            # Placer un ordre d'achat
            buy_order = place_buy_order(product_id, trade_amount, buy_price)
            print('Ordre d\'achat placé:', buy_order)

        # Vérifier si suffisamment de RNDR sont disponibles pour placer un ordre de vente
        rndr_balance = get_available_balance('RNDR')
        if rndr_balance >= trade_amount:
            # Placer un ordre de vente
            sell_order = place_sell_order(product_id, trade_amount, sell_price)
            print('Ordre de vente placé:', sell_order)

        # Attendre un certain laps de temps avant de passer à la prochaine itération
        time.sleep(60)  # Attendre 1 minute

# Exécuter le bot de trading
run_trading_bot()
