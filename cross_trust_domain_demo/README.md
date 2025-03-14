# Cross-Trust-Domain Identity Verification Demo

This demo showcases how agents from different trust domains (representing different companies or organizations) can securely interact with each other after proper identity verification.

## Prerequisites

- Python 3.8 or higher
- Two different AZTP API keys (representing different users/companies)

## Setup

1. Clone this repository
2. Navigate to the `cross_trust_domain_demo` directory
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   This will install:
   - aztp-client (AZTP client library)
   - python-dotenv (for environment variable management)
   - termcolor (required by aztp-client)

4. Set up the environment files using the setup script:
   ```
   python setup.py
   ```
   This interactive script will help you create:
   - `.env.research` for the Research Agent
   - `.env.blog` for the Blog Agent
   
   You can either use your own API keys or use sample keys for testing.

   Alternatively, you can manually create these files:

   **`.env.research`**:
   ```
   AZTP_API_KEY_RESEARCH=your_first_api_key_here
   ```

   **`.env.blog`**:
   ```
   AZTP_API_KEY_BLOG=your_second_api_key_here
   ```

## Running the Demo

There are three ways to run the demo:

### 1. Run the complete demo

```bash
python src/demo.py
```

This will:
- Create both agents with their respective API keys and trust domains
- Demonstrate the verification process
- Show the data exchange after successful verification

### 2. Run the Research Agent separately

```bash
python src/research_agent.py
```

This will:
- Create the Research Agent with its API key and trust domain
- Output the agent's AZTP ID for use with the Blog Agent

### 3. Run the Blog Agent separately

```bash
python src/blog_agent.py --research_agent_id AZTP-ID-FROM-RESEARCH-AGENT
```

This will:
- Create the Blog Agent with its API key and trust domain
- Attempt to verify and interact with the Research Agent using the provided ID

## Understanding the Output

The demo output will show:

1. Agent creation process for both agents
2. Identity verification attempts
3. Results of verification (success or failure)
4. Data exchange between agents (if verification succeeds)

## Modifying the Demo

You can modify the demo to test different scenarios:

- Change the trust domains in the code
- Modify the verification logic
- Add additional agents or trust domains
- Use the `--fail` flag with demo.py to demonstrate failed verification

## Troubleshooting

- Ensure both API keys are valid and have the necessary permissions
- Check that the trust domains are correctly configured
- Verify that the AZTP IDs are correctly passed between agents
- If you encounter any dependency issues, make sure all packages in requirements.txt are installed
- If you get an error about missing environment variables, run `python setup.py` to create the necessary .env files 