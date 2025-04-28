# rag-app-handson

- ライブラリのインストール

```
pip install -r requirements txt
```

実行方法

```
uvicorn main:app --reload
```

```
QUESTION='{"query":"プロンプトエンジニアリングとは何ですか？"}'

curl -X POST -H "Content-Type: application/json" -d "$QUESTION" -s http://localhost:8000/api/llm | jq .
```
