# 🤖 Agentic RAG-Based Application

A multi-agent **Retrieval-Augmented Generation (RAG)** application powered by **CrewAI**, **LangChain**, and **Llama 3.0** API.  
This project orchestrates **autonomous AI agents**—Researcher, Writer, Critic, and Reviser—working together in a loop to generate, refine, and deliver high-quality content without human intervention.

---

## 📌 Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Workflow](#workflow)
5. [Tech Stack](#tech-stack)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Example Output](#example-output)
9. [Future Enhancements](#future-enhancements)
10. [License](#license)

---

## 📖 Introduction
Traditional RAG systems retrieve information from external sources and feed it to a single LLM for generation.  
This project **extends RAG into an Agentic architecture**, where multiple AI agents collaborate:

- **Researcher** → Finds concise, topic-specific information  
- **Writer** → Drafts content based on research  
- **Critic** → Reviews and provides constructive feedback  
- **Reviser** → Refines the draft based on feedback  

This creates a **closed-loop content creation pipeline** capable of iterating until the output meets quality standards.

---

## ✨ Features
- **Agentic AI Workflow** – Autonomous agents with specialized roles
- **Dynamic Iteration** – Feedback loop ensures continuous improvement
- **Stateful Execution** – Maintains context across agent interactions
- **Conditional Branching** – Stops or revises content based on critic feedback
- **Customizable Prompts** – Easily adjust tone, length, and style
- **Hosted Llama 3.0 API Integration** – High-quality, low-latency text generation

---

## 🏗 Architecture
```plaintext
+-------------+      +--------+      +--------+      +--------+
|   START     | ---> |Research| ---> | Writer | ---> | Critic |
+-------------+      +--------+      +--------+      +--------+
                                           ^              |
                                           |              v
                                       +--------+     (Approve)
                                       |Reviser |------> END
                                       +--------+
````

Built using **LangGraph's StateGraph** for agent orchestration.

---

## 🔄 Workflow

1. **Researcher**: Gathers concise, relevant information about the given topic.
2. **Writer**: Creates a first draft from the research.
3. **Critic**: Reviews the draft, either approving or requesting a revision.
4. **Reviser**: Improves the draft based on feedback and sends it back for review.
5. **Loop**: Continues until Critic approves the content.

---

## 🛠 Tech Stack

* **Python 3.10+**
* [CrewAI](https://github.com/joaomdmoura/crewAI)
* [LangChain](https://www.langchain.com/)
* [LangGraph](https://github.com/langchain-ai/langgraph)
* [OpenAI API](https://platform.openai.com/) (Llama 3.0 hosted)
* Typing & Dataclasses for state management

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/agentic-rag-app.git
cd agentic-rag-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt
```

**Example `requirements.txt`**:

```txt
langchain
langgraph
crewai
openai
python-dotenv
```

---

## 🚀 Usage

1. **Set your API key** in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key
```

2. **Run the application**:

```bash
python main.py
```

3. **Example command**:

```bash
# Generate an article on "Climate Change Solutions"
python main.py "Climate change solutions"
```

---

## 📝 Example Output

**Input**:

```
Topic: "Climate change solutions"
```

**Output**:

```
FINAL RESULT:
Governments, businesses, and individuals must adopt renewable energy, enhance efficiency, and restore ecosystems to combat climate change.
```

**Execution log**:

```
Completed step: researcher
Researcher: Completed research on Climate change solutions
--------------------------------------------------
Completed step: writer
Writer: Created first draft based on research
--------------------------------------------------
Completed step: critic
Critic: Draft approved!
--------------------------------------------------
```

---

## 🔮 Future Enhancements

* Add **web search retrieval** for live, updated information
* Integrate **document loaders** for domain-specific data ingestion
* Support **multi-turn conversations** with topic refinement
* Add **GUI interface** for non-technical users
* Deploy as a **REST API** for easy integration with other systems

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
