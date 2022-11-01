from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
import os

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return f'''
    Welcome BitcoinAPI
    '''

@app.route("/bictoin_usd")
def return_show_info():

    engine = create_engine("sqlite:///./data/coins.sqlite")
    Base   = automap_base()

    Base.prepare(engine, reflect=True)

    bitcoin_usd = Base.classes.bitcoin_usd
    session     = Session(bind=engine)

    # TODO: Improve query
    results     = (
        session
        .query(bitcoin_usd.date, bitcoin_usd.price_usd)
        .all()
    )

    results           = [{"date":x[0], "price": x[1]} for x in results]
    results           = pd.DataFrame(results)
    results["date"]   = pd.to_datetime(results["date"], unit="ms")

    # Filter Q1
    results                = results.query("date>='2022-01-01' and date<='2022-03-31'")
    results["date_string"] = results["date"].dt.strftime("%Y-%m-%d")

    # Group by
    results = results.groupby("date_string")[["price"]].mean().reset_index()

    # 5-days period
    period = 0
    date_period = results.loc[0,"date_string"]
    for x in range(len(results)):
        if period==5: 
            period=0
            date_period = results.loc[x,"date_string"]

        period += 1
        results.loc[x,"period"] = date_period

    results = results.groupby("period")[["price"]].mean().reset_index().to_dict(orient="row")

    session.close()
    engine.dispose()

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)






