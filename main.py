from fastapi import FastAPI
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel

app = FastAPI()

@app.get('/')
def index():
  return {'data': {'name': 'Test'}}

class User(BaseModel):
    name: str

@app.post('/api/hello')
def hello_service(user: User):
    resp = { 'message': 'Hello, {}!'.format(user.name) }
    return resp

class Question(BaseModel):
    query: str

@app.post('/api/llm')
def llm_service(question: Question):
    prompt = question.query

    vertexai.init(location="us-west1") # vertexaiの初期化で、ロケーションを設定

    model = GenerativeModel("gemini-2.0-flash-001") # モデルを設定

    response = model.generate_content( # プロンプトをモデルに入れて出力(レスポンスを得る)
        prompt
    )

    print(response.text) # コンソールログにresponseのテキストを表示
    resp = { 'response': response.text } # responseを形作る
    return resp
