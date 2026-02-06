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
    usuario = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASS')
    
    # DIAGNÓSTICO: Verificando se as senhas estão chegando
    if not usuario or not senha:
        print("ERRO: As credenciais não foram encontradas no cofre (Secrets)!")
        return

    msg = EmailMessage()
    msg.set_content(conteudo)
    msg['Subject'] = f"Relatório Commodities {datetime.now().strftime('%d/%m')}"
    msg['From'] = usuario
    msg['To'] = usuario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(usuario, senha)
            smtp.send_message(msg)
        print("SUCESSO: O Gmail aceitou o e-mail e enviou!")
    except Exception as e:
        print(f"ERRO AO ENVIAR: {e}")

if __name__ == "__main__":
    relatorio = buscar_dados()
    print("Dados coletados. Tentando enviar e-mail...")
    enviar_email(relatorio)
