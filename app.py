from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date
from jogador import Jogador
from missoes import missoes_fixas

app = Flask(__name__)

def registrar_conhecimento(missao_nome, topico):
    """Função interna do servidor para salvar o diário."""
    arquivo = 'conhecimento.json'
    dados = []
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
                
    novo_log = {"data": str(date.today()), "missao": missao_nome, "topico": topico}
    dados.append(novo_log)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def dashboard():
    """Rota principal que exibe o painel."""
    # Lemos os dados direto do arquivo status.json para o HTML renderizar
    status_dados = {}
    if os.path.exists('status.json'):
        with open('status.json', 'r', encoding='utf-8') as f:
            status_dados = json.load(f)
            
    diario_dados = []
    if os.path.exists('conhecimento.json'):
        with open('conhecimento.json', 'r', encoding='utf-8') as f:
            try:
                diario_dados = json.load(f)
            except json.JSONDecodeError:
                diario_dados = []

    return render_template('index.html', status=status_dados, diario=diario_dados, missoes=missoes_fixas)

@app.route('/completar_missao', methods=['POST'])
def completar_missao():
    """Rota invisível que recebe o clique do botão e processa o XP."""
    missao_id = request.form.get('missao_id')
    topico = request.form.get('topico')
    
    if missao_id in missoes_fixas:
        m = missoes_fixas[missao_id]
        
        # Carrega o jogador real
        felipe = Jogador()
        felipe.carregar()
        
        # Adiciona Status
        felipe.xp += m['xp']
        felipe.atributos[m['attr']] += m['pontos']
        
        # Lógica de Ascensão (Level Up)
        while felipe.xp >= (felipe.nivel * 500):
            felipe.xp -= (felipe.nivel * 500)
            felipe.nivel += 1
            
        felipe.salvar() # Salva no status.json
        registrar_conhecimento(m['nome'], topico) # Salva no conhecimento.json
        
    # Redireciona de volta para o Dashboard instantaneamente
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # O Render usa uma variável de ambiente chamada PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)