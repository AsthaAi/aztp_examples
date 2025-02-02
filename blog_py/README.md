# AI Blog Generation with Secure Agents

A system that uses two AI agents (Research and Blog) working together to generate blog posts about AI security topics. The agents are secured using AZTP (Astha Zero Trust Protocol) for identity verification.

## Core Concept: AZTP Integration

AZTP (Agentic Zero Trust Protocol) follows a key design principle: transparent security wrapping. Here's how it works:

1. **Transparent Method Delegation**
   - AZTP wraps AI agents without modifying their core functionality
   - All agent methods (e.g., research, execute) work exactly as they would without AZTP
   - The security layer is completely transparent to the agent's operation

2. **Separation of Concerns**
   ```python
   # CrewAI handles agent functionality
   research_agent = ResearchAgent()
   
   # AZTP adds security without changing behavior
   secured_agent = await client.secure_connect(research_agent, "research-agent")
   
   # Use agent methods normally - AZTP is invisible to functionality
   result = await secured_agent.research(topic)
   ```

3. **What AZTP Adds**
   - Identity management (SPIFFE IDs)
   - Identity verification capabilities
   - Zero-trust security model through identity verification
   
4. **What AZTP Doesn't Do**
   - Modify agent behavior
   - Change method signatures
   - Interfere with CrewAI functionality
   - Alter agent outputs
   - Handle communication between agents (this happens at application level)

This design ensures that developers can focus on agent functionality while AZTP handles identity and verification independently. While agents can verify each other's identities through AZTP, the actual communication between agents is handled at the application level.

## Project Structure

```
blog/
├── agents/
│   ├── research_agent.py   # Research agent implementation
│   └── blog_agent.py       # Blog writing agent implementation
├── main.py                 # Main orchestration script
├── requirements.txt        # Project dependencies
└── output/                 # Generated blog posts
    └── blogs/             
```

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   OPENAI_API_KEY=your-openai-key
   AZTP_API_KEY=your-aztp-key
   AZTP_ENV=local
   ```

## Usage

Run the main script:
```bash
python main.py
```

This will:
1. Initialize and secure both agents with AZTP
2. Generate research on AI security topics
3. Transform research into blog posts
4. Save posts to the output directory

