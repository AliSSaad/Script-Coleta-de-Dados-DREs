class dicionarioEmpresas:
    def __init__(self):
        self.empresas = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet",
                         "AMZN": "Amazon", "BRK.A": "Berkshire-Hathaway", "NVDA": "NVIDIA",
                         "BRK.B": "Berkshire-Hathaway", "TSLA": "Tesla", "META": "Meta-Platforms",
                         "XOM": "Exxon", "UNH": "UnitedHealth-Group", "V": "Visa", "JNJ": "Johnson-Johnson",
                         "WMT": "Walmart", "JPM": "JPMorgan-Chase", "PG": "Procter-Gamble", "MA": "Mastercard",
                         "LLY": "Eli-Lilly", "CVX": "Chevron", "HD": "Home-Depot",
                         "ABBV": "AbbVie", "MRK": "Merck", "KO": "CocaCola", "AVGO": "Broadcom", "ORCL":"Oracle",
                         "AMD": "AMD", "BAC": "Bank-Of-America", "SCHW": "Charles-Schwab", "NFLX": "Netflix",
                         "INTC": "Intel", "SQ": "Block", "CRM": "Salesforce", "ADBE": "Adobe"}
    def get_nome_empresa(self, nome):
        try:
            nome_da_empresa = self.empresas[nome]
            return nome_da_empresa
        except KeyError:
            print("A empresa", nome, "não está no dicionário.")
            return None
