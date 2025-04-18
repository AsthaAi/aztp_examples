# AZTP Policy Demo (Python)

This is a Python demonstration of the AZTP (Agentic Zero Trust Protocol) client library, showing how to work with policies and identities.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory with your AZTP API key:
   ```
   AZTP_API_KEY=your_api_key_here
   ```

## Running the Demo

To run the policy demo:

```bash
python src/policy_demo.py
```

The demo will:

1. Display available trusted domains
2. Create a secure agent with a global identity
3. Retrieve and display the policy information for the agent

## Features Demonstrated

- Initializing the AZTP client
- Creating a secure agent
- Retrieving policy information
- Working with trusted domains
- Error handling

## Error Handling

The demo includes basic error handling for:

- Missing API key
- Connection issues
- Policy retrieval errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.
