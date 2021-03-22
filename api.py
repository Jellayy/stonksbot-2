from polygon import RESTClient
import pandas as pd
from datetime import datetime
import datetime as dt
import pytz
import asyncio
import VERY_SECRET_LAUNCH_CODES


async def get_polygon_dataframe(ticker, fromdate, todate):
    key = VERY_SECRET_LAUNCH_CODES.HYDROGEN_LAUNCH_CODE()
    with RESTClient(key) as client:
        resp = client.stocks_equities_aggregates(ticker=ticker, from_=fromdate, to=todate, multiplier="5",
                                                 timespan="minute")
        data = resp.results
        # print(data)
        if data:
            for i in data:
                # print(i["t"], i["vw"])
                date = datetime.fromtimestamp(i["t"] / 1000, tz=pytz.timezone('US/Eastern')).strftime("%Y-%m-%d "
                                                                                                      "%H:%M:%S")
                i["t"] = date
                # print(i)
            df = pd.DataFrame.from_dict(data).rename(
                columns={"v": "Volume", "vw": "Average", "o": "Open", "c": "Close", "h": "High", "l": "Low",
                         "t": "Time"}).set_index("Time")
            if 'n' in df.columns:
                df = df.drop(columns=["n"])
                return df
            else:
                # print(df)
                return df
        else:
            print(data)
            print("Dictionary is empty")
            return False


# print(asyncio.run(get_polygon_dataframe("GME", "2021-03-07", "2021-03-14")))
