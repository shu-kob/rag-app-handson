from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
import google.auth
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

credentials, project_id = google.auth.default()

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
    context_resp = retriever_service(question)
    context = context_resp['search_result']
    print(context)
    template = """質問: {question}

    以下の情報を参考にして、質問に答えてください。
    {context}
    """

    prompt_template = PromptTemplate.from_template(template)

    chain = prompt_template | model # prompt_templateをmodelに引き渡す処理を"|"を用いて簡単に実現

    response = chain.invoke({"question": human_question, "context": context}) # invokeは全ての処理が終わってから値を返す。他にはstreamなど
    print(response)
    resp = { 'answer': response }
    return resp

@app.post('/api/retriever')
def retriever_service(question: Question):
    search_query = question.query
    project_id
    location: str = "global"
    engine_id: str = os.environ['DISCOVERY_ENGINE_ID']
    def search(
        project_id: str,
        location: str,
        engine_id: str,
        search_query: str,
    ) -> discoveryengine.services.search_service.pagers.SearchPager:
        client_options = (
            ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
            if location != "global"
            else None
        )

        client = discoveryengine.SearchServiceClient(client_options=client_options)

        serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

        content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=True
            ),
            summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                summary_result_count=3,
                include_citations=True,
                ignore_adversarial_query=True,
                ignore_non_summary_seeking_query=True,
                model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                    preamble="文献の検索結果を要約してください"
                ),
                model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                    version="stable",
                ),
            ),
        )
        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=search_query,
	        page_size=3,
            content_search_spec=content_search_spec,
            query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
                condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
            ),
            spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
                mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
            ),
        )
        page_result = client.search(request)

        return page_result

    response = search(project_id, location, engine_id, search_query)
    resp = { 'search_result': response.summary.summary_text }
    print(resp)
    return resp
