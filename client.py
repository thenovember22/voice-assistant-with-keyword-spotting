import google.generativeai as genai
# Configure Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
# Load the model (Recommended free model)
model = genai.GenerativeModel("gemini-1.5-flash")
# System + User prompt merged (Gemini does not use roles the same way as OpenAI)
system_prompt = "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."
user_prompt   = "what is coding"
# Send the request
response = model.generate_content(
    system_prompt + "\nUser: " + user_prompt
)
# Print the response
print(response.text)
