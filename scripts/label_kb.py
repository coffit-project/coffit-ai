import pandas as pd
import os

# 1. 파일 경로 정의
input_path = "data/parsed/total_parsed.csv"
output_path = "data/labeled/labeled_kb.csv"

# 2. 파일 불러오기
df = pd.read_csv(input_path)

# 🔍 어떤 은행이 있는지 확인
print("📌 bank 컬럼 값들:", df["bank"].unique())

# 3. '국민' 은행만 필터링
kb_df = df[df['bank'] == '국민은행'].copy()

# 4. 샘플 500건만 추출 (무작위)
sample_df = kb_df.sample(n=500, random_state=42)  # 무작위

# 5. 저장 (index 포함)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
sample_df.to_csv(output_path, index=True, encoding="utf-8-sig")

print("✅ 라벨링용 국민은행 샘플 저장 완료!", output_path)