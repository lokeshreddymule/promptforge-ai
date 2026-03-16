import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


AVAILABLE_MODELS = {
    "Groq - Llama3.1 8B (Free)": "groq:llama-3.1-8b-instant",
    "Groq - Llama3.3 70B (Free)": "groq:llama-3.3-70b-versatile",
    "Groq - Mixtral 8x7B (Free)": "groq:mixtral-8x7b-32768",
    "Groq - Gemma2 9B (Free)": "groq:gemma2-9b-it",
    "Gemini 2.0 Flash (Free)": "gemini:gemini-2.0-flash",
    "Gemini 1.5 Flash (Free)": "gemini:gemini-1.5-flash",
    "Llama3 Local (Ollama)": "ollama:llama3",
    "OpenAI GPT-4o Mini": "openai:gpt-4o-mini",
}

GROQ_MODELS = {
    "Groq - Llama3.1 8B (Free)": "llama-3.1-8b-instant",
    "Groq - Llama3.3 70B (Free)": "llama-3.3-70b-versatile",
    "Groq - Mixtral 8x7B (Free)": "mixtral-8x7b-32768",
    "Groq - Gemma2 9B (Free)": "gemma2-9b-it",
}


def get_llm(model_name: str = "Groq - Llama3.1 8B (Free)", temperature: float = 0.7):
    model_value = AVAILABLE_MODELS.get(model_name, "groq:llama-3.1-8b-instant")
    provider, model_id = model_value.split(":", 1)

    if provider == "groq" and GROQ_AVAILABLE:
        return ChatGroq(
            model=model_id,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY"),
        )
    elif provider == "gemini" and GEMINI_AVAILABLE:
        return ChatGoogleGenerativeAI(
            model=model_id,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    elif provider == "ollama" and OLLAMA_AVAILABLE:
        return ChatOllama(model=model_id, temperature=temperature)
    elif provider == "openai" and OPENAI_AVAILABLE:
        return ChatOpenAI(
            model=model_id,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    # Fallback chain
    if GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
        return ChatGroq(model="llama-3.1-8b-instant", temperature=temperature,
                       api_key=os.getenv("GROQ_API_KEY"))
    if OLLAMA_AVAILABLE:
        return ChatOllama(model="llama3", temperature=temperature)

    raise ValueError("No LLM provider available.")


def get_optimizer_llm():
    """Use Groq as optimizer — fast and free."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and GROQ_AVAILABLE:
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            api_key=groq_key,
        )
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key and GEMINI_AVAILABLE:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,
            google_api_key=google_key,
        )
    if OLLAMA_AVAILABLE:
        return ChatOllama(model="llama3", temperature=0.2)

    raise ValueError("No LLM provider available.")


def generate_response(prompt: str, model_name: str = "Groq - Llama3.1 8B (Free)", temperature: float = 0.7) -> str:
    try:
        llm = get_llm(model_name, temperature)
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def estimate_tokens(text: str) -> int:
    return len(text) // 4
