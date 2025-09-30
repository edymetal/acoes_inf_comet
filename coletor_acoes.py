import json
import yfinance as yf
import pandas as pd

def coletar_dados_financeiros_api(ticker_symbol):
    """
    Coleta os dados financeiros (informações e histórico) de um ticker
    usando a biblioteca yfinance.
    """
    print(f"Buscando dados financeiros para {ticker_symbol} via API yfinance...")
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

    print("Dados financeiros obtidos com sucesso.")
    return {"info": info, "historico": hist_json}

def main():
    """
    Função principal para orquestrar a coleta de dados para múltiplos tickers.
    """
    try:
        with open('acoes.txt', 'r', encoding='utf-8') as f:
            tickers = [line.strip() for line in f if line.strip()]
        print(f"Tickers a serem processados: {tickers}")
    except FileNotFoundError:
        print("Erro: Arquivo 'acoes.txt' não encontrado. Crie o arquivo com um ticker por linha.")
        return

    dados_completos = {}
    for ticker in tickers:
        print(f"--- Iniciando a coleta de dados para o ticker: {ticker} ---")
        dados_financeiros = coletar_dados_financeiros_api(ticker)
        dados_completos[ticker] = dados_financeiros
        print(f"--- Coleta para {ticker} finalizada. ---")

    # Adiciona a data e hora da última atualização
    from datetime import datetime
    dados_completos["last_updated"] = datetime.now().isoformat()

    output_filename = "dados_acoes.json"
    print(f"\nSalvando todos os dados em {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=4)
    
    # Adiciona a data e hora da última atualização
    from datetime import datetime
    dados_completos["last_updated"] = datetime.now().isoformat()

    output_filename = "dados_acoes.json"
    print(f"\nSalvando todos os dados em {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=4)
    
    print(f"Dados salvos com sucesso. Verifique o arquivo {output_filename}.")
    print("Processo finalizado.")

if __name__ == "__main__":
    main()
