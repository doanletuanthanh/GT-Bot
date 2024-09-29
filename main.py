import discord
from discord.ext import commands
from discord import app_commands

from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=True, det_model_dir="en_number_mobile_v2.0_rec_infer.tar")
img_path = 'test-image-2.jpg'

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try: 
            guild = discord.Object(id=913806560088711188)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} command(s) to guild {guild.id}.')
        except Exception as e:
            print(f"Error syncing commands: {e}")


    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('dit me'):
            await message.channel.send(f'Dit me {message.author}!')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('React cc')
    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

GUILD_ID = discord.Object(id=913806560088711188)


@client.tree.command(name="hello", description="Says hello", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')

@client.tree.command(name="bosscheck", description="Kiem tra dmg boss", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    result = ocr.ocr(img_path, cls=False)
    text_output = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text_output += line[1][0] + "\n"

    await interaction.response.send_message(text_output)



client.run()



        