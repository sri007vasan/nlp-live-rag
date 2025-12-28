import os

from dotenv import load_dotenv
from llama_index.llms.types import ChatMessage, MessageRole
from llama_index.retrievers import PathwayRetriever
from traceloop.sdk import Traceloop

from pathway.xpacks.llm.vector_store import VectorStoreClient

load_dotenv()

# Verify Google API key is set
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please set it to your Google Gemini API key. "
        "You can obtain one from: https://aistudio.google.com/app/apikey"
    )


Traceloop.init(app_name=os.environ.get("APP_NAME", "PW - LlamaIndex (Streamlit)"))

DEFAULT_PATHWAY_HOST = "demo-document-indexing.pathway.stream"

PATHWAY_HOST = os.environ.get("PATHWAY_HOST", DEFAULT_PATHWAY_HOST)

PATHWAY_PORT = int(os.environ.get("PATHWAY_PORT", "80"))


def get_additional_headers():
    headers = {}
    key = os.environ.get("PATHWAY_API_KEY")
    if key is not None:
        headers = {"X-Pathway-API-Key": key}
    return headers


vector_client = VectorStoreClient(
    PATHWAY_HOST,
    PATHWAY_PORT,
    additional_headers=get_additional_headers(),
)


retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)
retriever.client = VectorStoreClient(
    host=PATHWAY_HOST, port=PATHWAY_PORT, additional_headers=get_additional_headers()
)

pathway_explaination = "Pathway is a high-throughput, low-latency data processing framework that handles live data & streaming for you."
DEFAULT_MESSAGES = [
    ChatMessage(role=MessageRole.USER, content="What is Pathway?"),
    ChatMessage(role=MessageRole.ASSISTANT, content=pathway_explaination),
]


def _initialize_chat_engine():
    """Initialize chat engine lazily to avoid circular imports and default OpenAI instantiation."""
    from llama_index.chat_engine.condense_plus_context import CondensePlusContextChatEngine
    from llama_index.llms.gemini import Gemini
    from llama_index.service_context import ServiceContext
    from llama_index.embeddings import OpenAIEmbedding
    
    llm = Gemini(model_name="models/gemini-2.5-flash")
    
    # Create service context with explicit Gemini LLM and local embedding model
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model="local"
    )
    
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        retriever=retriever,
        service_context=service_context,
        system_prompt="""You are RAG AI that answers users questions based on provided sources.
    IF QUESTION IS NOT RELATED TO ANY OF THE CONTEXT DOCUMENTS, SAY IT'S NOT POSSIBLE TO ANSWER USING PHRASE `The looked-up documents do not provde information about...`""",
        verbose=True,
        chat_history=DEFAULT_MESSAGES,
    )
    return chat_engine


# Lazy initialization of chat_engine
_chat_engine = None


def get_chat_engine():
    """Get or initialize the chat engine."""
    global _chat_engine
    if _chat_engine is None:
        _chat_engine = _initialize_chat_engine()
    return _chat_engine
