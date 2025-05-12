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
            {"isGlobalIdentity": True}
        )
        print("AZTP ID:", getattr(secured_agent.identity, 'aztp_id', secured_agent))

        # Verify the identity
        print(f"2. Verifying identity for agent: {agent_name}")
        verified_agent = await client.verify_identity(secured_agent)
        print("Verified Agent:", verified_agent)

        # Revoke the identity
        print(f"3. Revoking identity for agent: {agent_name}")
        revoke_result = await client.revoke_identity(
            secured_agent.identity.aztp_id,
            "Temporary Revocation"
        )
        print("Revoked Agent:", revoke_result)

        # Verify after revoke
        print(f"4. Verifying identity after revocation for agent: {agent_name}")
        is_valid_after_revoke = await client.verify_identity(secured_agent)
        print("Identity Valid After Revoke:", is_valid_after_revoke)

        # Reissue the identity
        print(f"5. Reissuing identity for agent: {agent_name}")
        reissue_result = await client.reissue_identity(
            secured_agent.identity.aztp_id
        )
        print("Identity Reissued:", reissue_result)

        # Verify after reissue
        print(f"6. Verifying identity after reissue for agent: {agent_name}")
        is_valid_after_reissue = await client.verify_identity(secured_agent)
        print("Identity Valid After Reissue:", is_valid_after_reissue)

        # Get and display policy information
        print(f"\n7. Getting policy information for agent: {agent_name}")
        identity_access_policy = await client.get_policy(
            secured_agent.identity.aztp_id
        )

        # Extract a specific policy by code (replace with your actual policy code)
        policy_code = "policy:9ca1aadf1964"  # Replace with your actual policy code
        policy = client.get_policy_value(
            identity_access_policy,
            "code",
            policy_code
        )
        print("\nPolicy:", policy)

        if policy:
            is_allow = client.is_action_allowed(policy, "list_users")
            print({"is_allow": is_allow})
            if is_allow:
                print("Allowed to run the action")
            else:
                print("Not allowed to run the action")
        else:
            print("Policy not found.")

    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    asyncio.run(main())
