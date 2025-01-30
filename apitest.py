from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://136.53.88.221:8080/v1", api_key="lm-studio")


def main():
    while True:
        # Ask the user for a prompt
        user_prompt = input("Please enter your prompt (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if user_prompt.lower() == 'exit':
            print("Goodbye!")
            break

        # Send the prompt to the model and get the response
        try:
            completion = client.chat.completions.create(
                model="Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2-GGUF",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            # Print the model's response
            print(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
