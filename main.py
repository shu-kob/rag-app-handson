from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate

app = FastAPI()

@app.get('/')
def index():
  return 'hello'

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
    human_question = question.query
    model = VertexAI(model_name="gemini-2.0-flash-001", location="us-west1")
    template = """質問: {question}

    ステップバイステップで考えてください。"""

    prompt_template = PromptTemplate.from_template(template)

    chain = prompt_template | model # prompt_templateをmodelに引き渡す処理を"|"を用いて簡単に実現

    response = chain.invoke({"question": human_question}) # invokeは全ての処理が終わってから値を返す。他にはstreamなど
    print(response)
    resp = { 'answer': response }
    return resp
