# 📈 Crewai Stocks Analysis
This project is a stock market analysis tool that leverages machine learning and financial data APIs to generate insightful stock trend analyses and news summaries. Built using LangChain and OpenAI's GPT models, it fetches stock prices, analyzes news, and creates a comprehensive newsletter for stock analysis.

This project was developed as part of the Machine Learning and AI classes from [Rocketseat](https://rocketseat.com.br)

---

## 🚀 Features

- **Stock Price Retrieval**: Fetches the last year's stock prices using the `yfinance` API.
- **News Analysis**: Finds the latest news about the stock and evaluates the market sentiment (fear or greed).
- **AI-Generated Report**: Creates a concise report including price trends, news summaries, and a fear/greed score using AI agents.
- **Interactive Web App**: Built with **Streamlit**, allowing users to input a stock ticker and get real-time analysis.

---

## 🛠️ How It Works

1. **Stock Price Retrieval**: Enter a stock ticker (e.g., `AAPL` for Apple), and the app fetches the last year of stock prices from Yahoo Finance.
   
2. **Trend Analysis**: An AI agent evaluates the stock’s price history to identify if the price is trending up, down, or remaining stable.

3. **News Sentiment Analysis**: Another AI agent searches for the latest news about the stock and provides a sentiment analysis (fear or greed).

4. **Report Generation**: The final AI agent synthesizes the stock price trend and news sentiment into a brief, three-paragraph newsletter-style report.

---

## 📂 Project Structure

- **`crewai-stocks.py`**: The main file handling stock data retrieval, analysis, and report generation.
- **`requirements.txt`**: Contains all the necessary Python packages to run the project.
---

## 🛠️ Technologies Used

- **Python**: Core programming language.
- **[yfinance](https://pypi.org/project/yfinance/)**: API for fetching stock data from Yahoo Finance.
- **[LangChain](https://python.langchain.com/)**: Framework to build AI agents using OpenAI's GPT models.
- **[Streamlit](https://streamlit.io/)**: Framework for building the interactive web interface.
- **[DuckDuckGo Search Tool](https://pypi.org/project/duckduckgo-search/)**: Used for fetching the latest news articles about the stock.

---

## 📥 Installation
You'll need to install [Python](https://www.python.org/downloads/) on your computer to set up and run the project locally. 

To set up and run the project locally:
1. Clone the repository
```bash
git clone https://github.com/tatacsd/crewai-stocks-agent.git
```

2. navigate to the project directory:
```bash
cd crewai-stocks-agent
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. run Streamlit app:
```bash
streamlit run crewai-stocks.py
```

5. The application will open in your web browser. You can also access it via `http://localhost:8501`.




## 📝 How to Use
1. Open the Streamlit app and enter a stock ticker (e.g., AAPL, TSLA).
2. The app will analyze the stock’s price history and related news.
3. The results will be displayed in a report format, including price trends, news summaries, and sentiment analysis.

## 📈 Example Tickers
Here are some example stock tickers you can try:

`AAPL`: Apple Inc.
`TSLA`: Tesla, Inc.
`AMZN`: Amazon.com, Inc.
