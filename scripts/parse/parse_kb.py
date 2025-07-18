import pandas as pd

# 1. CSV 파일 불러오기 (한글 깨짐 방지용 cp949 인코딩 사용)
df = pd.read_csv("data/raw/kb_transactions.csv", encoding="cp949")

# 2. 컬럼명 수동 지정
df.columns = ['date', 'type', 'merchant', 'memo', '출금액', '입금액', '잔액', 'bank', '구분']

# 3. 출금액 / 입금액을 하나의 amount 컬럼으로 통합 (출금: 음수, 입금: 양수)
df['출금액'] = df['출금액'].replace('-', '0').astype(str).str.replace(',', '')
df['입금액'] = df['입금액'].replace('-', '0').astype(str).str.replace(',', '')
df['amount'] = df['입금액'].astype(float) - df['출금액'].astype(float)

# 4. 날짜 형식 변환
df['date'] = pd.to_datetime(df['date'], format="%Y.%m.%d %H:%M:%S", errors='coerce')

# 5. 표준 컬럼 구성
df['category'] = ''  # 라벨링은 추후 수동 작업
df['bank'] = '국민은행'  # 모든 행에 동일하게 '국민은행' 입력
df = df[['date', 'amount', 'merchant', 'category', 'type', 'bank']]

# 6. 파생 컬럼 생성
df['day_of_week'] = df['date'].dt.dayofweek  # 월(0) ~ 일(6)
df['hour'] = df['date'].dt.hour

# 시간대 매핑
def time_cat(hour):
    if 0 <= hour < 6:
        return 'night'
    elif 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'evening'

df['time_category'] = df['hour'].apply(time_cat)
df['period_code'] = df['date'].dt.strftime('%Y-W%U')             # 예: 2025-W27
df['period_range'] = df['date'].dt.to_period("W").astype(str)    # 예: 2025-07-07/2025-07-13

# 7. 컬럼 순서 정리
df = df[[
    'date', 'amount', 'merchant', 'category', 'type', 'bank',
    'day_of_week', 'hour', 'time_category', 'period_code', 'period_range'
]]

# 8. 저장
df.to_csv("data/parsed/kb_parsed.csv", index=False, encoding="utf-8-sig")
print("✅ 국민은행 파싱 완료! → data/parsed/kb_parsed.csv")
