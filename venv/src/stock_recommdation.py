import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool, ScrapeWebsiteTool
import yfinance as yf 

# .env 파일로부터 환경 변수 로드
load_dotenv()

# 환경 변수 사용
api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY: {api_key}")

# 야후 파이낸스에서 가져온 주식 뉴스와 툴
ticker = yf.Ticker("GME")
scrape_tool = ScrapeWebsiteTool()

@tool("Stock News") # 주식 뉴스
def stock_news(ticker):
    """
    useful to get news about a stock.
    the input should be a ticker, for example AAPL, NET.
    """
    #인수는 ticker여야한다. ex) AAPL(애플)
    ticker = yf.Ticker(ticker)
    return ticker.news

@tool("Stock Price") # 주식 가격 차트
def stock_prices(ticker):
    """
    useful to get stock price data.
    the input should be a ticker, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

@tool("Income Statement") # 소득명세서
def income_stmt(ticker):
    """
    useful to get income statement of a company.
    the input should be a ticker, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.income_stmt

@tool("Balence Sheet") #대차대조표
def balence_sheet(ticker):
    """
    useful to get balence sheet.
    the input should be a ticker, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.balance_sheet

@tool("Insider Transactions") #내부자 거래
def insider_transactions(ticker):
    """
    useful to get insider transactions.
    the input should be a ticker, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.insider_transactions


#agent 설정
researcher = Agent(
            role="Researcher",
            goal="""Gather and interpret vast amounts of data 
                    to provide a comprehensive overview of the sentiment 
                    and news surrounding a stock""",
            #목표: 데이터를 수집하고 해석하여 주식을 둘러싼 정서와 뉴스를 파악
            backstory="""you're skilled in gathering and interpreting data from various sources. 
                        you read each data source carefully and extract the most important information. 
                        your insights are crucial for making informed investment decidions""",
            #배경: 다양한 출처에서 해석하는데 능숙하며 뉴스를 주의깊게 읽고 가장 중요한 정보를 추출가능함.
            tools=[
                scrape_tool,
                stock_news
            ],
);  

technical_analyst = Agent(
            role="Technical Analyst",
            goal="""analyze the movements of a stock 
                    and provide insights on trends, entry points, resistance and support levels""",
            #목표: 주식의 움직임을 분석하여 추세, 진입 시점 및 수준에 대한 인사이트를 제공하는 목표
            backstory="""an expert in technical analysis, you're known for your your ability to predict stock prices. 
                        you provide valuable insights to your customers""",
            #배경: 주식 움직임을 예측하는 전문가이며, 제공하는 인사이트가 고객에게 매우 가치가 있음.
             tools=[
                stock_prices
            ],
);

financial_analyst = Agent(           
            role="Financial Analyst",
            goal="""use financial statements, insider trading data
                    and other metrics to evaluate a stock's financial
                    health and performance""",
            #목표: 재무재표를 사용하여 주식의 재무 건전성과 성과를 평가하라고 지시
            backstory="""you're a very experienced investment advisor
                        that looks at a company's financial health,
                        market sentiment, and qualitative data to
                        make informed recommendations""",
            #배경: 회사의 재무건정성을 기반으로 추천을 하는 숙련된 투자전문가
             tools=[
                insider_transactions,
                income_stmt,
                balence_sheet
            ],
);

hedge_fund_manager = Agent(
            role="Hedge Fund Manager",
            goal="""manage a portfolio of stocks and make investment decisions 
            to maximize returns using insights from financial analysts and researchers""",
            #목표: 주식 포트폴리오를 관리하고, 수익을 극대화하기  
            backstory="""you're a seasoned hedge fund manager with a proven track record of 
            making profitable investments. you always impress your clients""",
            #배경: 수익성 있는 투자 결정을 내린 실적이 있고 너의 고객들을 항상 너를 믿음.
            verbose=True,
            #다른 에이전트들의 보고서를 보기 때문에 도구가 필요없음.
);

research = Task(
        description="""gather and analze the latest news and market sentiment surrounding
        {company}'s stock. provide a summary of the news and any notable shifts in sentimemt""",
        #작업설명: 해당 종목을 둘러싼 최신 뉴스와 시장 심리를 수집하고 분석
        agent=researcher, 
        #작업자
        expected_output="""your final answer MUST be a detailed summary of the news and market
        sentiment surrounding the stock""",
        #예상결과물: 해당 종목을 둘러싼 뉴스와 시장심리를 요약한 보고서
)

technical_analysis = Task(
        description="""conduct a technical analysis of the {company} stock price movements 
                        and identify key support and resistance levels chart patterns""",
        #작업설명: 주식의 가격 움직임을 살펴보고 주요 지지선, 저항성 및 차트 패턴을 식별
        agent=technical_analyst,
        expected_output="""your final answer MUST be a report with potential entry points, price targets 
        and any other relevant information""",
        #예상결과물: 잠재적 진입 지점과 가격 목표가 포함된 보고서
)

financial_analysis = Task(
        description="""analyze the {company}'s financial statements, balance sheet, insider trading data
                        and other metrics to evaluate {company}'s financial health and performance""",
        #작업설명: 회사의 재무제표와 내부자 거래 데이터를 살펴보기
        agent=financial_analyst,
        expected_output="""your final answer MUST be a report with an overview 
                        of {company}'s revenue, earnings, cash flow, and other key financial metrics""",                       
        #예상결과물: 회사의 매출, 수익, 현금 흐름, 및 기타 재무 재표가 포함된 보고서
)

investment_recommendation = Task(
        description="""based on the research, technical analysis, and financial analysis reports, 
                        provide a detailed investment recommendation for {company} stock""",
        #작업설명: 이전 에이전트가 수행한 모든 리서치와 보고서를 바탕으로 주식을 매수, 매도 또는 보유하도록 투자 추천
        agent=hedge_fund_manager,
        expected_output="""your final answer MUST be a detailed recommendation to BUY, SELL, or HOLD the stock.
                        provide a clear retionale for your recommendation""",
                        
        #예상결과물: 주식을 매수, 매도 또는 보유 중 하나와 그 이유를 제공하는 최종 보고서
        context = [
            research,
            technical_analysis,
            financial_analysis,
        ],
        output_file="investment_recommendation.md",
)

crew = Crew(
    tasks=[
        research,
        technical_analysis,
        financial_analysis,
        investment_recommendation
    ],
    agents=[
        researcher,
        technical_analyst,
        financial_analyst,
        hedge_fund_manager
    ],
    verbose=2, # 진행 어떻게 되는지 확인
)

result = crew.kickoff(
    inputs={
        "company":"TQQQ" #분석하려는 회사 이름을 넣기
    }
)

print('result:', result)