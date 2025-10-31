from openai import OpenAI

client = OpenAI()

response = client.responses.create(
  model="gpt-5-mini",
  input="Tell me a three sentence bedtime story about a unicorn."
)

print(response)


# TODO: This was for if a human would be running, not an agent (and you need to exist the docker container)