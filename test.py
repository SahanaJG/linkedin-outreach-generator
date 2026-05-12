import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyAISp0aeqaOpH6A63oqN5Vdbq7OplrKFRU")

# List all available models
models = genai.list_models()

for model in models:
    print(model.name)
