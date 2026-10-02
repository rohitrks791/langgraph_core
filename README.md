# LangGraph Core - Learning Notes

This repository is a hands-on to LangGraph, built around three workflows: a sequential state graph, customer-support query routing, and candidate screening. The examples show how to model shared state, implement nodes, connect them with edges, and use conditional routing to control execution, including where LLM calls fit into a graph.

## Concepts Covered

- **State:** `TypedDict` describes the expected shape of the graph's shared data. Each node receives th`e current state and returns fields to update. In these examples, state is passed within a graph invocation; durable checkpointing and resume support have not been added.
- **Nodes:** Python functions that perform a focused task, such as adding values, classifying a query, analyzing sentiment, or generating a response.
- **Edges:** Define the execution order between nodes. `START` begins the workflow, and `END` marks the completion of a path or graph.
- **Conditional edges:** A routing function examines the state and selects the next node, allowing a graph to branch based on its current data.
- **Compile and invoke:** After defining nodes and edges in a `StateGraph`, `compile()` creates an executable app and `invoke()` runs it with an input state.
- **LangChain prompt/model chain:** `ChatPromptTemplate` builds a prompt, and `prompt | llm` composes it with a model. A node returns the model output as part of the state.
- **Graph visualization:** The notebook attempts to display the graph as a Mermaid PNG so its node connections can be inspected.

## Examples Explored

### 1. Basic Sequential Graph

The arithmetic example in `graph_demo.ipynb` and `src/langgraph_core/graph.py` has two nodes:

1. `node_1` adds `x` and `y` and returns the result.
2. `node_2` doubles that result.
3. The edges define the flow `START -> node_1 -> node_2 -> END`.

With `x = 10` and `y = 5`, the final result is `30`. This is a compact example of a state schema, node outputs, and sequential edges.

### 2. Customer-Support Query Routing

The notebook and `src/langgraph_core/customer_support.py` define an LLM-driven workflow for customer queries:

1. `categorize` classifies a query as `Technical`, `Billing`, or `General`.
2. `analyze_sentiment` labels its sentiment as `Positive`, `Neutral`, or `Negative`.
3. The conditional edge calls `route_query`: negative sentiment goes to a human-escalation path; otherwise, the category selects the technical, billing, or general handler.
4. A support handler generates a response, while the escalation node returns a human-follow-up response.

Sample notebook queries include an invoice-pricing issue and questions about a purchase or service. This example explores branching after classification and using separate prompt/model calls for different tasks.

### 3. Candidate Screening

The notebook and `src/langgraph_core/candidate_selection.py` define a screening flow for a Python Developer application:

1. `categorize_experience` assesses the application as Entry-level, Mid-level, or Senior-level.
2. `assess_skillset` checks the candidate's skills against the Python role.
3. `route_app` sends a match to an HR interview. A senior candidate with a skill mismatch is escalated to a recruiter; other mismatches are rejected.

The notebook includes profiles with 10 years and 1 year of Java experience, a Python profile, and a profile with 5 years of C++ experience. The final decision depends on both the model's classification and the graph's routing rules.

## Workflow Pattern

The examples follow a shared pattern: put the input in state, define task-specific nodes, connect them with edges to express sequence or branches, and invoke the compiled graph with an initial state. Keeping LLM calls in task-specific nodes makes classification, analysis, response generation, and deterministic routing easier to inspect and change independently. Python code makes the routing decision; LLM nodes provide values that the routing function uses.

These workflows are currently learning demos. The notebook cells have not been executed, so the documented outputs and branches describe expected behavior from the code, not run-verified results. LLM output can vary, and routing depends on labels or substring checks. Before production use, add output validation and normalization, error handling, and tests.
