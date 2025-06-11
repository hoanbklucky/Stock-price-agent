from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import yfinance as yf

def get_stock_price(ticker: str):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", "Price not available")
    return {"price": price, "ticker": ticker}

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A simple agent that get stock price.',
    instruction="""You are a stock price assistant. Always use the get_stock_price tool.
                Include the ticker symbol in your response""",
    tools=[get_stock_price]
)

""" app = AdkApp(agent=root_agent)

for event in app.stream_query(
    user_id="USER_ID",
    message="Apple stock price today",
):
    print(event)
 """