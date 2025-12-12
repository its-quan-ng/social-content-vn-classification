import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent

def read_any(cands, keep_id=False):
    for name in cands:
        p = BASE / name
        if p.exists():
            print(f"✓ Load: {p}")
            if p.suffix == ".csv":
                df = pd.read_csv(p)
            else:
                df = pd.read_excel(p)
            
            # Rename Unnamed: 0 thành id (nếu cần giữ)
            if 'Unnamed: 0' in df.columns:
                if keep_id:
                    df = df.rename(columns={'Unnamed: 0': 'id'})
                else:
                    df = df.drop(columns=['Unnamed: 0'])
            
            return df
    raise FileNotFoundError(f"Not found: {', '.join(cands)}")

# Đọc - val và test GIỮ cột id
df_self = read_any(["self_collected.xlsx", "seft_collected.xlsx"])
df_uit_train = read_any(["UIT_train.xlsx"])
df_uit_val = read_any(["UIT_val.xlsx", "UIT_dev.xlsx"], keep_id=True)
df_uit_test = read_any(["UIT_test.xlsx"], keep_id=True)

print(f"\nUIT train: {len(df_uit_train)}, Collected: {len(df_self)}")

# Bỏ cột id khi merge train
train_df_uit = df_uit_train.drop(columns=['id']) if 'id' in df_uit_train.columns else df_uit_train
train_df_self = df_self.drop(columns=['id']) if 'id' in df_self.columns else df_self

# Merge
train_merged = pd.concat([train_df_uit, train_df_self], ignore_index=True)

# Loại duplicates
train_merged = train_merged.drop_duplicates(subset=["Sentence"], keep="first")

# Tạo id tuần tự
train_merged.insert(0, 'id', range(1, len(train_merged) + 1))

# Shuffle (id cũng bị xáo trộn)
train_merged = train_merged.sample(frac=1, random_state=42).reset_index(drop=True)

# Lưu
train_merged.to_csv(BASE / "train_merged.csv", index=False, encoding="utf-8-sig")
df_uit_val.to_csv(BASE / "val.csv", index=False, encoding="utf-8-sig")
df_uit_test.to_csv(BASE / "test.csv", index=False, encoding="utf-8-sig")

print(f"\n✓ Saved:")
print(f"  train_merged.csv: {len(train_merged)} rows")
print(f"  val.csv: {len(df_uit_val)} rows")
print(f"  test.csv: {len(df_uit_test)} rows")