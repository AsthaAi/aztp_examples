import asyncio
import os
from dotenv import load_dotenv
from aztp_client import Aztp
from aztp_client.common.config import whiteListTrustDomains 

# Load environment variables
load_dotenv()

# Initialize empty objects for all agents and tools
# SDRAgent (Global Parent) and its tools
sdr_agent = {}

# CustomerServiceAgent and its tools
customer_service_agent = {}
jira = {}
slack = {}
notion = {}
airtable = {}

# SalesAgent and its tools
sales_agent = {}
salesforce = {}
asana = {}
tableau = {}
gmail = {}

# RegionalSales agents and their tools
regional_sales1 = {}
regional_sales2 = {}
trello = {}
hubspot = {}
clickup = {}
zoom = {}

# LocalSales agents and their tools
local_sales = [{} for _ in range(4)]  # LocalSales1-4
figma = {}
mem0 = {}
docusign = {}
linkedin = {}

# SupportAgent and its tools
support_agent = {}
zendesk = {}
confluence = {}
teams = {}
monday = {}

# TechSupport agents and their tools
tech_support1 = {}
tech_support2 = {}
jira_service = {}
github = {}
tech_notion = {}
tech_slack = {}

async def main():
    try:
        # Initialize AZTP client
        API_KEY = os.getenv("AZTP_API_KEY")
        if not API_KEY:
            raise ValueError("AZTP_API_KEY environment variable is not set")

        client = Aztp(api_key=API_KEY)
        trust_domain = "gptarticles.xyz"

        print("\n1. Creating SDRAgent (Global)...")
        secured_sdr = await client.secure_connect(
            sdr_agent,
            "giveUniqueName", #Give unique name. Think this like domain name. If it is taken, you will get error in terminal. To fix that error, just chan
            {
                "isGlobalIdentity": True,
            }
        )
        print('SDRAgent AZTP ID:', secured_sdr.identity.aztp_id)
        # Verify SDRAgent identity
        sdr_verified = await client.verify_identity(secured_sdr)
        print('SDRAgent Identity Verified:', sdr_verified)

        # Create and secure CustomerServiceAgent
        print("\n2. Creating CustomerServiceAgent...")
        secured_customer_service = await client.secure_connect(
            customer_service_agent,
            'customer-friday',
            {
                "parentIdentity": secured_sdr.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('CustomerServiceAgent AZTP ID:', secured_customer_service.identity.aztp_id)
        # Verify CustomerServiceAgent identity
        cs_verified = await client.verify_identity(
            secured_customer_service
        )
        print('CustomerServiceAgent Identity Verified:', cs_verified)

        # Secure CustomerServiceAgent's tools
        print("\nSecuring CustomerServiceAgent's tools...")
        secured_jira = await client.secure_connect(
            jira,
            'jira1',
            {
                "parentIdentity": secured_customer_service.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        
        jira_verified = await client.verify_identity(
            secured_jira
        )
        print('Jira Tool Identity Verified:', jira_verified)

        secured_slack = await client.secure_connect(
            slack,
            'slackFriday',
            {
                "parentIdentity": secured_customer_service.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Slack Tool AZTP ID:', secured_slack.identity.aztp_id)

        slack_verified = await client.verify_identity(
            secured_slack
        )
        print('Slack Tool Identity Verified:', slack_verified)

        secured_notion = await client.secure_connect(
            notion, 
            'notion1',
            {
                "parentIdentity": secured_customer_service.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Notion Tool AZTP ID:', secured_notion.identity.aztp_id)

        secured_airtable = await client.secure_connect(
            airtable,
            'airtable1',
            {
                "parentIdentity": secured_customer_service.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Airtable Tool AZTP ID:', secured_airtable.identity.aztp_id)

        # Create and secure SalesAgent
        print("\n3. Creating SalesAgent...")
        secured_sales = await client.secure_connect(
            sales_agent,
            'sales-agent-2',
            {
                "parentIdentity": secured_sdr.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('SalesAgent AZTP ID:', secured_sales.identity.aztp_id)
        sales_verified = await client.verify_identity_using_agent_name(
            'sales-agent-2',
            trust_domain=trust_domain,
        )
        print('SalesAgent Identity Verified:', sales_verified)

        # Secure SalesAgent's tools
        print("\nSecuring SalesAgent's tools...")
        secured_salesforce = await client.secure_connect(
            salesforce,
            'salesforce1',
            {
                "parentIdentity": secured_sales.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Salesforce Tool AZTP ID:', secured_salesforce.identity.aztp_id)
       

        sales_verified = await client.verify_identity(
            secured_sales
        )
        print('SalesAgent Identity Verified by agent object:', sales_verified)

        secured_asana = await client.secure_connect(
            asana,
            'asana1',
            {
                "parentIdentity": secured_sales.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Asana Tool AZTP ID:', secured_asana.identity.aztp_id)

        secured_tableau = await client.secure_connect(
            tableau,
            'tableau1',
            {
                "parentIdentity": secured_sales.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Tableau Tool AZTP ID:', secured_tableau.identity.aztp_id)

        secured_gmail = await client.secure_connect(
            gmail,
            'gmail1',
            {
                "parentIdentity": secured_sales.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Gmail Tool AZTP ID:', secured_gmail.identity.aztp_id)

        # Create and secure RegionalSales agents
        regional_agents = []
        for i in range(2):
            print(f"\n4. Creating RegionalSales{i+1}...")
            secured_regional = await client.secure_connect(
                regional_sales1 if i == 0 else regional_sales2,
                f"regional-sales1-{i+1}",
                {
                    "parentIdentity": secured_sales.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'RegionalSales{i+1} AZTP ID:', secured_regional.identity.aztp_id)
            regional_verified = await client.verify_identity(
                secured_regional
            )
            print(f'RegionalSales{i+1} Identity Verified:', regional_verified)
            regional_agents.append(secured_regional)

            # Secure RegionalSales tools
            print(f"\nSecuring RegionalSales{i+1}'s tools...")
            secured_trello = await client.secure_connect(
                trello,
                'trello1',
                {
                    "parentIdentity": secured_regional.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Trello Tool AZTP ID:', secured_trello.identity.aztp_id)
            trello_verified = await client.verify_identity(
                secured_trello
            )
            print('Trello Tool Identity Verified:', trello_verified)

            secured_hubspot = await client.secure_connect(
                hubspot,
                'hubspot1',
                {
                    "parentIdentity": secured_regional.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Hubspot Tool AZTP ID:', secured_hubspot.identity.aztp_id)
            hubspot_verified = await client.verify_identity(
                secured_hubspot
            )
            print('Hubspot Tool Identity Verified:', hubspot_verified)

            secured_clickup = await client.secure_connect(
                clickup,
                'clickup1',
                {
                    "parentIdentity": secured_regional.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Clickup Tool AZTP ID:', secured_clickup.identity.aztp_id)
            clickup_verified = await client.verify_identity(
                secured_clickup
            )
            print('Clickup Tool Identity Verified:', clickup_verified)

            secured_zoom = await client.secure_connect(
                zoom,
                'zoom1',
                {
                    "parentIdentity": secured_regional.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Zoom Tool AZTP ID:', secured_zoom.identity.aztp_id)
            zoom_verified = await client.verify_identity(
                secured_zoom
            )
            print('Zoom Tool Identity Verified:', zoom_verified)

        # Create and secure LocalSales agents
        for i, regional_agent in enumerate(regional_agents):
            for j in range(2):
                local_index = i * 2 + j
                print(f"\n5. Creating LocalSales{local_index+1}...")
                secured_local = await client.secure_connect(
                    local_sales[local_index],
                    f"local-sales-1-{local_index+1}",
                    {
                        "parentIdentity": regional_agent.identity.aztp_id,
                        "trustDomain": trust_domain,
                        "isGlobalIdentity": False
                    }
                )
                print(f'LocalSales{local_index+1} AZTP ID:', secured_local.identity.aztp_id)
                local_verified = await client.verify_identity(
                    secured_local
                )
                print(f'LocalSales{local_index+1} Identity Verified:', local_verified)

                # Secure LocalSales tools
                print(f"\nSecuring LocalSales{local_index+1}'s tools...")
                secured_figma = await client.secure_connect(
                    figma,
                    'figma1',
                    {
                        "parentIdentity": secured_local.identity.aztp_id,
                        "trustDomain": trust_domain,
                        "isGlobalIdentity": False
                    }
                )
                print(f'Figma Tool AZTP ID:', secured_figma.identity.aztp_id)
                figma_verified = await client.verify_identity(
                    secured_figma
                )
                print('Figma Tool Identity Verified:', figma_verified)

                secured_mem0 = await client.secure_connect(
                    mem0,
                    'mem01',
                    {
                        "parentIdentity": secured_local.identity.aztp_id,
                        "trustDomain": trust_domain,
                        "isGlobalIdentity": False
                    }
                )
                print(f'Mem0 Tool AZTP ID:', secured_mem0.identity.aztp_id)
                mem0_verified = await client.verify_identity(
                    secured_mem0
                )
                print('Mem0 Tool Identity Verified:', mem0_verified)

                secured_docusign = await client.secure_connect(
                    docusign,
                    'docusign1',
                    {
                        "parentIdentity": secured_local.identity.aztp_id,
                        "trustDomain": trust_domain,
                        "isGlobalIdentity": False
                    }
                )
                print(f'DocuSign Tool AZTP ID:', secured_docusign.identity.aztp_id)
                docusign_verified = await client.verify_identity(
                    secured_docusign
                )
                print('DocuSign Tool Identity Verified:', docusign_verified)

                secured_linkedin = await client.secure_connect(
                    linkedin,
                    'linkedin1',
                    {
                        "parentIdentity": secured_local.identity.aztp_id,
                        "trustDomain": trust_domain,
                        "isGlobalIdentity": False
                    }
                )
                print(f'LinkedIn Tool AZTP ID:', secured_linkedin.identity.aztp_id)
                linkedin_verified = await client.verify_identity(
                    secured_linkedin
                )
                print('LinkedIn Tool Identity Verified:', linkedin_verified)

        # Create and secure SupportAgent
        print("\n6. Creating SupportAgent...")
        secured_support = await client.secure_connect(
            support_agent,
            'support-agent-2',
            {
                "parentIdentity": secured_sdr.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('SupportAgent AZTP ID:', secured_support.identity.aztp_id)
        support_verified = await client.verify_identity(
            secured_support
        )
        print('SupportAgent Identity Verified:', support_verified)

        # Secure SupportAgent's tools
        print("\nSecuring SupportAgent's tools...")
        secured_zendesk = await client.secure_connect(
            zendesk,
            'zendesk1',
            {
                "parentIdentity": secured_support.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Zendesk Tool AZTP ID:', secured_zendesk.identity.aztp_id)
        zendesk_verified = await client.verify_identity(
            secured_zendesk
        )
        print('Zendesk Tool Identity Verified:', zendesk_verified)

        secured_confluence = await client.secure_connect(
            confluence,
            'confluence1',
            {
                "parentIdentity": secured_support.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Confluence Tool AZTP ID:', secured_confluence.identity.aztp_id)
        confluence_verified = await client.verify_identity(
            secured_confluence
        )
        print('Confluence Tool Identity Verified:', confluence_verified)

        secured_teams = await client.secure_connect(
            teams,
            'teams1',
            {
                "parentIdentity": secured_support.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Teams Tool AZTP ID:', secured_teams.identity.aztp_id)
        teams_verified = await client.verify_identity(
            secured_teams
        )
        print('Teams Tool Identity Verified:', teams_verified)

        secured_monday = await client.secure_connect(
            monday,
            'monday1',
            {
                "parentIdentity": secured_support.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False
            }
        )
        print('Monday Tool AZTP ID:', secured_monday.identity.aztp_id)
        monday_verified = await client.verify_identity(
            secured_monday
        )
        print('Monday Tool Identity Verified:', monday_verified)

        # Create and secure TechSupport agents
        for i in range(2):
            print(f"\n7. Creating TechSupport{i+1}...")
            secured_tech = await client.secure_connect(
                tech_support1 if i == 0 else tech_support2,
                f"tech-support-{i+1}",
                {
                    "parentIdentity": secured_support.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'TechSupport{i+1} AZTP ID:', secured_tech.identity.aztp_id)
            tech_verified = await client.verify_identity(
                secured_tech
            )
            print(f'TechSupport{i+1} Identity Verified:', tech_verified)

            # Secure TechSupport tools
            print(f"\nSecuring TechSupport{i+1}'s tools...")
            secured_jira_service = await client.secure_connect(
                jira_service,
                'jira-service',
                {
                    "parentIdentity": secured_tech.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Jira Service Tool AZTP ID:', secured_jira_service.identity.aztp_id)
            jira_service_verified = await client.verify_identity(
                secured_jira_service
            )
            print('Jira Service Tool Identity Verified:', jira_service_verified)

            secured_github = await client.secure_connect(
                github,
                'github1',
                {
                    "parentIdentity": secured_tech.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'GitHub Tool AZTP ID:', secured_github.identity.aztp_id)
            github_verified = await client.verify_identity(
                secured_github
            )
            print('GitHub Tool Identity Verified:', github_verified)

            secured_tech_notion = await client.secure_connect(
                tech_notion,
                'tech-notion1',
                {
                    "parentIdentity": secured_tech.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Tech Notion Tool AZTP ID:', secured_tech_notion.identity.aztp_id)
            tech_notion_verified = await client.verify_identity(
                secured_tech_notion
            )
            print('Tech Notion Tool Identity Verified:', tech_notion_verified)

            secured_tech_slack = await client.secure_connect(
                tech_slack,
                'tech-slack1',
                {
                    "parentIdentity": secured_tech.identity.aztp_id,
                    "trustDomain": trust_domain,
                    "isGlobalIdentity": False
                }
            )
            print(f'Tech Slack Tool AZTP ID:', secured_tech_slack.identity.aztp_id)
            tech_slack_verified = await client.verify_identity(
                secured_tech_slack
            )
            print('Tech Slack Tool Identity Verified:', tech_slack_verified)

        print("\nFinal Agent Hierarchy:")
        print("SDRAgent (Global)")
        print("├── CustomerServiceAgent")
        print("│   └── Tools: jira, slack, notion, airtable")
        print("├── SalesAgent")
        print("│   ├── Tools: salesforce, asana, tableau, gmail")
        print("│   ├── RegionalSales1")
        print("│   │   ├── Tools: trello, hubspot, clickup, zoom")
        print("│   │   ├── LocalSales1")
        print("│   │   │   └── Tools: figma, mem0, docusign, linkedin")
        print("│   │   └── LocalSales2")
        print("│   │       └── Tools: figma, mem0, docusign, linkedin")
        print("│   └── RegionalSales2")
        print("│       ├── Tools: trello, hubspot, clickup, zoom")
        print("│       ├── LocalSales3")
        print("│       │   └── Tools: figma, mem0, docusign, linkedin")
        print("│       └── LocalSales4")
        print("│           └── Tools: figma, mem0, docusign, linkedin")
        print("└── SupportAgent")
        print("    ├── Tools: zendesk, confluence, teams, monday")
        print("    ├── TechSupport1")
        print("    │   └── Tools: jira_service, github, notion, slack")
        print("    └── TechSupport2")
        print("        └── Tools: jira_service, github, notion, slack")

    except Exception as error:
        print('Error:', str(error))

if __name__ == "__main__":
    asyncio.run(main()) 