import pandas as pd

df = pd.read_csv("../data/parsed/total_parsed.csv")

ibk_df = df[df["bank"] == "기업은행" ].copy()

# 카테고리 분류
def classify_category(merchant):
    if any(keyword in merchant for keyword in ["커피", "카페", "다방", "공차", "달다곰이", "탐앤탐스", "탐탐", "이디야", "투썸", "매머드", "브레드", "스타벅스", "컴포즈", "메가", "망고", "배스킨", "차백도", "케이크", "파스쿠찌", "크레페", "피코야", "파리바게뜨", "빵", "플럼비"]):
        return "카페/음료"
    elif any(keyword in merchant for keyword in ["넥슨", "스팀", "카카오페이지", "플레이스테이션", "플스", "엔터테인", "유플러스"]):
        return "게임/엔터"
    elif any(keyword in merchant for keyword in ["분식", "치킨", "식당", "한솥", "KFC", "라멘", "이자카야", "롯데리아", "맥도날드", "밥", "버거", "김밥", "양식", "차돌", "마라탕", "연어", "냉면", "떡볶이", "활어", "스시", "샤브", "타코", "한식", "푸드",
                                                 "배달의민족", "쿠팡잇츠", "요기요", "우아한", "맥주", "김가네", "닭강정", "던킨", "차돌풍", "정통집", "국밥", "순대국", "한우"]):
        return "식사/외식"
    elif any(keyword in merchant for keyword in ["후불교통", "지하철", "버스", "택시", "기후동행", "카카오T", "코레일"]):
        return "교통"
    elif any(keyword in merchant for keyword in ["멜론", "유튜브 프리미엄", "넷플릭스", "넷플", "유튜브", "FLO", "티빙", "Tving", "Wave", "쿠팡플레이", "구독", "App"]):
        return "구독/정기결제"
    elif any(keyword in merchant for keyword in ["ATM", "송금", "페이", "이체", "PAYCO"]):
        return "금융/이체"
    elif any(keyword in merchant for keyword in ["의류", "쇼핑", "이랜드", "CU", "세븐", "GS25", "씨유", "마트", "쿠팡", "무신사", "다이소", "무인양푼", "무지", "올리브", "에이블리", "브랜디", "KREAM", "아이파크몰", "지에스", "이니스프리", "더현대"]):
        return "쇼핑/의류"
    else:
        return "기타"

ibk_df["category"] = ibk_df["merchant"].fillna("").apply(classify_category)

# 표준 스키마로 정리
df_final = ibk_df[[
    "date", "amount", "merchant", "category", "type",
    "bank", "day_of_week", "hour", "time_category", "period_code", "period_range"
]]

df_final.to_csv("../data/labeled/labeled_ibk.csv", index=False, encoding='utf-8-sig')

# 결과 미리 보기
print(df_final.head())
