import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from github import Github, GithubException
from app.utils.github_repo import GitHubRepo
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

def load_environment_variables():
    load_dotenv()
    os.environ['PINECONE_API_KEY'] = os.environ.get('PINECONE_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

def initialize_pinecone_client():
    return Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))

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
    
    ACCESS_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
    pc = initialize_pinecone_client()

    # Check if index already exists
    if pc.list_indexes().index(req["name"]):
        return

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
        if 'py' in file:
            # Split documents into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
            documents = text_splitter.split_text(ghr.get_file_content(file))

            # Choose the embedding model and vector store 
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            PineconeVectorStore.from_texts(texts=documents, embedding=embeddings, index_name=req["name"])

    return {"message": "Vectorization completed"}

