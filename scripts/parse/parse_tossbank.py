import pandas as pd

# 1. CSV 불러오기
df = pd.read_csv("data/raw/tossbank_transactions.csv", encoding="cp949")

# 2. 컬럼명 정리 (원본 → 표준 컬럼)
df = df.rename(columns={
    "거래 일시": "date",
    "적요": "merchant",
    "거래 유형": "type",
    "거래 금액": "amount"
})

# 2-1. 은행 출처 컬럼 추가 (고정값으로 설정)
df["bank"] = "토스뱅크"

# 3. date → datetime 형식으로 변환
df["date"] = pd.to_datetime(df["date"], format="%Y.%m.%d %H:%M:%S")

# 4. 금액 양수/음수 정리
# 이미 음수/양수 구분이 되어 있으므로 float으로 변환만 해줌
df["amount"] = df["amount"].astype(str).str.replace(",", "")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  # NaN이 있는 경우 제거 위해

# 5. 필요 없는 컬럼 제거 (계좌번호, 잔액 등)
df = df[["date", "amount", "merchant", "type", "bank"]]

# 6. 카테고리 컬럼 추가 (현재는 공란 → 라벨링 단계에서 채움)
df["category"] = ""

# 7. 파생 컬럼 추가
df["day_of_week"] = df["date"].dt.dayofweek         # 월(0) ~ 일(6)
df["hour"] = df["date"].dt.hour                     # 시(0~23)

# 시간대 라벨링 함수
def time_cat(hour):
    if 0 <= hour < 6:
        return "night"
    elif 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    else:
        return "evening"

df["time_category"] = df["hour"].apply(time_cat)

# 주차 구분 (분석용/출력용 둘 다 생성)
df["period_code"] = df["date"].dt.strftime("%Y-W%U")                      # 분석용: 2025-W24
df["period_range"] = df["date"].dt.to_period("W").astype(str)            # 시각화용: 2025-06-09/2025-06-15

# 8. 컬럼 순서 재정렬
df = df[[
    "date", "amount", "merchant", "category", "type", "bank",
    "day_of_week", "hour", "time_category", "period_code", "period_range"
]]

# 9. 저장
df.to_csv("data/parsed/tossbank_parsed.csv", index=False, encoding="utf-8-sig")

print("✅ 토스뱅크 파싱 완료! → data/parsed/tossbank_parsed.csv")
