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

    // Get and display policy information
    console.log("\n2. Getting policy information for agent:", agentName);
    const identityAccessPolicy = await aztpClient.getPolicy(
      securedAgent.identity.aztpId
    );

    // Display policy information
    console.log("\nPolicy Information:");
    for (const policy of identityAccessPolicy.data) {
      console.log("\nPolicy Statement:", policy.policyStatement);
      if (policy.policyStatement.Statement[0].Effect === "Allow") {
        console.log(
          "Statement Effects:",
          policy.policyStatement.Statement[0].Effect
        );
        console.log(
          "Statement Actions1:",
          policy.policyStatement.Statement[0].Action
        );
        if (policy.policyStatement.Statement[0].Condition) {
          console.log(
            "Statement Conditions:",
            policy.policyStatement.Statement[0].Condition
          );
        }
        console.log("Identity:", policy.identity);
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

main().catch(console.error);
