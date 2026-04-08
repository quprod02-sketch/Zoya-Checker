import streamlit as st
import pandas as pd
import time
from playwright.sync_api import sync_playwright
st.title("Zoya Shariah Checker (Accurate)")
input_tickers = st.text_area("Enter tickers", "AAPL, NVDA, XOM")
def check_ticker(ticker, page):
   url = f"https://zoya.finance/stocks/{ticker.lower()}"
   try:
       page.goto(url, timeout=60000)
       page.wait_for_timeout(3000)  # wait for JS to load
       content = page.inner_text("body").lower()
       if "not Shariah-compliant" in content:
           return "Not Shariah-compliant"
       elif "Shariah-compliant" in content:
           return "Shariah-compliant"
       else:
           return "Unknown"
   except:
       return "Error"

if st.button("Check Compliance"):
   tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]
   results = []
   progress = st.progress(0)
   with sync_playwright() as p:
       browser = p.chromium.launch(headless=True)
       page = browser.new_page()
       for i, ticker in enumerate(tickers):
           status = check_ticker(ticker, page)
           results.append((ticker, status))
           progress.progress((i + 1) / len(tickers))
           time.sleep(2)  # safe delay
       browser.close()
   df = pd.DataFrame(results, columns=["Ticker", "Status"])
   st.dataframe(df)
   csv = df.to_csv(index=False).encode("utf-8")
   st.download_button("Download CSV", csv, "results.csv")
