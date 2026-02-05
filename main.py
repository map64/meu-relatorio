import yfinance as yf
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

def buscar_dados():
    ativos = {
        "Ibovespa": "^BVSP",
        "Vale Debênture (CVRDA6)": "CVRDA6.SA",
        "Ouro (USD)": "GC=F",
        "Soja (USD)": "ZS=F"
    }
    
    corpo = f"Resumo de Mercado - {datetime.now().strftime('%d/%m/%Y')}\n\n"
    for nome, ticker in ativos.items():
        try:
            acao = yf.Ticker(ticker)
            preco = acao.history(period="1d")['Close'].iloc[-1]
            corpo += f"{nome}: {preco:.2f}\n"
        except:
            corpo += f"{nome}: Dados indisponíveis\n"
    return corpo

def enviar_email(conteudo):
    # O GitHub vai pegar os dados do "Cofre" (Secrets) que você configurou
    usuario = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASS')

    msg = EmailMessage()
    msg.set_content(conteudo)
    msg['Subject'] = f"Relatório Commodities {datetime.now().strftime('%d/%m')}"
    msg['From'] = usuario
    msg['To'] = usuario # Envia para você mesmo

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(usuario, senha)
        smtp.send_message(msg)

if __name__ == "__main__":
    relatorio = buscar_dados()
    enviar_email(relatorio)
    print("E-mail enviado com sucesso!")
