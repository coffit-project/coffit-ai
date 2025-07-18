import pandas as pd

# 1. 전체 데이터 로드
df = pd.read_csv("data/parsed/total_parsed.csv", encoding="utf-8-sig")

# 2. 본인 은행 데이터 필터링 (전체 행 유지)
df_tossbank = df[df["bank"] == "토스뱅크"].copy()

# 3. 저장 (모든 컬럼 포함 + index 포함)
df_tossbank.to_csv("data/labeled/labeled_tossbank.csv", index=True, encoding="utf-8-sig")

print("✅ 내 은행 전체 데이터 저장 완료 → labeled_tossbank.csv")
