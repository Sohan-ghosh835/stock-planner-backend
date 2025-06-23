from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
from userdb import register_user, login_user, save_search, save_investment, get_user_data
from predictor import predict_prices
from analyzer import calculate_indicators
from ai_guide import generate_advice

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class AuthDetails(BaseModel):
    email: str
    password: str

class Investment(BaseModel):
    user_id: str
    ticker: str
    note: str

@app.post("/register")
def register(data: AuthDetails):
    return register_user(data.email, data.password)

@app.post("/login")
def login(data: AuthDetails):
    return login_user(data.email, data.password)

@app.get("/user/{user_id}")
def get_user(user_id: str):
    return get_user_data(user_id)

@app.post("/invest")
def add_investment(investment: Investment):
    save_investment(investment.user_id, investment.ticker, investment.note)
    return {"message": "Investment saved"}

@app.get("/stock/{ticker}/{user_id}")
def get_stock_data(ticker: str, user_id: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    close_prices = hist['Close'].dropna()
    prediction = predict_prices(close_prices)
    save_search(user_id, ticker)
    return {
        "latest_price": close_prices.iloc[-1],
        "history": close_prices.to_dict(),
        "predicted": prediction
    }

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
    close_prices = hist['Close'].dropna()
    return calculate_indicators(close_prices)

@app.get("/ai-guide/{ticker}")
def ai_guide(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
    close_prices = hist['Close'].dropna()
    indicators = calculate_indicators(close_prices)
    return {"message": generate_advice(indicators)}
