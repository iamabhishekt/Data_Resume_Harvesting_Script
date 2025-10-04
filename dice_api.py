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
Based on the following job description, generate a Dice.com Boolean search query string.

Job Description:
{job_description}

Instructions:
1. Extract all key skills, technologies, tools, and qualifications from the job description
2. Group similar terms together (e.g., Appian related terms, programming languages, etc.)
3. Create synonyms and variations for each term (e.g., "Appian Developer", "Appian Engineer", "Appian Architect")
4. Format the query using Boolean operators: OR within groups, AND between groups
5. Use quotes for multi-word phrases
6. Make the query comprehensive but relevant
7. For cloud/AWS terms, use variations like: (AWS OR "Amazon Web Services" OR "Cloud Integration" OR "AWS services")


Format example:
(Term1 OR "Term Variation 1" OR "Term Variation 2") AND (Term2 OR "Term2 Variation") AND (Term3 OR Term4)

Generate ONLY the Dice query string, nothing else.
"""

    print("Generating Dice query using ChatGPT API...")

    try:
        # Call ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-3.5-turbo" for lower cost
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert recruiter who creates precise Boolean search queries for job search platforms like Dice.com. You understand technical skills and can create comprehensive search strings."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
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


def main():
    """Main function to run the script"""

    # File paths
    job_desc_file = "job_description.txt"
    output_file = "Dice_string.txt"

    # Generate the query
    generate_dice_query_with_chatgpt(job_desc_file, output_file)


if __name__ == "__main__":
    main()