# Dependencies
import requests
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Logs:
archivo = open("main_logs.txt", "a")

# Current time: 
date_now = round(time.time() * 1000)

cadenaConexion = 'mysql+pymysql://admin:ActTG0suTbdIROlYmwnG@database-bitcoin.c6hom09gkozn.us-east-2.rds.amazonaws.com/coins'

try: 
    # Build daily url
    url_daily = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    btc_daily = requests.get(url_daily).json()

    btc_daily = btc_daily["bitcoin"]["usd"]

    engine = create_engine(cadenaConexion)

    # Base
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    bitcoin_usd = Base.classes.bitcoin_usd

    session = Session(bind=engine)

    coin_x = bitcoin_usd(
        date      = date_now,
        price_usd = btc_daily
    )

    session.add(coin_x)

    session.commit()
    session.close()
    engine.dispose()
    mensaje = f"{date_now} | Success\n"
    print(mensaje)
    archivo.writelines(mensaje)
except Exception as E:
    mensaje = f"{date_now} | Error\n {E}"
    print(mensaje)
    archivo.writelines(mensaje)

archivo.close()