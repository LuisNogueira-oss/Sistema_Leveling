import os
import json
from datetime import date
from jogador import Jogador
from missoes import missoes_fixas
from mercado import obter_preco_btc

def registrar_conhecimento(missao_nome, topico):
    """Grava o aprendizado no histórico JSON."""
    arquivo = 'conhecimento.json'
    dados = []
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
                
    novo_log = {
        "data": str(date.today()),
        "missao": missao_nome,
        "topico": topico
    }
    dados.append(novo_log)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        
    print(f"\n[ORÁCULO]: Conhecimento '{topico}' gravado na eternidade.")

def executar_sistema():
    felipe = Jogador()
    felipe.carregar()
    
    preco = obter_preco_btc()
    if preco:
        tendencia = " ▲" if preco > felipe.ultimo_btc else " ▼"
        felipe.ultimo_btc = preco
        display_btc = f"R$ {preco:,}{tendencia}"
        status = "ONLINE"
    else:
        display_btc = f"R$ {felipe.ultimo_btc:,} (CACHED)"
        status = "LIMITADO"

    os.system('cls' if os.name == 'nt' else 'clear')
    meta = int(felipe.nivel * 500)
    
    print("="*70)
    print(f" OPERADOR: {felipe.nome.upper()} | STATUS: {status} | BTC: {display_btc}")
    print(f" NÍVEL: {felipe.nivel} | XP: {felipe.xp}/{meta} | LÓGICA: {felipe.atributos['logica']} (RANK C)")
    print("="*70)

    for id, m in missoes_fixas.items():
        print(f" [{id}] {m['nome'].ljust(20)} | +{m['xp']} XP | +{m['pontos']} {m['attr'].capitalize()}")

    esc = input("\nID da missão: ")
    if esc in missoes_fixas:
        m = missoes_fixas[esc]
        
        # Novo gatilho de conhecimento
        print("-" * 50)
        topico = input(f"Relatório de Conhecimento - O que foi dominado em '{m['nome']}'?\n> ")
        registrar_conhecimento(m['nome'], topico)
        print("-" * 50)
        
        felipe.xp += m['xp']
        felipe.atributos[m['attr']] += m['pontos']
        
        while felipe.xp >= (felipe.nivel * 500):
            felipe.xp -= (felipe.nivel * 500)
            felipe.nivel += 1
            print(f"\n!!! ASCENSÃO DETECTADA: NÍVEL {felipe.nivel} !!!")
        
        felipe.salvar()
        print("\n[SISTEMA]: Sincronização de status concluída.")

if __name__ == "__main__":
    executar_sistema()
    