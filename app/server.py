import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langserve import add_routes
from app.agents.pr import pr_chain
from app.agents.test import test_chain
from app.agents.review import review_chain
from app.agents.generate import generate_chain
from app.utils.vectorize import vectorize_codebase 
from app.utils.vectorize import load_environment_variables, initialize_pinecone_client
from github import GithubException

app = FastAPI()

# Define CORS origins
origins = [
    "http://localhost:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Adding routes
add_routes(app, pr_chain, enable_feedback_endpoint=True, path="/pr")
add_routes(app, test_chain, enable_feedback_endpoint=True, path="/test")
add_routes(app, review_chain, enable_feedback_endpoint=True, path="/review")
add_routes(app, generate_chain, enable_feedback_endpoint=True, path="/generate")

# Define the Pydantic model for the request body
class VectorizeRequest(BaseModel):
    name: str
    github_url: str
    branch: str

# Endpoint to vectorize codebase
@app.post("/vectorize")
async def vectorize(req: VectorizeRequest):
    try:
        # Load environment variables
        load_environment_variables()
        
        # Initialize Pinecone client
        pc = initialize_pinecone_client()

        # Check if index already exists
        if req.name in pc.list_indexes():
            return {"message": "Index already exists"}, 200

        # Call the vectorize_codebase function
        result = vectorize_codebase(req.dict())
        return {"message": "Vectorization completed successfully"}, 200

    except GithubException as e:
        raise HTTPException(status_code=400, detail=f"GitHub error: {e.data['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
