import os
import asyncio
from dotenv import load_dotenv
from aztp_client import Aztp, whiteListTrustDomains


async def main():
    # Load environment variables
    load_dotenv()

    # Initialize the client with API key from environment
    api_key = os.getenv("AZTP_API_KEY")
    if not api_key:
        raise ValueError("AZTP_API_KEY is not set")

    client = Aztp(api_key=api_key)

    try:
        # Display available trusted domains
        print("\nAvailable Trusted Domains:")
        print(whiteListTrustDomains)

        # Create base agents
        crew_agent = {}
        agent_name = "PolicyDemoAgentPY"

        # Issue identity
        print(f"1. Issuing identity for agent: {agent_name}")
        secured_agent = await client.secure_connect(
            crew_agent,
            agent_name,
            {
                "isGlobalIdentity": True
            }
        )
        print("AZTP ID:", secured_agent)

        # Get and display policy information
        print(f"\n2. Getting policy information for agent: {agent_name}")
        identity_access_policy = await client.get_policy(
            secured_agent.identity.aztp_id
        )

        # Display policy information
        print("\nPolicy Information:")
        if isinstance(identity_access_policy, dict):
            # Handle dictionary response
            for policy in identity_access_policy.get('data', []):
                print("\nPolicy Statement:", policy.get('policyStatement'))
                statement = policy.get('policyStatement', {}).get(
                    'Statement', [{}])[0]
                if statement.get('Effect') == "Allow":
                    print("Statement Effect:", statement.get('Effect'))
                    print("Statement Actions:", statement.get('Action'))
                    if 'Condition' in statement:
                        print("Statement Conditions:",
                              statement.get('Condition'))
                    print("Identity:", policy.get('identity'))
        else:
            # Handle string response
            print(identity_access_policy)

    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    asyncio.run(main())
