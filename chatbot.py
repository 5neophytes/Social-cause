import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the OpenAI API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Ensure the API key is set
if not api_key:
    raise ValueError("API key is missing. Please ensure it's set in the .env file.")

# Initialize the OpenAI client
openai.api_key = api_key

# Function to process the user query and return the model's response
def solve_user_query(query):
    try:
        # Prepare the prompt for the model
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]

        # Call the OpenAI API with the provided query
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" if needed
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        # Extract the model's response
        answer = response['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main function to take user input and provide the solution
def main():
    print("Welcome! Ask me anything, and I'll do my best to provide a solution.")

    finance_keywords = ["finance", "money", "stocks", "loan", "investment", "savings", "interest", "credit", "budget", "economy"]
    
    while True:
        # Capture the user query
        user_query = input("Enter your question (or type 'exit' to quit): ")

        # Exit condition
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        if any(keyword in user_query.lower() for keyword in finance_keywords):
            # Solve the user query using the OpenAI model
            response = solve_user_query(user_query)
            print(f"\nResponse: {response}\n")
        else:
            print("I'm sorry, i can only answer finance related questions.")
            break

if __name__ == "__main__":
    main()
