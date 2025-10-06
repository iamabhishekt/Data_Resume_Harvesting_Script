import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def generate_dice_query_with_chatgpt(job_desc_file, output_file, api_key=None):
    """
    Generate Dice Boolean search query from job description using ChatGPT API
    """

    # Initialize OpenAI client
    if api_key is None:
        api_key = os.environ.get('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass it as parameter.")

    client = OpenAI(api_key=api_key)

    # Read job description
    try:
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
    except FileNotFoundError:
        print(f"Error: {job_desc_file} not found!")
        return None

    # Create the prompt for ChatGPT
    prompt = f"""
You are analyzing job descriptions to create a focused Dice.com Boolean search query.

IMPORTANT INSTRUCTIONS:
1. The input may contain MULTIPLE job descriptions from different roles/companies
2. If multiple roles are detected, create a query that covers the MOST COMMON or PRIMARY role
3. Focus ONLY on technical skills, tools, technologies, and platforms
4. STRICTLY EXCLUDE all soft skills
5. If one role clearly dominates (appears most), focus the query on that role

Job Descriptions:
{job_description}

CRITICAL QUERY STRUCTURE RULES:

1. ROLE VARIATIONS (First group only):
   - Use OR to connect role title variations
   - Example: ("SDET" OR "Software Development Engineer in Test" OR "Test Automation Engineer")

2. UNIQUE TECHNICAL SKILLS (Separate AND groups):
   - Each UNIQUE technical skill/technology gets its own AND group
   - Within each group, ONLY use OR for variations/synonyms/abbreviations of THE SAME THING
   - Example: Java is different from Python - MUST be separate AND groups
   - Example: Jenkins is different from Maven - MUST be separate AND groups
   - Example: Unix is different from Python - MUST be separate AND groups

3. WHAT GOES TOGETHER WITH OR (Same skill/technology):
   - Abbreviations of SAME thing: AWS OR "Amazon Web Services" OR "Amazon Cloud"
   - Services of SAME platform: EC2 OR S3 OR Lambda OR RDS (all AWS services)
   - Synonyms of SAME thing: Selenium OR "Selenium WebDriver" (both are Selenium)
   - Versions of SAME thing: Python OR Python3 OR "Python scripting" (all Python)
   - Expansions of SAME acronym: CI/CD OR "Continuous Integration" OR "Continuous Deployment"

4. WHAT MUST BE SEPARATE WITH AND (Different skills):
   - Different programming languages: Java AND Python (NOT: Java OR Python)
   - Different OS/platforms: Unix AND Windows (NOT: Unix OR Python)
   - Different tools: Jenkins AND Maven (NOT: Jenkins OR Maven)
   - Different testing tools: Selenium AND Cucumber (NOT: Selenium OR Cucumber)
   - Different frameworks: Spring AND Angular (NOT: Spring OR Angular)

QUERY STRUCTURE FORMAT:
(Role OR "Role Variation") AND (Skill1 OR Skill1_synonym OR Skill1_abbrev) AND (Skill2_DIFFERENT OR Skill2_synonym) AND (Skill3_DIFFERENT OR Skill3_synonym)

CORRECT EXAMPLES:

Example 1 - SDET (CORRECT):
("SDET" OR "Software Development Engineer in Test" OR "Test Automation Engineer")
AND (Java OR "Java/J2EE" OR J2EE OR JDK)
AND (Python OR Python3 OR "Python scripting")
AND (Selenium OR "Selenium WebDriver")
AND (Cucumber OR BDD OR "Cucumber BDD")
AND (AWS OR "Amazon Web Services" OR EC2 OR Lambda OR RDS OR Redshift OR EMR)
AND (Unix OR Linux OR "Unix shell scripting" OR "shell scripting")
AND (Angular OR "Angular JS" OR "Angular UI")
AND ("CI/CD" OR "Continuous Integration" OR "Continuous Deployment")
AND (Jenkins OR "Jenkins CI")
AND (Maven OR "Apache Maven")
AND ("Automated Testing" OR "test automation" OR "automation framework")

Why this is CORRECT:
✅ Java separate from Python (different languages)
✅ Selenium separate from Cucumber (different tools)
✅ Jenkins separate from Maven (different build tools)
✅ Unix variations stay together (Unix OR Linux - similar OS)
✅ AWS services together (all AWS)

Example 2 - Java Developer (CORRECT):
("Java Developer" OR "Java Engineer" OR "Backend Developer")
AND (Java OR "Java/J2EE" OR J2EE OR JDK)
AND ("Spring Boot" OR Spring OR "Spring Framework")
AND (Microservices OR "microservice architecture")
AND (AWS OR "Amazon Web Services" OR EC2 OR S3 OR Lambda)
AND (REST OR "REST API" OR RESTful OR "RESTful services")
AND (SQL OR "SQL queries" OR "SQL database")
AND (PostgreSQL OR Postgres)
AND (Docker OR "Docker containers")
AND (Kubernetes OR K8s OR "Kubernetes orchestration")
AND (Git OR GitHub OR GitLab OR "version control")

WRONG EXAMPLES (Do NOT do this):

❌ WRONG: (Java OR Python OR Selenium)
   - These are COMPLETELY DIFFERENT skills
   - Should be: (Java) AND (Python) AND (Selenium)

❌ WRONG: (Unix OR "Unix shell scripting" OR Python)
   - Python is a DIFFERENT programming language, not a Unix variation
   - Should be: (Unix OR Linux OR "Unix shell scripting") AND (Python OR Python3)

❌ WRONG: ("CI/CD" OR Jenkins OR Maven)
   - Jenkins and Maven are DIFFERENT tools
   - Should be: ("CI/CD" OR "Continuous Integration") AND (Jenkins) AND (Maven)

❌ WRONG: (Java OR "Java/J2EE" OR Python)
   - Python is DIFFERENT from Java
   - Should be: (Java OR "Java/J2EE" OR J2EE) AND (Python OR Python3)

❌ WRONG: (Selenium OR "Selenium WebDriver" OR Cucumber)
   - Cucumber is DIFFERENT from Selenium
   - Should be: (Selenium OR "Selenium WebDriver") AND (Cucumber OR BDD)

❌ WRONG: (AWS) AND (EC2) AND (Lambda) AND (S3)
   - All AWS services, should be together
   - Should be: (AWS OR "Amazon Web Services" OR EC2 OR Lambda OR S3)

TECHNICAL SKILLS ONLY - What to INCLUDE:

✅ Programming Languages:
   - Java, Python, JavaScript, C#, Go, Ruby, etc.

✅ Software/Platforms/Tools:
   - ServiceNow, ServiceNow SAM Pro, Appian, Documentum
   - AWS, Azure, GCP, EC2, S3, Lambda, RDS
   - Git, Jenkins, Maven, Docker, Kubernetes
   - Selenium, Cucumber, JUnit, TestNG, Cypress

✅ Frameworks/Libraries:
   - Spring, Spring Boot, React, Angular, Django, Flask
   - SAIL, BPM, REST API, microservices

✅ Databases:
   - SQL, PostgreSQL, MongoDB, Oracle, MySQL, Redshift

✅ Discovery/Monitoring Tools:
   - Workspace One, ILMT, discovery tools, monitoring tools

✅ Technical Acronyms/Abbreviations:
   - CI/CD, BDD, API, REST, J2EE, SAM Pro, DFC, xPlore

✅ Technical Processes (if tool-specific):
   - Publisher Packs (ServiceNow tool feature)
   - D2 Config, D2 Classic (Documentum features)

NON-TECHNICAL SKILLS/CONCEPTS - What to STRICTLY EXCLUDE:

❌ Business Concepts/Activities:
   - Software Asset Management (business activity, not a tool)
   - License Reconciliation (business process, not a tool)
   - Software Audit Defense (business activity)
   - Cost Optimization (business goal)
   - Vendor Negotiations (business activity)
   - Audit Renewals (business process)
   - Risk Assessments (business activity)
   - Compliance Tracking (business activity)
   - Business Objectives (business concept)
   - Enterprise Environments (generic term)
   - Licensing Strategies (business concept)
   - Software Usage Analysis (business activity)

❌ Soft Skills:
   - Communication, stakeholder management
   - Teamwork, collaboration, cross-functional teams
   - Leadership, mentorship, guidance
   - Problem-solving, analytical thinking
   - Time management, task management

❌ Generic Terms:
   - "Experience with...", "Knowledge of..."
   - "Excellent", "Strong", "Proven"
   - "End-to-end", "Optimization"
   - Executive dashboards (business reporting, not a tool)

CRITICAL RULE FOR SERVICENOW SAM:
- Include: "ServiceNow SAM Pro" (software tool)
- Include: "Publisher Packs" (specific ServiceNow feature)
- Include: "Workspace One" (discovery tool)
- Include: "ILMT" (IBM tool)
- EXCLUDE: "Software Asset Management" (business activity)
- EXCLUDE: "License Reconciliation" (business process)
- EXCLUDE: "Audit Defense" (business activity)
- EXCLUDE: "Compliance Tracking" (business activity)
- EXCLUDE: "Cost Optimization" (business goal)

EXAMPLE - ServiceNow SAM Query (CORRECT):
("ServiceNow SAM" OR "SAM Analyst" OR "ServiceNow SAM Pro")
AND ("ServiceNow SAM Pro" OR "SAM Pro")
AND ("Publisher Packs" OR "ServiceNow Publisher Packs")
AND (Microsoft OR Oracle OR IBM OR Adobe)  ← Vendor names (tools/platforms)
AND ("Workspace One" OR "VMware Workspace One")
AND (ILMT OR "IBM License Metric Tool")
AND (ServiceNow OR "Service Now")

EXAMPLE - ServiceNow SAM Query (WRONG):
❌ ("Software Asset Management" OR "License Reconciliation" OR "Audit Defense")
   - These are business activities, not tools
❌ ("Cost Optimization" OR "Compliance Tracking" OR "Risk Assessments")
   - These are business goals/processes, not technical skills
❌ ("Vendor Negotiations" OR "Stakeholder Management")
   - These are soft skills/business activities

CONSTRAINTS:
- Maximum 12 AND groups (each group can have multiple OR variations)
- First group: Role variations with OR
- Remaining groups: Each unique technical skill with its variations/synonyms
- Use AND between different/unique skills
- Use OR within same skill (abbreviations, synonyms, related terms)
- ONLY technical skills - NO soft skills whatsoever
- Use quotes for multi-word phrases

Generate ONLY the Dice Boolean query string, nothing else. No explanations, no comments.
"""

    print("Generating Dice query using ChatGPT API...")

    try:
        # Call ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-3.5-turbo" for lower cost
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter specializing in IT staffing. You analyze job descriptions and create focused, effective Boolean search queries for Dice.com. You understand how to prioritize skills and create targeted searches that balance comprehensiveness with precision. You can identify the most important role when multiple job descriptions are present and focus the query accordingly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,  # Lower temperature for more focused/consistent output
            max_tokens=800  # Reduced to encourage more concise queries
        )

        # Extract the generated query
        dice_query = response.choices[0].message.content.strip()

        # Save to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dice_query)

        print(f"\n✓ Dice query generated successfully!")
        print(f"✓ Output saved to: {output_file}")
        print(f"\nGenerated Query:\n{dice_query}")

        # Display API usage info
        print(f"\nAPI Usage:")
        print(f"  Model: {response.model}")
        print(f"  Tokens used: {response.usage.total_tokens}")

        return dice_query

    except Exception as e:
        print(f"Error calling ChatGPT API: {e}")
        return None


