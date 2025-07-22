import pandas as pd

def estimate_savings(csv_path: str, saving_rate: float = 0.5, threshold: float = 0.2, test_mode: bool = False):
    # 데이터 불러오기
    df = pd.read_csv(csv_path, parse_dates=['date'])

    # 지출 내역만 필터링 (음수 금액)
    df = df[df['amount'] < 0].copy()

    # 금액 절댓값 처리 (양수로 만듦)
    df['amount'] = df['amount'].abs()

    # period_code 정렬
    all_periods = df['period_code'].drop_duplicates().sort_values().tolist()

    if test_mode:
        # ✅ 테스트용: 가장 최근 2주차 제외한 전체 기간으로 평균 계산
        latest_period = all_periods[-2]
        recent_df = df[df['period_code'] != latest_period]
        current_week = df[df['period_code'] == latest_period]
    else:
        # ✅ 실제 서비스용: 최근 4주 기준으로 비교
        recent_periods = all_periods[-4:]
        recent_df = df[df['period_code'].isin(recent_periods)]
        latest_period = recent_periods[-1]
        current_week = recent_df[recent_df['period_code'] == latest_period]

    # 카테고리별 각 주차별 소비 합계
    weekly_by_category = recent_df.groupby(['period_code', 'category'])['amount'].sum().reset_index()

    # 카테고리별 주차 평균
    avg_by_category = weekly_by_category.groupby('category')['amount'].mean()

    # 현재 주차 카테고리별 합계
    current_week_sum = current_week.groupby('category')['amount'].sum().reset_index()

    # 최근 주차 확인
    print("최근 주차:", latest_period)
    print("최근 주차 소비 내역:")
    print(current_week_sum)

    # 절약 가능 금액 계산
    savings = {}

    for _, row in current_week_sum.iterrows():
        category = row['category']
        current = row['amount']
        past_avg = avg_by_category.get(category, current)

        if current > past_avg * (1 + threshold):
            over = current - past_avg
            savings[category] = round(over * saving_rate)

    return savings


if __name__ == "__main__":
    # test_mode=True → 테스트용 기준 (최근 주 제외 전체 평균)
    # test_mode=False → 실제 서비스 기준 (최근 4주 평균)
    result = estimate_savings("data/labeled/total_labeled.csv", test_mode=True)
    print("절약 가능 금액 추정 결과:")
    print(result)
