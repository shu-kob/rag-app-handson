# rag-app-handson

## 準備

```
python -m venv fastapi-env
```

```
source fastapi-env/bin/activate
```

- Windowsのコマンドプロンプトの場合

```
fastapi-env/Scripts/activate
```

```
pip install fastapi uvicorn
```

```
touch main.py
```

```
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
  return 'hello'
```

- 実行

```
uvicorn main:app --reload
```

- 別ターミナルにて

```
curl -s http://localhost:8000/
```

## ライブラリのインストール

```
pip install -r requirements.txt
```

## 実行方法

```
uvicorn main:app --reload
```

- 別ターミナルにて

```
QUESTION='{"query":"プロンプトエンジニアリングとは何ですか？"}'

curl -X POST -H "Content-Type: application/json" -d "$QUESTION" -s http://localhost:8000/api/llm | jq .
```
