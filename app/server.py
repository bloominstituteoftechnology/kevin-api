from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.pr import pr_chain
from app.test import test_chain
from app.review import review_chain
from app.generate import generate_chain

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, pr_chain, enable_feedback_endpoint=True, path="/pr")
add_routes(app, test_chain, enable_feedback_endpoint=True, path="/test")
add_routes(app, review_chain, enable_feedback_endpoint=True, path="/review")
add_routes(app, generate_chain, enable_feedback_endpoint=True, path="/generate")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)