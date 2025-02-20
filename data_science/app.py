from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# ===== Página Principal =====
@app.route('/')
def home():
    return render_template('base.html')

# ===== Análise de Vendas =====
@app.route('/vendas')
def analise_vendas():
    try:
        # Carrega os dados
        df = pd.read_csv('data/vendas.csv')
        
        # Processamento de dados com pandas
        df['Data'] = pd.to_datetime(df['Data'])  # Converte para data
        df['Mês'] = df['Data'].dt.month  # Extrai o mês
        resumo = df.groupby('Produto')['Valor'].agg(['sum', 'mean', 'count'])  # Agregações
        
        # Dados para o template
        return render_template('vendas.html',
                            tabela=resumo.to_html(classes='table table-striped'),
                            top_produto=resumo['sum'].idxmax(),
                            total_vendas=resumo['sum'].sum().round(2))
    
    except FileNotFoundError:
        return "Erro: Arquivo 'vendas.csv' não encontrado na pasta data/."

if __name__ == '__main__':
    app.run(debug=True)