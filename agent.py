import os
from typing import Dict, TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langchain.chat_models import init_chat_model

# Define our state
class AgentState(TypedDict):
    messages: List[str]
    topic: str
    research: str
    draft: str
    feedback: str
    final_draft: str
    next: str  # To track the next step

# Initialize our LLM
llm = init_chat_model(
    "gpt-4o-mini", model_provider="azure_openai", temperature=0
)

# Create our agent nodes
def researcher(state: AgentState) -> AgentState:
    """Research agent gathers information on the topic."""
    topic = state["topic"]
    
    # Create a prompt for the researcher
    prompt = f"You are a research assistant. Find key information about: {topic}. Provide a concise summary (max 20 words)."
    
    # Get response from LLM
    messages = [SystemMessage(content="You are a helpful research assistant."), 
                HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Update state with research results
    state["research"] = response.content
    state["messages"].append(f"Researcher: Completed research on {topic}")
    
    return state

def writer(state: AgentState) -> AgentState:
    """Writer agent creates content based on research."""
    research = state["research"]
    topic = state["topic"]
    
    # Create a prompt for the writer
    prompt = f"You are a content writer. Using this research: '{research}', write a short article about {topic} (max 40 words)."
    
    # Get response from LLM
    messages = [SystemMessage(content="You are a skilled content writer (max 40 words)."), 
                HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Update state with draft
    state["draft"] = response.content
    state["messages"].append("Writer: Created first draft based on research")
    
    return state

def critic(state: AgentState) -> AgentState:
    """Critic agent reviews the draft and provides feedback."""
    draft = state["draft"]
    
    # Create a prompt for the critic
    prompt = f"You are a content critic. Review this draft and provide constructive feedback: '{draft}'"
    
    # Get response from LLM
    messages = [SystemMessage(content="You are a helpful content critic (dont be so strict). Reply with 'great job' OR 'need revision'."), 
                HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Update state with feedback
    state["feedback"] = response.content
    state["messages"].append("Critic: Provided feedback on draft")
    
    # Determine if we need another revision or if we're done
    if "excellent" in response.content.lower() or "great job" in response.content.lower():
        state["final_draft"] = state["draft"]
        state["messages"].append("Critic: Draft approved!")
        state["next"] = "end"
    else:
        state["messages"].append("Critic: Requesting revision")
        state["next"] = "revise"
    
    return state

def reviser(state: AgentState) -> AgentState:
    """Writer revises based on critic feedback."""
    draft = state["draft"]
    feedback = state["feedback"]
    
    # Create a prompt for revision
    prompt = f"You are a content editor. Revise this draft: '{draft}' based on this feedback: '{feedback}'"
    
    # Get response from LLM
    messages = [SystemMessage(content="You are a skilled content editor (max 40 words)."), 
                HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Update state with revised draft
    state["draft"] = response.content
    state["messages"].append("Writer: Created revised draft based on feedback")
    
    return state

# Define router function for conditional branching
def router(state: AgentState) -> str:
    """Route to the next node based on the 'next' field in state."""
    return state["next"]

# Build our graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)
workflow.add_node("critic", critic)
workflow.add_node("reviser", reviser)

# Add entry point - this is the key fix
workflow.add_edge(START, "researcher")

# Add the rest of the edges
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "critic")

# Add conditional routing after critic
workflow.add_conditional_edges(
    "critic",
    router,
    {
        "revise": "reviser",
        "end": END
    }
)

workflow.add_edge("reviser", "critic")

# Compile the graph
app = workflow.compile()

# Run the workflow
def run_workflow(topic: str):
    # Initialize state
    initial_state = {
        "messages": [],
        "topic": topic,
        "research": "",
        "draft": "",
        "feedback": "",
        "final_draft": "",
        "next": ""
    }
    
    ### Use this when we have to track the flow precisely
    # Execute the workflow and track the final state
    final_state = initial_state
    for output in app.stream(initial_state):
        step_name = list(output.keys())[0] if output else "Unknown"
        print(f"Completed step: {step_name}")
        
        # Update our tracking of the final state
        if output:
            final_state = output[step_name]
        
        # Print the latest message if available
        if output and output[step_name]["messages"]:
            print(output[step_name]["messages"][-1])
            print("-" * 50)
    
    # Print final result
    print("\nFINAL RESULT:")
    print("=" * 80)
    if final_state.get("final_draft"):
        print(final_state["final_draft"])
    else:
        print("No final draft was produced.")
    print("=" * 80)
    
    return final_state

    #### Use this when the pipeline has to be run without logging
    # output = app.invoke(initial_state)
    # print(output['final_draft'])
    # return output


# Example usage
if __name__ == "__main__":
    result = run_workflow("Climate change solutions")
