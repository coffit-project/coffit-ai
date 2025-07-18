import pandas as pd
import glob
import os
import chardet

# 1. 병합할 폴더 경로
labeled_dir = "data/labeled"

# 2. 병합 대상 파일 찾기 (labeled_*.csv)
csv_files = glob.glob(os.path.join(labeled_dir, "labeled_*.csv"))

# 3. DataFrame 리스트 생성
df_list = []

for file in csv_files:
    with open(file, "rb") as f:
        result = chardet.detect(f.read(10000))
        encoding = result["encoding"]

    print(f"📂 {file} → 인코딩: {encoding}")
    df = pd.read_csv(file, encoding=encoding)
    
    # 필요 시 인덱스 컬럼 제거
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    df_list.append(df)

# 4. 병합
merged_df = pd.concat(df_list, ignore_index=True)

# 5. 저장
output_path = os.path.join(labeled_dir, "total_labeled.csv")
merged_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 라벨링된 데이터 병합 완료 → {output_path}")
