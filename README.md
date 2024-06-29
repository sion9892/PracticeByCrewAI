<div>
<h2>CrewAI를 활용하여 주식 투자 하기</h2>
</div>
<br>

<div>
<h3>목표</h3>
: 어떤 종목에 대한 buy/sell/hold와 그 근거가 담긴 보고서
</div>

<div>
<h3>설계</h3>
<h4>1. Agents</h4>
    Researcher : 해당 종목에 대한 최신 뉴스를 조사. <br>
    Technical Analyst  : 주식의 움직임을 분석하여 추세, 진입 시점 및 수준에 대한 인사이트를 제공.  <br>
    Financial Analyst : 재무재표를 사용하여 주식의 재무 건전성과 성과를 평가하라고 지시.  <br>
    Hedge fund manger :  researcher, technical analyst, financial analyst의 보고서를 읽고 최종적으로 해당 종목에 대한 buy/sell/hold 결정을 내림.  <br>
<br>
<h4>2. Tasks</h4>
   Research, Technical analysis, Financial analysis, Investment recommendation  <br>
<br>
<h4>3. Tools</h4>
   For Researcher : scrape_tool, stock_news  <br>
   For Technical Analyst : stock_prices  <br>
   For Financial Analyst : insider_transactions, income_stmt, balence_sheet  <br>
   For Hedge fund manger : Nothing  <br>
<br>
</div>

<div>
<h3>참고 레퍼런스</h3>
: 노마드코더 https://www.youtube.com/watch?v=-59bKxwir5Q&t=301s <br>
이 영상을 보고 클린 코딩함. <br>
그외 crewAI 공식문서, 구글링 등 <br>
</div>












