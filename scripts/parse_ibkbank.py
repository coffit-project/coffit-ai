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
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

df["time_category"] = df["hour"].apply(get_time_category)

df["period_code"] = df["date"].dt.strftime("%Y-W%U")                      # 분석용: 2025-W24
df["period_range"] = df["date"].dt.to_period("W").astype(str)            # 시각화용: 2025-06-09/2025-06-15


df["category"] = df["merchant"].fillna("").apply()
df["bank"] = "기업은행"

# 표준 스키마로 정리
df_final = df[[
    "date", "amount", "merchant", "category", "type",
    "bank", "day_of_week", "hour", "time_category", "period_code", "period_range"
]]

df_final.to_csv("../data/parsed/ibk_parsed.csv", index=False, encoding='utf-8-sig')

# 결과 미리 보기
print(df_final.head())
