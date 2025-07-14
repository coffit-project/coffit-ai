import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

input_path = os.path.join(BASE_DIR, 'data', 'raw', 'shinhan_transactions.xls')
output_path = os.path.join(BASE_DIR, 'data', 'parsed', 'shinhan_parsed.csv')

df = pd.read_excel(input_path)

df['date'] = pd.to_datetime(df['거래일'])
df['amount'] = df['금액']
df['merchant'] = df['가맹점명']
df['category'] = ''  # 공란 처리
df['type'] = df['이용구분']
df['bank'] = '신한'

df['day_of_week'] = df['date'].dt.weekday
df['hour'] = df['date'].dt.hour
df['time_category'] = df['hour'].apply(
    lambda x: 'night' if 0 <= x < 6 else
              'morning' if 6 <= x < 12 else
              'afternoon' if 12 <= x < 18 else
              'evening'
)

# 주차 구분 (분석용/출력용 둘 다 생성)
df["period_code"] = df["date"].dt.strftime("%Y-W%U")                      # 분석용: 2025-W24
df["period_range"] = df["date"].dt.to_period("W").astype(str)            # 시각화용: 2025-06-09/2025-06-15

final_columns = [
    'date', 'amount', 'merchant', 'category', 'type', 'bank',
    'day_of_week', 'hour', 'time_category', 'period_code', 'period_range'
]
parsed_df = df[final_columns]

os.makedirs(os.path.dirname(output_path), exist_ok=True)
parsed_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("Shinhan 파싱 완료:", output_path)