def extract_job_roles_from_description(job_desc_file):
    """
    Extract distinct job roles/titles from the job description file
    Returns a list of roles found
    """
    try:
        with open(job_desc_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for common role patterns
        import re
        role_patterns = [
            r'Role\s*[:\-]\s*([^\n]+)',
            r'Position\s*[:\-]\s*([^\n]+)',
            r'Job Title\s*[:\-]\s*([^\n]+)',
            r'Title\s*[:\-]\s*([^\n]+)'
        ]

        roles = []
        for pattern in role_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            roles.extend([m.strip() for m in matches])

        # Remove duplicates while preserving order
        unique_roles = []
        for role in roles:
            if role not in unique_roles and len(role) > 3:  # Filter out very short matches
                unique_roles.append(role)

        return unique_roles
    except Exception as e:
        print(f"Error extracting roles: {e}")
        return []


def main():
    """Main function to run the script"""
    import sys

    # File paths
    job_desc_file = "job_description.txt"
    output_file = "Dice_string.txt"

    # Check if file exists
    if not os.path.exists(job_desc_file):
        print(f"❌ Error: {job_desc_file} not found!")
        print("💡 Create a job_description.txt file with your job requirements")
        return

    # Try to detect multiple roles
    print("\n🔍 Analyzing job description file...")
    roles = extract_job_roles_from_description(job_desc_file)

    if len(roles) > 1:
        print(f"\n⚠️  Detected {len(roles)} different job roles:")
        for i, role in enumerate(roles, 1):
            print(f"   {i}. {role}")

        print("\n💡 TIP: For better results with multiple roles:")
        print("   • Option 1: Create a single focused query (recommended)")
        print("   • Option 2: Create separate job_description.txt files for each role")
        print("   • Option 3: Keep only the most important role in the file")

        response = input("\nContinue with a single focused query for the primary role? (Y/n): ")
        if response.lower() == 'n':
            print("Cancelled. Please update job_description.txt with a single role.")
            return

        print("\n📝 Creating focused query for the most common/primary role...")

    # Generate the query
    print("\n" + "=" * 60)
    generate_dice_query_with_chatgpt(job_desc_file, output_file)
    print("=" * 60)


if __name__ == "__main__":
    main()