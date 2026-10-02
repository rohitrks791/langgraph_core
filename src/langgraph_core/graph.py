from typing import TypedDict
from langgraph.graph import StateGraph, START, END
#Graph display
from IPython.display import Image, display

#Main Graph class (main data we want to be stored.)
class State(TypedDict):
    x: int
    y: int
    result: int


def func1(state: State) -> State:
    result = state["x"] + state["y"]
    return {"result": result}


def func2(state: State) -> State:
    result = state["result"] * 2
    return {"result": result}


workflow = StateGraph(State)

workflow.add_node("node_1", func1)
workflow.add_node("node_2", func2)

workflow.add_edge(START, "node_1")
workflow.add_edge("node_1", "node_2")
workflow.add_edge("node_2", END)

app = workflow.compile()

response = app.invoke({"x": 10, "y": 5})
print(response)

try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    pass