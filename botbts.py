import time
import requests
import smtplib

from email.mime.text import MIMEText
TOKEN = ""

CHAT_IDS = [
# ID TELEGRAM
]


EMAIL =
PASSWORD =

#Correo del remitente con contraseña (temporal)
DESTINOS = [
## A quien llegaran los dstos (Correo)
]


URLS = [
    "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-07-05-2026/event/1400642AA1B78268",
    "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-09-05-2026/event/1400642AA32C84D5",
    "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-10-05-2026/event/1400642AA32D84D7"
]


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept-Language": "es-MX,es;q=0.9"
}


def telegram(msg):
    for chat_id in CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            r = requests.post(url, data={
                "chat_id": chat_id,
                "text": msg
            })
            print(f"📲 Telegram ({chat_id}) -> {r.status_code}")
        except Exception as e:
            print("❌ Error Telegram:", e)

def correo(msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        for destino in DESTINOS:
            m = MIMEText(msg)
            m["Subject"] = "🚨 BTS BOLETOS DISPONIBLES"
            m["From"] = EMAIL
            m["To"] = destino
            server.send_message(m)

        server.quit()
        print("📧 Correos enviados")

    except Exception as e:
        print("❌ Error correo:", e)

def hay_boletos(html):
    page = html.lower()

    # ❌ BLOQUEAR
    if any(x in page for x in [
        "sold out",
        "agotado",
        "no tickets available",
        "no hay boletos"
    ]):
        return False

    
    señales = [
        "find tickets",
        "comprar boletos",
        "ticket selection",
        "map",
        "seat"
    ]

    if any(x in page for x in señales):
        return True

    return False

print(" BOT BTS 24/7 ")

telegram("BOT BTS ACTIVO ")

while True:
    try:
        for URL in URLS:
            print(" Revisando:", URL)

            r = requests.get(URL, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("⚠️ Error página:", r.status_code)
                continue

            if hay_boletos(r.text):

                mensaje = f"""🚨 BTS ALERTA 🚨 🔥 POSIBLE BOLETO DISPONIBLE 🔥 {URL}
"""
                

                telegram(mensaje)
                correo(mensaje)

                print("🚨 BOLETOS DETECTADOS 🚨")

                time.sleep(300)

        print("⏳ esperando...")
        time.sleep(20)

    except Exception as e:
        print("❌ Error general:", e)
        time.sleep(60)
