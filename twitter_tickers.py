"""
Twitter and stock tickers
Singletons used across the codebase.

"""
tickers = ['AAPL', 'MSFT', 'MMM', 'TSLA',
           'DE', 'HD', 'UNP', 'CAT', 'GS', 'COST']

tickers_twitter = ['ApplePodcasts', 'Microsoft', '3M', 'Tesla', 'JohnDeere',
                   'HomeDepot', 'UnionPacific', 'CaterpillarInc', 'GoldmanSachs', 'Costcocanada']

ticker_twitter_map = {
    'ApplePodcasts': 'AAPL',
    'Microsoft': 'MSFT',
    '3M': 'MMM',
    'Tesla': 'TSLA',
    'JohnDeere': 'DE',
    'HomeDepot': 'HD',
    'UnionPacific': 'UNP',
    'CaterpillarInc': 'CAT',
    'GoldmanSachs': 'GS',
    'Costcocanada': 'COST'
}
