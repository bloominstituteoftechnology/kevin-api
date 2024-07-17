import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from github import Github, GithubException
from app.utils.github_repo import GitHubRepo
from app.utils.database import Database
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

def load_environment_variables():
    load_dotenv()
    os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def initialize_pinecone_client():
    api_key = os.getenv('PINECONE_API_KEY')
    if not api_key:
        raise ValueError("PINECONE_API_KEY is not set in the environment variables")
    return Pinecone(api_key=api_key)

def extract_github_owner_repo(url):
    """
    Extracts the owner and repository name from a GitHub URL.
    
    Parameters:
    url (str): The GitHub URL.
    
    Returns:
    tuple: A tuple containing the owner and repository name.
    """
    if url.startswith("https://github.com/"):
        parts = url[len("https://github.com/"):].strip('/').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            return owner, repo
    return None, None

def vectorize_codebase(req):
    load_environment_variables()
    
    ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    pc = initialize_pinecone_client()

    # Check if index already exists
    existing_indexes = [index["name"] for index in pc.list_indexes()]
    if req["name"] in existing_indexes:
        return {"message": "Index already exists"}

    # Create index if it doesn't exist
    pc.create_index(
        name=req["name"],
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

    owner, repo_name = extract_github_owner_repo(req['github_url'])

    ghr = GitHubRepo(owner, repo_name, ACCESS_TOKEN)
    files = ghr.get_file_structure()

    for file in files:
        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
        documents = text_splitter.split_text(ghr.get_file_content(file))

        # Choose the embedding model and vector store 
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Adjust model name if needed
        PineconeVectorStore.from_texts(texts=documents, embedding=embeddings, index_name=req["name"])
    
    # Save record to MongoDB
    db = Database('projects')
    record = {
        "name": req["name"],
        "github_url": req["github_url"],
        "owner": owner,
        "repo_name": repo_name,
        "id": req["auth0_id"],
        "files_processed": len(files)
    }
    print(record)
    db.write_one(record)

    return {"message": "Vectorization completed and record saved to the database"}

