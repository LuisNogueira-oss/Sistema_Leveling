import json

class Jogador:
    def __init__(self, nome="Felipe"):
        self.nome = nome
        self.nivel = 4
        self.xp = 0
        self.ultimo_btc = 0
        self.atributos = {"logica": 0, "estetica": 0, "tesouraria": 0}

    def salvar(self):
        dados = {
            "nome": self.nome, "nivel": int(self.nivel), "xp": int(self.xp),
            "ultimo_btc": int(self.ultimo_btc),
            "atributos": {k: int(v) for k, v in self.atributos.items()}
        }
        with open('status.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar(self):
        try:
            with open('status.json', 'r', encoding='utf-8') as f:
                d = json.load(f)
                self.nivel = int(d.get("nivel", 4))
                self.xp = int(d.get("xp", 0))
                self.ultimo_btc = int(d.get("ultimo_btc", 0))
                self.atributos = d.get("atributos", self.atributos)
        except FileNotFoundError:
            self.salvar()