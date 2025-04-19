# Blog Generation with AZTP Trust Chain

This example demonstrates how to create a secure blog generation system using AZTP (Astha Zero Trust Protocol) to establish trust between different components.

## Components

1. **Research Agent**: Conducts research on given topics using OpenAI's API
2. **Blog Agent**: Creates blog posts based on research findings
3. **Storage Service**: Manages local storage of blog posts in Markdown format

## Trust Chain

The system establishes a secure trust chain between components:
- Research Agent ↔️ Blog Agent (bi-directional trust)
- Blog Agent ↔️ Storage Service (bi-directional trust)

## Storage Implementation

The system stores blog posts locally with the following features:
- Blog posts are saved as Markdown files with YAML frontmatter
- Each file includes metadata (author, researcher, date, status)
- Files are stored in a `blogs` directory in the project root
- Filenames are generated using timestamps and sanitized titles
- Example filename: `2024-02-15T10-30-45-123Z-zero-trust-architecture-in-ai-systems.md`

## Setup

1. Create a `.env` file with your API keys:
```
AZTP_API_KEY=your_aztp_api_key
OPENAI_API_KEY=your_openai_api_key
```

2. Install dependencies:
```bash
npm install
```

## Usage

Run the example:
```bash
npm run dev
```

This will:
1. Initialize and secure all components with AZTP
2. Conduct research on a topic
3. Generate a blog post
4. Save the post to local storage
5. List all available blog posts

## Blog Post Format

Each blog post is saved with the following structure:
```markdown
---
title: Post Title
author: Blog Agent
researcher: Research Agent
date: 2024-02-15T10:30:45.123Z
status: completed
---

Blog content here...
```

## Directory Structure

```
.
├── src/
│   ├── agents/
│   │   ├── research-agent.ts
│   │   └── blog-agent.ts
│   ├── services/
│   │   └── storage.ts
│   └── main.ts
├── blogs/           # Generated blog posts are stored here
├── .env
└── README.md
```

## Error Handling

The system includes comprehensive error handling for:
- Missing API keys
- Failed trust chain verification
- Storage operation failures
- Broken connections between components