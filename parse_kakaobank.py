import pandas as pd
import os
from datetime import datetime

# 경로
INPUT_PATH = '../data/raw/kakaobank_transactions.csv'
OUTPUT_PATH = '../data/parsed/kakaobank_parsed.csv'

def get_time_category(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'


def parse_kakaobank():
    # CSV 불러오기
    df = pd.read_csv(INPUT_PATH, encoding='cp949')

    # 컬럼명 표준화
    df = df.rename(columns={
        '거래일시': 'date',
        '거래금액': 'amount',
        '내용': 'merchant',
        '거래구분': 'type',
        '구분': 'inout'
    })

    # 거래일시 → datetime 형식
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d %H:%M:%S')

    # 금액 정리
    df['amount'] = df['amount'].replace(',', '', regex=True).astype(int)
    df['amount'] = df.apply(lambda row: -row['amount'] if row['inout'] == '출금' else row['amount'], axis=1)


    # 새로운 컬럼 생성
    df['category'] = ''
    df['bank'] = '카카오뱅크'
    df['day_of_week'] = df['date'].dt.weekday
    df['hour'] = df['date'].dt.hour
    df['time_category'] = df['hour'].apply(get_time_category)
    df["period_code"] = df["date"].dt.strftime("%Y-W%U")

    # 필요한 컬럼만 선택 (표준 스키마 순서대로)
    df = df[['date', 'amount', 'merchant', 'category', 'type', 'bank',
             'day_of_week', 'hour', 'time_category', 'period_code']]

    # 저장
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
    print(f' 파싱 완료: {OUTPUT_PATH}')

if __name__ == '__main__':
    parse_kakaobank()
