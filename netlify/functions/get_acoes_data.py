import json
import yfinance as yf
import pandas as pd
import os

def coletar_dados_financeiros_api(ticker_symbol):
    """
    Coleta os dados financeiros (informações e histórico) de um ticker
    usando a biblioteca yfinance.
    """
    # print(f"Buscando dados financeiros para {ticker_symbol} via API yfinance...") # Netlify Functions don't show stdout easily
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. Obter informações gerais da ação
    info = ticker.info
    
    # 2. Obter histórico de preços (ex: último ano)
    hist = ticker.history(period="1y")
    
    # Converter o histórico (DataFrame) para um formato compatível com JSON
    hist_json = hist.reset_index().to_dict(orient='records')
    for record in hist_json:
        for key, value in record.items():
            if isinstance(value, pd.Timestamp):
                record[key] = value.isoformat()

    # print("Dados financeiros obtidos com sucesso.")
    return {"info": info, "historico": hist_json}

def handler(event, context):
    """
    Netlify Function handler para coletar dados de ações.
    """
    try:
        # Para simplificar o deploy inicial, vamos usar uma variável de ambiente ou uma lista padrão.
        # O ideal é que os tickers venham de uma variável de ambiente do Netlify.
        tickers_str = os.environ.get("TICKERS", "PETR4.SA,VALE3.SA,ITUB4.SA") # Exemplo de tickers
        tickers = [t.strip() for t in tickers_str.split(',') if t.strip()]

        if not tickers:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({"error": "Nenhum ticker especificado. Configure a variável de ambiente TICKERS."}) 
            }

        dados_completos = {}
        for ticker in tickers:
            dados_financeiros = coletar_dados_financeiros_api(ticker)
            dados_completos[ticker] = dados_financeiros
        
        from datetime import datetime
        dados_completos["last_updated"] = datetime.now().isoformat()

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(dados_completos, ensure_ascii=False, indent=4)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": str(e)})
        }