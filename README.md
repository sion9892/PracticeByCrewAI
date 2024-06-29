CrewAI를 활용하여 주식 투자 하기

참고 레퍼런스
: 노마드코더 https://www.youtube.com/watch?v=-59bKxwir5Q&t=301s 
이 영상을 보고 클린 코딩함.
그외 crewAI 공식문서, 구글링 등

목표
: 어떤 종목에 대한 buy/sell/hold와 그 근거가 담긴 보고서

설계
1. Agents
    Researcher : 해당 종목에 대한 최신 뉴스를 조사.
    Technical Analyst  : 주식의 움직임을 분석하여 추세, 진입 시점 및 수준에 대한 인사이트를 제공.
    Financial Analyst : 재무재표를 사용하여 주식의 재무 건전성과 성과를 평가하라고 지시.
    Hedge fund manger :  researcher, technical analyst, financial analyst의 보고서를 읽고 최종적으로 해당 종목에 대한 buy/sell/hold 결정을 내림.

2. Tasks
   Research, Technical analysis, Financial analysis, Investment recommendation
   
4. Tools
   For Researcher : scrape_tool, stock_news
   For Technical Analyst : stock_prices
   For Financial Analyst : insider_transactions, income_stmt, balence_sheet
   For Hedge fund manger : Nothing




