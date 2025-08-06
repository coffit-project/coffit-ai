import pandas as pd
import os

# 베이스 경로 설정 (scripts/ 기준)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# print("BASE_DIR:", BASE_DIR)

# 경로 정의
total_path = os.path.join(BASE_DIR, "data", "parsed", "total_parsed.csv")
# print("total_path:", total_path)
output_path = os.path.join(BASE_DIR, "data", "labeled", "labeled_kb.csv")

# 1. 전체 데이터 불러오기
total_df = pd.read_csv(total_path, encoding="utf-8-sig")

# 2. 국민은행 데이터만 필터링
kb_df = total_df[total_df["bank"] == "국민은행"].copy()

# 3. 카테고리 라벨링 함수
def label_category(merchant):
    m = str(merchant)
    if any(k in m for k in ["스타벅스", "투썸", "씨유", "카페", "빽다방", "굿웨더", "던킨도너츠", "핫브레드", "공차", "이디야", "호두붐", "만월경", "매머드", "더비즈랩", "파리바게뜨", "뿡어당", "플럼비", "커피", "케이크팝", "할리스", "메가", "커피빈", "소금빵", "읍천리382", "컴포즈커피", "까쉬", "슬로우브레드", "바나프레소", "블루보틀"]):
        return "카페/음료"
    elif any(k in m for k in ["롤링파스타", "아이스크림", "파머스마켓", "쿠팡이츠", "봄의정원", "육미안", "춘리", "버거킹", "샤브로21", "백소정", "명랑쌀핫도그", "냉면", "담솥", "맥도날드", "파스타", "써브웨이", "돈카츠", "라홍방", "라면", "니뽕내뽕", "메이빌", "신전떡볶이", "마라", "떡순튀", "와플대학", "최대패", "춘천본점닭갈비", "알촌", "돈화당", "카레", "난포", "라멘", "멘지", "미도인", "소코아", "정통집", "본크레페", "우아한형제들", "현대옥", "보배반점", "언앨리셰프", "이오로", "차일디쉬", "샤브온당", "규카츠", "라라면가", "압구정샌드위치", "투파인드피터", "참나무본가", "김통", "농월정", "성수다락"]):
        return "식사/외식"
    elif any(k in m for k in ["카카오T", "택시", "SR", "K-패스", "우버", "코레일", "UT"]):
        return "교통"
    elif any(k in m for k in ["갤러리아", "이마트", "성남사랑상품권", "삼성전자서비스", "벌툰", "드림월드", "지에스", "노브랜드", "케이티알파", "세븐일레븐", "올리브영", "누리빗", "교보문고", "홈플러스", "에이블리", "CHAK", "아트박스", "약국", "KICC", "피어싱", "포토이즘", "AK", "PC방", "다이소", "신세계", "시현하다", "롯데", "스터디룸", "Amazon", "인터파크", "대원미디어", "캡슐", "영풍문고", "오렌즈", "프린트카페", "번개장터", "KICC", "네이버파이낸셜", "포토에이스", "크림", "뉴코아", "쿠로상점", "펀시티", "굿즈", "두니부", "애니", "라신반", "돈룩업"]):
        return "쇼핑/의류"
    elif any(k in m for k in ["고플랙스코인", "오락", "오티티프라임", "퍼니랜드", "CGV", "캐치미", "쇼미더뽑기", "메가박스", "보드게임카페", "사격팡", "메타코인", "판타스틱코인", "Realworld", "안드로메다서현", "악쓰는하마", "PC방"]):
        return "게임/엔터"
    elif any(k in m for k in ["유튜브프리미엄", "KT", "구글플레이", "NETFLIX", "Netflix"]):
        return "구독/정기결제"
    elif any(k in m for k in ["PAYCO", "토스페이", "네이버페이", "KB카드출금", "카카오페이", "인터넷상거래", "MG", "신한", "마스타해외", "토뱅"]):
        return "금융/이체"
    else:
        return "기타"

# 4. 라벨링 적용
kb_df["category"] = kb_df["merchant"].apply(label_category)

# 5. 저장
os.makedirs(os.path.dirname(output_path), exist_ok=True)
kb_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 국민은행 라벨링 완료: {output_path}")