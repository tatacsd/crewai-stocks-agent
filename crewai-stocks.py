# Import libs
import json
import os
from datetime import datetime
import ipykernel 
import yfinance as yf

from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool

# Get openai from langchain
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults

# Use streamlit to create a web app
import streamlit as st

# Create Yahoo Finance tool

# Get the ticket - Stock - using yfinance
def fetch_stock_price(ticket):
    data = yf.download(ticket, start='2023-08-22', end='2024-08-22')
    return data

# Create a tool for crewai to use
yahoo_finance_tool = Tool(
    name='Yahoo Finance Tool',
    description='Fetch the last year of historical prices for a specific stock ({ticker}) from the Yahoo Finance API.',
    func = lambda ticket: fetch_stock_price(ticket)
)

# Import OpenAi LLM - GPT
os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(model="gpt-3.5-turbo" )

# Create Agent
agentStockPriceAnalysis = Agent(
    role="Senior Stock Price Analyst",
    goal="Find the {ticket} stock price and analyses trends",
    backstory="""You are highly experienced in analyzing the price of a specific stock and make predictions about its future price.""",
    verbose=True,
    llm=llm,
    max_iter=5,
    memory=True,
    allow_delegation=False,
    tools=[yahoo_finance_tool]
)

# Create a Task for the agent
getStockPriceTask = Task(
    description="Analyze the stock {ticket} price history and create a trend analysis of up, down or sideways.",
    expected_output="""Specify the current trend stock price - up, down or sideways
    eg. "APPL stock price is going up" or "APPL stock price is going down" or "APPL stock price is sideways".""",
    agent=agentStockPriceAnalysis
)

# Import Search tool
search_tool = DuckDuckGoSearchResults(backend='news', num_results=10)

# Create a Agent to analyze the news
agentNewsAnalyst = Agent(
    role="Senior Stock News Analyst",
    goal="""Create a short summary of the market new related to the stock {ticket} company. Specify the current trend - up, down or sideways with the news context.
    For each requested asset, specify a number between 0 and 100, where 0 means extreme fear and 100 means extreme greed.
    """,
    backstory="""You are highly experienced in analyzing the marketing trends and news and have tracked assets for more than 10 years.
    
    you are also master level analyst in traditonal market and have deep understand of human psychology.

    You understand news, their titles and information, but you look at those with health dose of skepticism.

    You consider also the source of the news articles.
    """,
    verbose=True,
    llm=llm,
    max_iter=10,
    memory=True,
    allow_delegation=False,
    tools=[search_tool]
)

getNewsTask = Task(
    description=f"""Take the stock and always include BTC to it, if not requested,
    use search tool to search each one individually.

    The current date is {datetime.now()}.

    Compose a helpful report.
    
    """,
    expected_output="""a summary of the overall market and one sentence summary for each request asset.

    Include a fear/greed score for each asset based on the news and market sentiment. Use the format:
    <STOCK ASSET>
    <ONE SENTENCE SUMMARY BASED ON NEWS>
    <TREND PREDICTION - UP, DOWN, SIDEWAYS>
    <FEAR/GREED SCORE>
    
    """,
    agent=agentNewsAnalyst
)


stockAnalystWriterAgent = Agent(
    role="""Senior Stock Analyst Writer""",
    goal="""Analyze the trends prices and news and write insightful compelling and informative three paragraph long newsletter based on the stock report and price trend.""",
    backstory="""You are widely accepted as the best stock analyst in the market. You understand complex concepts and create compling stories and narratives that resonates 
    with wider audiences.
    You understand macro factros and combine theories - eg. cycle theory and fundamental analysis. You are able to hold multiples opnioins when analyzing anything.
    """,
    verbose=True,
    llm=llm,
    max_iter=5,
    memory=True,
    allow_delegation=True
)

writeAnalysisTask = Task(
    description="""Use the stock price trend and the stock news report to create an analyses and write the newsletter about the {ticket} 
    company that is brief and highligh the most important points.
    Focus on the stock price trend, news and frea/greed socre. What are the newa future considerations?
    Include the previous analyses of stock and news sumary.
    """,
    expected_output="""An eloquent 3 paragraphs newsletter formated as markdown in an easy redable manner. It should contain:
    - 3 bullets executive summary
    - Introduction - set overall picture and spike up the interest
    - main part provides the meat of the analysis including the news summary and fear/greed scores
    - summary - key facts and concrete future trend predictions - up, down or sideways.
    """,
    agent=stockAnalystWriterAgent,
    context=[getStockPriceTask, getNewsTask]
)

crew = Crew(
    agents =[agentStockPriceAnalysis, agentNewsAnalyst, stockAnalystWriterAgent], # Add the agents to the crew
    tasks =[getStockPriceTask, getNewsTask, writeAnalysisTask], # Add the tasks
    verbose = True, # Set verbose to True
    process = Process.hierarchical, # Set the process to hierarchical
    full_output=True, # Set full_output to True
    share_crew=False, # Set share_crew to False
    manager_llm=llm, # Set the manager_llm to the LLM
    max_iter=15 # Set the max_iter to 15
)



with st.sidebar:
    st.header("Enter The Stock To Analyze")
    with st.form(key='search_form'):
        ticket = st.text_input("Select the ticket")
        submit_button = st.form_submit_button(label='Submit')
if submit_button:
    if not ticket:
        st.error("Please enter a ticket")
    else:
        results = crew.kickoff(
            inputs={
                "ticket": ticket
            }
        )
        st.subheader("Results of your analysis")
        st.write(results['final_output'])

