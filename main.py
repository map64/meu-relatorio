import yfinance as yf

def buscar_dados():
    # Lista de ativos que você quer monitorar
    ativos = {
        "Ibovespa": "^BVSP",
        "Vale Debênture (CVRDA6)": "CVRDA6.SA",
        "Vale (VALE3.SA)": "VALE3.SA",
        "Ouro (USD)": "GC=F",
        "Soja (USD)": "ZS=F",
        "Petróleo Brent": "BZ=F",
    }
    
    print(f"--- Relatório de Mercado ---")
    for nome, ticker in ativos.items():
        try:
            acao = yf.Ticker(ticker)
            preco = acao.history(period="1d")['Close'].iloc[-1]
            print(f"{nome}: {preco:.2f}")
        except:
            print(f"{nome}: Não foi possível carregar os dados agora.")

if __name__ == "__main__":
    buscar_dados()
