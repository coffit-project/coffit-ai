import pandas as pd
import glob
import os

# 1. 병합 대상 폴더 경로
parsed_dir = "data/parsed"

# 2. *_parsed.csv 파일만 읽기
csv_files = glob.glob(os.path.join(parsed_dir, "*_parsed.csv"))

# 3. 데이터프레임 리스트로 저장
df_list = []

for file in csv_files:
    df = pd.read_csv(file, encoding="utf-8-sig")
    df_list.append(df)

# 4. 병합
merged_df = pd.concat(df_list, ignore_index=True)

# 5. 중복 제거 (필요 시)
merged_df.drop_duplicates(inplace=True)

# 6. 저장
merged_df.to_csv(os.path.join(parsed_dir, "total_parsed.csv"), index=False, encoding="utf-8-sig")

print("✅ 모든 parsed 데이터 병합 완료! → data/parsed/total_parsed.csv")
