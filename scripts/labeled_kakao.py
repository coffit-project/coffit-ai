import pandas as pd

# 설정
BANK_NAME = '카카오뱅크'

INPUT_PATH = f'../data/parsed/total_parsed.csv'
FINAL_OUTPUT_PATH = f'../data/labeled/labeled_Kakao.csv'

# 카테고리 자동 분류 함수
def classify(merchant):
    rules = {
        "카페/음료": ["커피", "카페", "바나프레소", "공차", "탐앤탐스", "이디야", "투썸", "매머드", "컴포즈","파리바게뜨"],
        "식사/외식": ["분식", "치킨", "식당", "샤브로", "술집", "라멘", "마트", "롯데리아", "CU", "맥도날드",
                     "버거킹", "밥", "버거", "김밥", "마라탕", "연어", "냉면", "GS25", "떡볶이", "씨유"],
        "쇼핑/의류": ["의류", "쇼핑", "에이블리", "무신사", "지그재그", "올리브영", "다이소"],
        "교통": ["후불교통", "지하철", "버스", "택시", "KTX"],
        "구독/정기결제": ["넷플릭스", "멜론", "유튜브", "웨이브", "티빙"],
        "금융/이체": ["카카오페이", "송금", "이체", "계좌", "ATM"],
        "게임/엔터": ["스팀", "게임", "노래방", "영화", "CGV", "엔터"]
    }
    if pd.isna(merchant): return "기타"
    for category, keywords in rules.items():
        if any(kw in merchant for kw in keywords):
            return category
    return "기타"

# 실행
if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    df = df[df['bank'] == BANK_NAME]
    print(f"[INFO] {BANK_NAME} 거래 {len(df)}건 로드 완료")

    df['category'] = df['merchant'].apply(classify)
    df.to_csv(FINAL_OUTPUT_PATH, index=True, encoding='utf-8-sig')
    print(f"전체 자동 라벨링 완료 → {FINAL_OUTPUT_PATH}")


