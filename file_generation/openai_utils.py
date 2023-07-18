import openai
import os
from openai.error import RateLimitError, APIError

# Set the OpenAI API key
openai.api_key = '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'

# Function to generate a response using OpenAI's GPT-3.5-turbo model
def generate_response(prompt):
  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
        "role": "system",
        "content": "You are a helpful assistant."
      }, {
        "role": "user",
        "content": prompt
      }],
      max_tokens=2000,
      n=1,
      stop=None,
    )
  except (RateLimitError, APIError):
    print("ran into the error: It was dealt with")
    return generate_response(prompt)
  
  return response['choices'][0]['message']['content'].strip()