# Blog Generation System (Python)

A secure multi-agent system that generates blog posts using OpenAI and AZTP security. This example demonstrates how to:
- Create and secure multiple AI agents
- Implement secure agent-to-agent communication
- Verify agent identities
- Handle secure data flow

## Architecture

```
┌──────────────┐                              ┌──────────────┐
│  Research    │                              │    Blog      │
│   Agent      │    Agentic Zero Trust       │   Agent      │
│              │◄─────── Protocol ──────────►│              │
│  (OpenAI)    │         (AZTP)              │  (OpenAI)    │
└──────────────┘                              └──────────────┘
```

## Prerequisites

- Python >= 3.8
- OpenAI API key
- AZTP API key (get one at [astha.ai](https://astha.ai))

## Setup

1. Create a virtual environment (recommended):
```bash
cd blog_python
python -m venv <your-env-name>
source <your-env-name>/bin/activate  # On Windows: <your-env-name>\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_key_here

# AZTP Configuration
AZTP_API_KEY=your_aztp_key_here
```

## Running the Example

1. Make sure your virtual environment is activated
2. Run the main script:
```bash
python src/main.py
```

## Implementation Details

### 1. Initialize AZTP Client
```python
import aztp_client as aztp

client = aztp.initialize({
    'api_key': os.getenv('AZTP_API_KEY')
})
```

### 2. Create and Secure Agents
```python
# Create base agents
research_agent = ResearchAgent(openai_api_key)
blog_agent = BlogAgent(openai_api_key)

# Secure the agents
secured_research = await client.secure_connect(research_agent, {
    'name': "research-assistant"
})

secured_blog = await client.secure_connect(blog_agent, {
    'name': "blog-writer"
})
```

### 3. Verify Agent Identities
```python
# Verify both agents
if not all([
    await client.verify_identity(secured_research),
    await client.verify_identity(secured_blog)
]):
    raise SecurityError("Agent identity verification failed")
```

### 4. Use Secured Agents
```python
# Research phase
research_data = await secured_research.research(topic)

# Blog writing phase
blog_content = await secured_blog.create_blog(research_data)
```

## Project Structure

```
blog_python/
├── src/
│   ├── agents/
│   │   ├── research_agent.py   # Research agent implementation
│   │   └── blog_agent.py       # Blog agent implementation
│   └── main.py                # Main orchestration
├── requirements.txt
└── README.md
```

## Security Features Demonstrated

- 🔐 Agent identity management with SPIFFE
- 🤝 Secure agent-to-agent communication
- ✅ Identity verification before operations
- 📝 Automatic method delegation

## Output

The system generates blog posts in markdown format, saved in `output/blogs/` directory with timestamps.

## Error Handling

The example includes error handling for:
- Missing API keys
- Identity verification failures
- Agent communication errors
- File system operations 
