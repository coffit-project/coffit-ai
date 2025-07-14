import pandas as pd

# 엑셀 파일 불러오기 (.xls 형식)
df = pd.read_excel("../data/raw/ibk_transactions.xls", header=None, names=[
    "date", "withdraw", "deposit", "merchant",
    "message", "type", "bank"
], engine='xlrd')  # ⚠️ xlrd가 설치되어 있어야 함

# 금액 통합 (입금은 +, 출금은 -)
def parse_amount(val):
    if pd.isna(val):
        return 0
    if isinstance(val, str):
        return float(val.replace(",", "").replace("원", "").strip())
    return float(val)

df["withdraw"] = df["withdraw"].apply(parse_amount)
df["deposit"] = df["deposit"].apply(parse_amount)

df["amount"] = df["deposit"] - df["withdraw"]

# 날짜 파싱
df["date"] = pd.to_datetime(df["date"])
df["day_of_week"] = df["date"].dt.dayofweek
df["hour"] = df["date"].dt.hour

def get_time_category(hour):
    if 5 <= hour < 11:
        return "오전"
    elif 11 <= hour < 17:
        return "오후"
    elif 17 <= hour < 21:
        return "저녁"
    else:
        return "새벽"

df["time_category"] = df["hour"].apply(get_time_category)

df["period_code"] = df["date"].dt.strftime("%Y-W%U")                      # 분석용: 2025-W24
df["period_range"] = df["date"].dt.to_period("W").astype(str)            # 시각화용: 2025-06-09/2025-06-15

# 카테고리 분류
def classify_category(merchant):
    if any(keyword in merchant for keyword in ["커피", "카페", "A.M카페", "다방", "공차", "달다곰이", "탐앰탐스", "이디야", "투썸", "메머드", "핫브레드"]):
        return "카페"
    elif any(keyword in merchant for keyword in ["피코야", "분식", "치킨", "식당", "한솥", "KFC", "라멘", "마트", "이자카야", "롯데리아", "CU", "세븐", "맥도날드", "파리바개뜨", "버거킹", "밥", "버거", "김밥", "양식", "차돌", "마라탕", "연어", "냉면", "GS25", "떡볶이", "씨유"]):
        return "식비"
    elif any(keyword in merchant for keyword in ["하이힐", "의류", "쇼핑", "이랜드"]):
        return "의류"
    elif any(keyword in merchant for keyword in ["후불교통", "지하철", "버스", "택시", "기후동행"]):
        return "교통"
    else:
        return "기타"

df["category"] = df["merchant"].fillna("").apply(classify_category)
df["bank"] = "기업은행"

# 표준 스키마로 정리
df_final = df[[
    "date", "amount", "merchant", "category", "type",
    "bank", "day_of_week", "hour", "time_category", "period_code", "period_range"
]]

df_final.to_csv("../data/parsed/ibk_parsed.csv", index=False, encoding='utf-8-sig')

# 결과 미리 보기
print(df_final.head())
