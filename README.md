🏛️ LLM Council — Local & Distributed Multi-LLM System
Project Overview

This project implements a local and distributed version of the LLM Council, inspired by Andrej Karpathy’s idea of combining multiple Large Language Models (LLMs) to improve reasoning quality.

Instead of relying on a single model, the system orchestrates multiple locally deployed LLMs, each running as an independent service. These models collaborate through a three-stage workflow: independent answers, peer review, and final synthesis by a dedicated Chairman model.

The entire system runs without any cloud-based API. All inference is performed locally using Ollama, and all components communicate through REST APIs.

Core Idea: Why an LLM Council?

Single-model answers can be biased, incomplete, or fragile.
The LLM Council approach introduces:

Diversity of reasoning

Self-critique between models

Aggregation of perspectives

Improved robustness of final answers

The user is also able to inspect intermediate outputs, making the reasoning process transparent.

Council Workflow
Stage 1 — First Opinions

The user submits a prompt through the frontend UI.

The backend orchestrator forwards the query to each council member LLM.

Each LLM:

Runs independently

Uses its own local model

Produces its own answer

All responses are collected and displayed in a tabbed interface.

Stage 2 — Review & Ranking

Each council member receives:

The answers produced by the other models

With identities anonymized

Each LLM evaluates the responses and ranks them according to:

Accuracy

Insight

Rankings are sent back to the orchestrator.

This stage introduces self-critique and cross-evaluation, which is a key aspect of the project.

Stage 3 — Chairman Final Answer

A dedicated Chairman LLM:

Receives all original responses

Receives all rankings

The Chairman does not generate an initial answer.

Its sole responsibility is to synthesize everything into a final response presented to the user.

System Architecture

The system is composed of four main layers:

1. Council Member Services

Each council member runs as an independent FastAPI service, exposing a simple /chat endpoint.

A typical council service:

Uses FastAPI

Calls a local Ollama instance

Runs a specific model (e.g. phi3, llama3, mistral)

Can be deployed on its own machine

Each service is stateless and only responsible for:

Receiving messages

Querying its local LLM

Returning the generated content

2. Chairman Service

The Chairman:

Runs as a separate FastAPI service

Uses its own model instance

Does not participate in Stage 1

Only performs synthesis in Stage 3

In our implementation, the Chairman uses Mistral, chosen for its strong summarization and reasoning abilities.

3. Backend Orchestrator

The backend orchestrator coordinates the entire workflow:

Dispatches the user query to all council members

Collects first-stage answers

Redistributes responses for review

Aggregates rankings

Calls the Chairman for final synthesis

Persists conversation data

The orchestrator is configured through a central configuration file that defines:

Council members

Chairman

REST endpoints

Storage location

This design makes the system modular and extensible.

4. Frontend

The frontend provides a simple ChatGPT-like interface that allows users to:

Submit prompts

View each council member’s response

Inspect review and ranking results

Read the Chairman’s final answer

The UI emphasizes transparency of reasoning, not just the final output.

Distributed Deployment
Models Used

We used three different local LLMs, each running on a separate machine:

Role	Model	Runtime
Council Member 1	phi3:latest	Ollama
Council Member 2	llama3.1:8b	Ollama
Council Member 3	mistral:latest	Ollama
Chairman	mistral:latest	Ollama

This ensures:

Model diversity

Hardware separation

Real distributed execution

Machine Distribution

Each council LLM runs on a different machine

The Chairman runs on a dedicated machine

All components communicate via REST APIs

The frontend and orchestrator connect transparently to all services

This fully satisfies the distributed architecture requirement.

Configuration

The backend configuration defines:

Council members

Chairman

Service endpoints

Data storage paths

Each model is referenced by name and mapped to a REST endpoint, allowing easy replacement or extension without code changes.

Conversation data (responses, rankings, final answers) is stored locally to enable:

Debugging

Replay

Analysis

End-to-End Execution

When the system is running:

User submits a prompt

All council members respond independently

Responses are reviewed and ranked

Chairman synthesizes the final answer

User can inspect all intermediate steps

Everything runs locally, distributed, and end-to-end functional.

Improvements Over the Original Implementation

Compared to the original cloud-based LLM Council:

Fully local inference (no OpenRouter, no OpenAI)

True distributed deployment across machines

Clear separation between:

Council members

Chairman

Orchestrator

More transparent architecture

Easier experimentation with different models

Learning Outcomes

This project allowed us to:

Design a distributed AI system

Deploy and manage multiple local LLMs

Build REST-based AI services

Implement multi-agent critique workflows

Understand the limitations and strengths of different models

Work collaboratively on a non-trivial codebase

Generative AI Usage Statement

Generative AI tools were used transparently in this project.

They assisted with:

Code refactoring

Documentation drafting

Debugging

Architectural discussions

All final decisions, integrations, and validations were performed by the team.

Conclusion

This project demonstrates that collaborative multi-LLM systems can be built locally, distributed, and without cloud dependency, while preserving advanced reasoning workflows such as self-review and synthesis.

The LLM Council architecture provides a strong foundation for future experimentation in multi-agent AI systems.
