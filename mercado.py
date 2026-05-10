import requests

def obter_preco_btc():
    try:
        # Consulta à API pública da Coinbase para o par BTC-BRL
        url = "https://api.coinbase.com/v2/prices/BTC-BRL/spot"
        resposta = requests.get(url, timeout=5)
        dados = resposta.json()
        preco = float(dados['data']['amount'])
        return int(preco)
    except Exception:
        return None  # Retorna None em caso de falha na conexão
