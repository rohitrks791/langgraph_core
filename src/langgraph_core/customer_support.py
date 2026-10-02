from typing_extensions import TypedDict, Dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from IPython.display import Image, display
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from dotenv import load_dotenv

load_dotenv()

llm = ChatNVIDIA(
    model="nvidia/nemotron-3-super-120b-a12b",
    temperature=0.6
)
# response = llm.invoke("what is langchain") # AIMessage response is returned
# print(response.text)
# exit
# State will be the input schema for all the nodes and edges in the graph.
# So whenever we creating nodes or edges, the state we need to pass(everything is passed as a dict)
# Define State of the Graph
class State(TypedDict):
    query: str
    category: str
    sentiment: str
    response: str

def categorize(state: State) -> State:
    prompt = ChatPromptTemplate.from_template("Categorize the following query into one of the following categories"
    "Technical, Billing, General. Query: {query}")

    #create a chain that returns category for the query
    chain = prompt | llm
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def analyze_sentiment(state: State) -> State:
    print("\nAnalyzing the sentiment: ")
    prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of the following customer query and ans in one word"
        "Response with either 'Positive', 'Neutral', or 'Negative'. Query: {query}"
    )
    chain = prompt | llm
    sentiment = chain.invoke({"query": state["query"]}).content
    print(f"\nSentiment : {sentiment}")
    return {"sentiment": sentiment}

# we can some other llm to handle this
def handle_technical(state: State) -> State:
    print(f'\nHandling the technical query')
    prompt = ChatPromptTemplate.from_template(
        "Provide a technical support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

# we can some other llm to handle this
def handle_billing(state: State) -> State:
    print(f'\nHandling the billing query')
    prompt = ChatPromptTemplate.from_template(
        "Provide a billing support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

# we can some other llm to handle this
def handle_general(state: State) -> State:
    print(f'\nHandling the general query')
    prompt = ChatPromptTemplate.from_template(
        "Provide a general support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

# we can some other llm to handle this
def esclate(state: State) -> State:
    print(f"Esclating Query")
    return {"response": "This query has been esclate to a human agent due to its negative sentiment."}

# returning the name of the next node:
def route_query(state: State) -> str:
    if "negative" in state["sentiment"].lower():
        return "esclate"
    elif "technical" in state["category"].lower():
        return "handle_technical"
    elif "billing" in state["category"].lower():
        return "handle_billing"
    else:
        return "handle_general"


def run_customer_support(query: str) -> Dict[str, str]:
    results = app.invoke({"query": query})
    return {
        "category":results['category'],
        "sentiment":results['sentiment'],
        "response": results['response'],
    }

# Test the workflow
query = "The price value in my invoice is wrong"
result = run_customer_support()
print(f"\n\nComputed Result:")
print(f"Query: {query}")
print(f"\n\nCategory: {result['category']}")
print(f"\n\nSentiment: {result['sentiment']}")
print(f"\n\nResponse: {result['response']}")
print("\n")
# Create State Graph(Workflow)
workflow = StateGraph(State)

workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_technical", handle_technical)
workflow.add_node("handle_billing", handle_billing)
workflow.add_node("handle_general", handle_general)
workflow.add_node("esclate", esclate)

workflow.add_conditional_edges(
    "analyze_sentiment",
    route_query,
    {
        "esclate": "esclate",
        "handle_technical": "handle_technical",
        "handle_billing": "handle_billing",
        "handle_general": "handle_general",
    }
)
workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_edge("handle_technical", END)
workflow.add_edge("handle_billing", END)
workflow.add_edge("handle_general", END)
workflow.add_edge("esclate", END)

workflow.set_entry_point("categorize")
app = workflow.compile()
try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    pass