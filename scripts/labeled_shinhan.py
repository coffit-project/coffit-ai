import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

total_path = os.path.join(BASE_DIR, "data", "parsed", "total_parsed.csv")
output_path = os.path.join(BASE_DIR, "data", "labeled", "labeled_shinhan.csv")

# 1. total_parsed.csv 불러오기
total_df = pd.read_csv(total_path)

# 2. 신한은행 데이터만 필터링
shinhan_df = total_df[total_df["bank"] == "신한"].copy()

# 3. 카테고리 라벨링 함수 정의
def label_category(merchant):
    m = str(merchant)
    if any(k in m for k in ["투썸", "스타벅", "카페", "커피", "이디야", "매머드", "베이커리", "케이크", "Coffee"]):
        return "카페/음료"
    elif any(k in m for k in ["식당", "맥주", "라멘", "국밥", "밀면", "치킨", "마라", "아이스크림", "밥", "우아한"]):
        return "식사/외식"
    elif any(k in m for k in ["버스", "택시", "철도", "코레일", "KTX"]):
        return "교통"
    elif any(k in m for k in ["무신사", "올리브영", "마켓", "마트", "백화점", "쿠팡", "에이블리", "GS", "세븐일레븐", "씨유"]):
        return "쇼핑/의류"
    elif any(k in m for k in ["PC방", "노래", "넷플릭스", "게임", "보드게임", "엔터"]):
        return "게임/엔터"
    elif any(k in m for k in ["AWS", "넷플릭스", "유튜브", "멜론"]):
        return "구독/정기결제"
    elif any(k in m for k in ["송금", "이체", "출금", "페이", "카카오"]):
        return "금융/이체"
    else:
        return "기타"

# 4. 라벨링 적용
shinhan_df["category"] = shinhan_df["merchant"].apply(label_category)

# 5. 저장 (디렉터리 없으면 생성)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
shinhan_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ Shinhan 라벨링 완료: {output_path}")
