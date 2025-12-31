# Multi-Agent Economic Market Simulation

## Overview

This project is an autonomous multi-agent simulation designed to model complex economic interactions and emergent market behaviors. Unlike traditional economic models that assume rational actors, this simulation utilizes Large Language Models (LLMs) to power agents with distinct personalities, cognitive biases, and specific strategic objectives (e.g., hoarding, high-frequency trading, or stimulus injection).

The core challenge this project solves is the simulation of "human" irrationality in financial markets. By assigning specific psychological profiles (such as "Panic Seller," "Value Investor," or "Industrialist") to autonomous agents, the system observes how liquidity crises, asset bubbles, and wealth distribution organically emerge from individual micro-decisions.

The system features a centralized Market authority that enforces strict economic rules ("Laws of Physics" for assets) while allowing agents to negotiate via public order books and private direct messaging.

## Architecture

The system is built using Python and LangGraph, following a strictly modular architecture that separates agent cognition from simulation state management.

### Core Components

1.  **The Agent (Cognitive Layer)**
    Each participant is an instance of the `Agent` class. The agent does not directly manipulate the simulation database. Instead, it perceives the world through a constructed context (rendered via Jinja2 templates) containing:
    * **Memory:** A persistent internal monologue that evolves every turn.
    * **Inventory:** Real-time read of cash and assets (Apple, Chip, Gold).
    * **Market Board:** Public active offers.
    * **Ticker Tape:** A log of recent trades (public and private) to signal market temperature.
    * **Inbox:** Private notifications and direct offers.

    The Agent's decision-making process is a state graph (LangGraph) consisting of:
    * **Analysis Node:** Reads the context and updates the internal monologue/strategy.
    * **Router:** Decides whether to act or wait.
    * **Action Node:** Executes tools (`create_offer`, `accept_offer`) if applicable.

2.  **The Market (Source of Truth)**
    The `Market` class acts as the central authority and clearinghouse. It holds the "God View" of the simulation.
    * **Validation:** It enforces logic (e.g., an agent cannot sell what they do not own; an agent cannot buy without sufficient cash).
    * **Execution:** It performs atomic transactions, transferring assets and cash between agent inventories.
    * **Broadcasting:** It updates the public board and sends notifications to agent inboxes.

3.  **The Simulation Loop (Orchestrator)**
    A main control loop iterates through rounds. In each round, every agent is triggered sequentially. The loop manages the flow of time and persists transaction data for post-simulation analysis.

### Data Flow Diagram

```mermaid
graph TD
    subgraph Simulation Environment
        DB[(Simulation Database)]
        M[Market Authority]
    end

    subgraph Agent Process
        Ctx[Context Builder]
        LG[LangGraph Workflow]
        Tools[Tool Execution]
    end

    DB -->|Inventory & Prices| M
    M -->|Market State| Ctx
    DB -->|Agent State| Ctx
    
    Ctx -->|Formatted Prompts| LG
    LG -->|Decision| Tools
    
    Tools -->|Function Call| M
    M -->|Validate & Commit| DB