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

TASK:
Analyze the above text and create ONE focused Dice.com Boolean search query that:

1. Identifies the primary/most common role (e.g., "Java Developer", "Python Developer", "SDET", "Appian Developer")
2. Extracts ONLY the TOP 8-12 most important TECHNICAL skills for that role
3. Groups similar technical terms together with OR operators
4. Uses AND operators between different skill groups
5. Includes variations and synonyms for each technical term
6. Uses quotes for multi-word phrases

TECHNICAL SKILLS TO INCLUDE:
- Programming languages (Java, Python, JavaScript, C#, etc.)
- Frameworks and libraries (Spring, React, Angular, etc.)
- Platforms and tools (Appian, ServiceNow, AWS, Azure, etc.)
- Databases (SQL, PostgreSQL, MongoDB, Oracle, etc.)
- Development tools (Git, Jenkins, Maven, IntelliJ, etc.)
- Specific technologies (REST APIs, microservices, Docker, Kubernetes, etc.)
- Domain-specific technical skills (BPM, ETL, SAIL, RPA, etc.)

SOFT SKILLS TO STRICTLY EXCLUDE:
- Problem-solving, analytical thinking, critical thinking
- Communication, verbal/written communication, stakeholder management
- Teamwork, collaboration, cross-functional teams
- Customer focus, customer-oriented, end-user needs
- Continuous learning, adaptability, self-management
- Leadership, mentorship, guidance
- Time management, task management, prioritization
- Any other behavioral or interpersonal skills

QUERY STRUCTURE:
- Start with role-specific terms: (RoleTitle OR "Role Variation 1" OR "Role Variation 2")
- Follow with core TECHNICAL platform/tool (most important first)
- Add specific technical skills and technologies only
- Include programming languages and frameworks
- Add relevant technical tools

FORMAT EXAMPLE:
("Appian Developer" OR "Appian Architect" OR "Appian Engineer") AND (Appian OR "Appian platform" OR "Appian low-code") AND (SAIL OR "Appian SAIL" OR "Appian UI") AND (BPM OR "Business Process Management" OR "process modeling") AND (RPA OR "Appian RPA" OR automation) AND (Java OR JavaScript OR J2EE) AND (REST OR "REST API" OR "web services") AND (SQL OR database OR "data management")

CONSTRAINTS:
- Maximum 12 skill groups (each group can have multiple OR variations)
- ONLY technical skills - NO soft skills whatsoever
- Focus on verifiable, searchable technical competencies
- Prioritize technical skills mentioned multiple times across descriptions
- If a skill is behavioral/interpersonal, DO NOT include it

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