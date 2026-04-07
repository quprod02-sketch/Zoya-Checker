import streamlit as st
import requests
import pandas as pd
import time
st.set_page_config(page_title="Zoya Shariah Checker (API)", layout="wide")
st.title("🕌 Zoya Shariah Compliance Checker (Fast API Version)")
st.write("Enter stock tickers (comma-separated) to check Shariah compliance using Zoya API.")
input_tickers = st.text_area("Tickers", "AAPL, NVDA, XOM, TSLA, MU, TSM, CVX")
# NOTE: This endpoint is inferred from network calls (may change in future)
def check_ticker_api(ticker):
   url = f"https://zoya.finance/api/stocks/{ticker.lower()}"
   headers = {
       "User-Agent": "Mozilla/5.0",
       "Accept": "application/json"
   }
   try:
       response = requests.get(url, headers=headers, timeout=15)
       if response.status_code != 200:
           return "Error"
       data = response.json()
       # Adjust based on actual API structure
       status = data.get("compliance", "unknown").lower()
       if "not" in status:
           return "Not Shariah-compliant"
       elif "compliant" in status:
           return "Shariah-compliant"
       else:
           return "Unknown"
   except Exception:
       return "Error"

if st.button("Check Compliance"):
   tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]
   results = []
   progress = st.progress(0)
   for i, ticker in enumerate(tickers):
       status = check_ticker_api(ticker)
       results.append((ticker, status))
       progress.progress((i + 1) / len(tickers))
       time.sleep(0.2)  # small delay to be safe
   df = pd.DataFrame(results, columns=["Ticker", "Status"])
   st.success("Completed!")
   st.dataframe(df)
   csv = df.to_csv(index=False).encode("utf-8")
   st.download_button("Download CSV", csv, "zoya_results.csv", "text/csv")
st.markdown("---")
st.caption("⚠️ This uses an unofficial API endpoint inferred from Zoya. It may change anytime.")
