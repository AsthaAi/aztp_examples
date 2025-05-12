import aztp, { whiteListTrustDomains } from "aztp-client";
import dotenv from "dotenv";

dotenv.config();

async function main() {
  // Initialize the client with API key from environment
  const API_KEY = process.env.AZTP_API_KEY;
  if (!API_KEY) {
    throw new Error("AZTP_API_KEY is not set");
  }

  const aztpClient = aztp.initialize({
    apiKey: API_KEY,
  });

  try {
    // Display available trusted domains
    console.log("\nAvailable Trusted Domains:");
    console.log(whiteListTrustDomains);

    // Create base agents
    const crewAgent = {};
    const agentName = "PolicyDemoAgent";

    // Issue identity
    console.log("1. Issuing identity for agent:", agentName);
    const securedAgent = await aztpClient.secureConnect(crewAgent, agentName, {
      isGlobalIdentity: true,
    });
    console.log("AZTP ID:", securedAgent);

    // Verify the identity
    console.log("2. Verifying identity for agent:", agentName);
    const verifiedAgent = await aztpClient.verifyIdentity(securedAgent);
    console.log("Verified Agent:", verifiedAgent);

    // Revoke the identity
    console.log("3. Revoking identity for agent:", agentName);
    const revokedAgent = await aztpClient.revokeIdentity(
      securedAgent.identity.aztpId,
      "Temporary Revocation"
    );
    console.log("Revoked Agent:", revokedAgent);

    // Verify the identity again
    console.log("4. Verifying identity after revocation for agent:", agentName);
    const verifiedAgentAfterRevocation = await aztpClient.verifyIdentity(
      securedAgent
    );
    console.log(
      "Verified Agent after revocation:",
      verifiedAgentAfterRevocation
    );

    // Reissue the identity
    console.log("5. Reissuing identity for agent:", agentName);
    const reissuedAgent = await aztpClient.reissueIdentity(
      securedAgent.identity.aztpId
    );
    console.log("Reissued Agent after reissue:", reissuedAgent);

    // Verify the reissued identity
    console.log("6. Verifying reissued identity for agent:", agentName);
    const verifiedAgentAfterReissue = await aztpClient.verifyIdentity(
      securedAgent
    );
    console.log("Verified Reissued Agent:", verifiedAgentAfterReissue);

    // Get and display policy information
    console.log("\n7. Getting policy information for agent:", agentName);
    const identityAccessPolicy = await aztpClient.getPolicy(
      securedAgent.identity.aztpId
    );

    const policy = aztpClient.getPolicyValue(
      identityAccessPolicy.data,
      "code",
      "policy:9ca1aadf1964"
    );

    console.log("\nPolicy:", policy);

    if (policy) {
      const isAllow = aztpClient.isActionAllowed(policy, "list_users");
      console.log({ isAllow });
      if (isAllow) {
        console.log("Allowed to run the action");
      } else {
        console.log("Not allowed to run the action");
      }
    } else {
      console.log("Policy not found");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

main().catch(console.error);
