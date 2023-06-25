import discord
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.environ['SECRET_KEY']
chat_history = ''


class MyClient(discord.Client):

  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    print(f'Message from {message.author}: {message.content}')
    global chat_history
    chat_history += f'{message.author}: {message.content}'
    if self.user != message.author:
      if self.user in message.mentions:
        channel = message.channel
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=chat_history +
                                            "\nHussamGPT:",
                                            temperature=1,
                                            max_tokens=256,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0)
        message_to_send = response.choices[0].text
        await channel.send(message_to_send)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)