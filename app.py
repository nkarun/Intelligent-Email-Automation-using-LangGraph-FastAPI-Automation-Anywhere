import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph import Workflow 
from src.states.state import Email


import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI app instance
app = FastAPI()

# Print the LangChain API key (for debug purposes — remove in production!)
print(os.getenv("LANGCHAIN_API_KEY"))

# Set environment variable for LangSmith (used by LangChain/LangGraph)
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# -------------------------
# 📩 Email Processing Route
# -------------------------



@app.post("/Email")
async def process_email(request: Request):
    """
    Accepts a POST request with 'subject' and 'body' of an email.
    Invokes a LangGraph workflow using a Groq-backed LLM.
    Returns the structured output/state from the graph.
    """

    # Parse incoming JSON body
    data = await request.json()

    # Extract subject and body from the request
    subject = data.get("subject", "")
    body = data.get("body", "")

    print("Subject:", subject)
    print("Body:", body)

    state = {
        "emails": [],
        "current_email": None,
        "email_category": "",
        "generated_email": "",
        "rag_queries": [],
        "retrieved_documents": "",
        "writer_messages": [],
        "sendable": False,
        "trials": 0,
        "subject": subject,
        "body": body
    }    

    # Basic validation
    #if not subject and not body:
    #    return {"error": "Email subject or body must be provided."}

    # -------------------------
    # 🔮 Get the LLM (Groq-backed)
    # -------------------------
    #groqllm = GroqLLM()
    #llm = groqllm.get_llm()

    # -------------------------
    # 🧠 Build the LangGraph
    # -------------------------
    graph_builder = Workflow(subject=subject,body=body)
    result = graph_builder.app.invoke(state)
    
    # Return the graph output as a JSON response
    return {"data": result}
    #result = graph.app.run()  # or however your graph runs
    
    print("Workflow result:", result)


# -------------------------
# 🚀 Launch the server
# -------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
