import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

#  1. 데이터 로딩
data_path = os.path.join("data", "KDDTest+.txt")
df = pd.read_csv(data_path, header=None)

#  2. 컬럼 이름 부여 (공식 NSL-KDD 컬럼명)
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment",
    "urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted",
    "num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label", "difficulty_level"  # ✅ 추가됨
]
df.columns = columns
df = df.drop("difficulty_level", axis=1)

#  3. 라벨 이진화
df["label"] = df["label"].apply(lambda x: "normal" if x == "normal" else "attack")

#  4. 문자열 컬럼 인코딩
for col in ["protocol_type", "service", "flag"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

#  5. 특성/타겟 분리
X = df.drop("label", axis=1)
y = df["label"]

#  6. 타겟 인코딩
y = LabelEncoder().fit_transform(y)

#  7. 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  8. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

#  9. 저장
joblib.dump(model, os.path.join("models", "ids_model.pkl"))
joblib.dump(scaler, os.path.join("models", "scaler.pkl"))

print(" 모델 학습 및 저장 완료!")
