# Blog Generation with AZTP Trust Chain (Python)

This example demonstrates how to create a secure blog generation system using AZTP (Astha Zero Trust Protocol) to establish trust between different components.

## Components

1. **Research Agent**: Conducts research on given topics using OpenAI's API
2. **Blog Agent**: Creates blog posts based on research findings
3. **Storage Service**: Manages local storage of blog posts in Markdown format

## Trust Chain Architecture

The system establishes a secure trust chain between components:

```
Blog Agent (Global Identity)
├── Research Agent (Child) ↔️ Blog Agent
└── Storage Service (Child) ↔️ Blog Agent
```

All connections are bi-directional and verified before operations:
- Research Agent ↔️ Blog Agent
- Blog Agent ↔️ Storage Service

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
OPENAI_API_KEY=your_openai_api_key
AZTP_API_KEY=your_aztp_api_key
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the example:
```bash
python src/main.py
```

This will:
1. Initialize and secure all components with AZTP:
   - Blog Agent as global identity
   - Research Agent as child of Blog Agent
   - Storage Service as child of Blog Agent
2. Verify bi-directional trust between components
3. Conduct research on a topic
4. Generate a blog post
5. Save the post to local storage
6. List all available blog posts

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
│   │   ├── research_agent.py
│   │   └── blog_agent.py
│   ├── services/
│   │   └── storage.py
│   └── main.py
├── blogs/           # Generated blog posts are stored here
├── requirements.txt
├── .env
└── README.md
```

## Error Handling

The system includes comprehensive error handling for:
- Missing API keys
- Failed trust chain verification
- Storage operation failures
- Broken connections between components
- Component verification failures

## Connection Verification

The system verifies:
1. Component identities:
   - Research Agent
   - Blog Agent
   - Storage Service

2. Bi-directional connections:
   - Research Agent → Blog Agent
   - Blog Agent → Research Agent
   - Blog Agent → Storage Service
   - Storage Service → Blog Agent

All verifications must pass before any operations are performed.

