LLM Council — Local & Distributed Multi-LLM System
Project Overview

This project is inspired by Andrej Karpathy’s idea of combining multiple Large Language Models (LLMs) to improve reasoning quality. We started from the original GitHub code and then refactored and modified it to run entirely locally and in a distributed setup.

Rather than relying on a single model, the system orchestrates several locally deployed LLMs, each running as an independent service. These models collaborate through a three-stage workflow that includes independent answer generation, peer review between models, and final synthesis by a dedicated Chairman model.

The entire system operates without any cloud-based API. All inference is performed locally using Ollama, and all components communicate exclusively through REST APIs. This makes the system fully self-hosted, reproducible, and suitable for distributed deployment across multiple machines.

Core Idea: Why an LLM Council?

Single-model answers can often be biased, incomplete, or fragile. The LLM Council approach addresses these limitations by introducing diversity of reasoning and structured self-critique between models. By aggregating multiple perspectives and forcing models to evaluate one another’s outputs, the system produces more robust and well-reasoned final answers.

An important aspect of this approach is transparency. The user is able to inspect all intermediate outputs produced during the reasoning process, including the initial answers and the review phase, rather than only seeing a single opaque final response.

Council Workflow
Stage 1 — First Opinions

The workflow begins when the user submits a prompt through the frontend interface. This prompt is received by the backend orchestrator, which forwards it to each council member LLM.

Each LLM runs independently, uses its own local model, and generates its own response without access to the other models’ outputs. All responses are then collected by the orchestrator and displayed in the frontend using a tabbed interface, allowing the user to inspect each answer individually.

Stage 2 — Review & Ranking

In the second stage, each council member receives the answers produced by the other models. Model identities are anonymized to prevent bias during evaluation.

Each LLM analyzes the provided responses and ranks them according to accuracy and insight. These rankings are then sent back to the backend orchestrator. This stage introduces structured self-critique and cross-evaluation, which is a central element of the LLM Council approach.

Stage 3 — Chairman Final Answer

In the final stage, a dedicated Chairman LLM takes over. The Chairman receives all original responses as well as all ranking information generated during the review phase.

The Chairman does not generate an initial answer of its own. Its sole responsibility is to synthesize the available information into a single coherent and well-structured final response, which is then presented to the user.

System Architecture

The system is composed of four main components: council member services, a chairman service, a backend orchestrator, and a frontend interface.

Each council member runs as an independent FastAPI service exposing a simple /chat endpoint. These services connect to a local Ollama instance and run a specific LLM model such as Phi-3, LLaMA 3.1, or Mistral. Each service is stateless and is only responsible for receiving messages, querying its local LLM, and returning the generated response. Council services can be deployed on separate machines without modification.

The Chairman runs as a separate FastAPI service with its own dedicated model instance. It does not participate in the first opinion stage and is only invoked during the final synthesis phase. In this implementation, the Chairman uses the Mistral model due to its strong summarization and reasoning capabilities.

The backend orchestrator coordinates the entire workflow. It dispatches user queries to council members, collects first-stage responses, redistributes answers for review, aggregates rankings, calls the Chairman service, and persists conversation data. The orchestrator is configured through a central configuration file that defines council members, endpoints, and storage paths, making the system modular and easy to extend.

The frontend provides a ChatGPT-like user interface that allows users to submit prompts, inspect individual council member responses, review ranking results, and read the Chairman’s final answer. The interface is designed to emphasize transparency of reasoning rather than hiding intermediate steps.

Distributed Deployment

The system uses three different local LLMs running on separate machines: Phi-3, LLaMA 3.1 (8B), and Mistral. Each of these models acts as a council member and is served locally via Ollama. The Chairman also runs Mistral but as a dedicated and isolated service.

This deployment ensures model diversity, hardware separation, and true distributed execution. Each council LLM runs on a different machine, while the Chairman runs on its own dedicated machine. All components communicate using REST APIs, and the frontend and orchestrator connect transparently to all services.

Configuration

The backend configuration defines the list of council members, the chairman service, the REST endpoints for each model, and the data storage paths. Each model is referenced by name and mapped to a service URL, allowing models to be replaced or extended without code changes.

Conversation data, including responses, rankings, and final answers, is stored locally. This enables debugging, replaying conversations, and post-analysis of the reasoning process.

End-to-End Execution

When the system is running, the user submits a prompt through the frontend. All council members respond independently, after which their responses are reviewed and ranked. The Chairman then synthesizes a final answer based on all available information. Throughout this process, the user can inspect every intermediate step.

The entire workflow runs locally, in a distributed manner, and is fully functional from end to end.

Demo Instructions (Live TD Session)

This section describes how to run the complete system during the live demonstration.

1. Start Council Member & Chairman Services

Each LLM runs as an independent FastAPI service.
On the corresponding machines (or terminals), start the services as follows:

# Council Member 1
python -m uvicorn member1_service:app --port 8002

# Council Member 2
python -m uvicorn member2_service:app --host 0.0.0.0 --port 8003

# Council Member 3
python -m uvicorn member3_service:app --host 0.0.0.0 --port 8004

# Chairman Service
python -m uvicorn chairman_service:app --host 0.0.0.0 --port 8005


Each service connects to its local Ollama instance and exposes a /chat endpoint.

2. Start the Backend Orchestrator

Once all LLM services are running, start the backend orchestrator:

python -m backend.main


The orchestrator:

Dispatches queries to council members

Manages the review & ranking stage

Calls the Chairman for final synthesis

3. Start the Frontend

Finally, start the frontend interface:

npm run dev

Then open the application in your browser:

http://localhost:5173

<img width="1883" height="914" alt="image" src="https://github.com/user-attachments/assets/44c48b2e-16aa-4d14-b598-2a2a4f7e1ba5" />

Improvements Over the Original Implementation

Compared to the original cloud-based LLM Council, this implementation removes all dependency on OpenRouter or OpenAI, supports true distributed deployment across multiple machines, clearly separates council members, the chairman, and the orchestrator, and provides a more transparent and extensible architecture. It also makes experimentation with different local models significantly easier.

Learning Outcomes

This project provided hands-on experience in designing a distributed AI system, deploying and managing multiple local LLMs, building REST-based AI services, and implementing multi-agent critique workflows. It also enabled a deeper understanding of the strengths and limitations of different LLMs and required collaborative work on a non-trivial codebase.

Generative AI Usage Statement

Generative AI tools were used transparently throughout this project to assist with code refactoring, documentation drafting, debugging, and architectural discussions (chatgpt). All final decisions, integrations, and validations were performed by the team.

Conclusion

This project demonstrates that collaborative multi-LLM systems can be built locally, deployed in a distributed manner, and operated without any cloud dependency while preserving advanced reasoning workflows such as self-review and synthesis. The LLM Council architecture provides a strong foundation for future experimentation in multi-agent AI systems.
