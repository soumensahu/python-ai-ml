from fastapi import FastAPI,Query

from rag_async.queues.workers import process_query
from .clients.rq_client import queue
app = FastAPI()

@app.get('/')
def root():
    return {"status":"server is up and running"}

@app.post('/chat')
def chat(
    query:str=Query(...,description="query to search in the pdf file")
):
    job=queue.enqueue(process_query, query)
    return {"status":"queued", "job_id":job.id}

@app.get('/result')
def get_result(
        job_id:str=Query(...,description="job id to get the result")
):
    job=queue.fetch_job(job_id)
    result=job.return_value()
    return {"status":"completed", "result":result}