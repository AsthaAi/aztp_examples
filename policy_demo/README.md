# AZTP Policy Demo

This project demonstrates the usage of the AZTP Client library for managing and retrieving policy information.

## Prerequisites

- Node.js >= 14.0.0
- npm or yarn
- AZTP API Key

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the root directory and add your AZTP API key:
   ```
   AZTP_API_KEY=your_api_key_here
   ```

## Running the Demo

To run the demo:

```bash
npm start
```

This will:

1. Initialize the AZTP client
2. Create a secured agent
3. Retrieve and display the policy information for the agent

## Project Structure

- `src/policyDemo.ts` - Main demo file
- `.env` - Environment variables (API key)
- `package.json` - Project configuration and dependencies
- `tsconfig.json` - TypeScript configuration

## Available Scripts

- `npm start` - Run the demo
- `npm run build` - Build the TypeScript code
- `npm run dev` - Run in development mode with auto-reload
