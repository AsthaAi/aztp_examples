# Blog Generation System (TypeScript)

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

- Node.js >= 14.0.0
- TypeScript >= 4.9.0
- OpenAI API key
- AZTP API key (get one at [astha.ai](https://astha.ai))

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_key_here

# AZTP Configuration
AZTP_API_KEY=your_aztp_key_here
AZTP_ENV=local
```

## Running the Example

1. Build the project:
```bash
npm run build
```

2. Run the example:
```bash
npm start
```

## Implementation Details

### 1. Initialize AZTP Client
```typescript
import aztp from 'aztp-client';

const client = aztp.initialize({
    apiKey: process.env.AZTP_API_KEY
});
```

### 2. Create and Secure Agents
```typescript
// Create base agents
const researchAgent = new ResearchAgent(openaiApiKey);
const blogAgent = new BlogAgent(openaiApiKey);

// Secure the agents
const securedResearch = await client.secureConnect(researchAgent, {
    name: "research-assistant"
});

const securedBlog = await client.secureConnect(blogAgent, {
    name: "blog-writer"
});
```

### 3. Verify Agent Identities
```typescript
// Verify research agent
const researchValid = await client.verifyIdentity(securedResearch);
const researchIdentity = await client.getIdentity(securedResearch);

// Verify blog agent
const blogValid = await client.verifyIdentity(securedBlog);
const blogIdentity = await client.getIdentity(securedBlog);
```

### 4. Use Secured Agents
```typescript
// Research phase
const researchData = await securedResearch.research(topic);

// Blog writing phase
const blogData = await securedBlog.createBlog(researchData);
```

## Project Structure

```
blog_ts/
├── src/
│   ├── agents/
│   │   ├── research-agent.ts   # Research agent implementation
│   │   └── blog-agent.ts       # Blog agent implementation
│   ├── types.ts               # Type definitions
│   └── main.ts               # Main orchestration
├── package.json
└── tsconfig.json
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