import openai
import os
import json
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
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to store the query and response, overwriting the JSON file
def store_response_in_json(user_query, model_response, filename="responses.json"):
    # Structure the data as a dictionary
    data = {
        "query": user_query,
        "response": model_response
    }

    # Overwrite the file with the new data (mode 'w' ensures the file is overwritten)
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Main function to take user input and provide the solution
def main():
    print("Welcome! I can assist you with finance-related questions.")
    
    finance_keywords = ["finance", "money", "stocks", "loan", "investment", "savings", "interest", "credit", "budget", "economy"]
    
    user_query = input("Enter your question: ")
        

    if any(keyword in user_query.lower() for keyword in finance_keywords):
        response = solve_user_query(user_query)
        print(f"\nResponse: {response}\n")
        # Overwrite the query and response in the JSON file
        store_response_in_json(user_query, response)
    else:
        print("Sorry, I cannot help you answer this question.\n")

if __name__ == "__main__":
    main()
