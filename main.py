from fastapi import FastAPI
from pydantic import BaseModel

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
