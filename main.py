import discord
from discord.ext import commands
from discord import app_commands

from paddleocr import PaddleOCR


import pygetwindow
import pyautogui
from PIL import Image
import numpy as np
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=True, det_model_dir="en_number_mobile_v2.0_rec_infer.tar")
# img_path = 'test-image-2.jpg'

window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
left, top = window.topleft
right, bottom = window.bottomright
window_width = right - left
window_height = bottom - top

crop_left = int(0.066 * window_width)     
crop_top = int(0.473 * window_height)     
crop_right = int(0.133 * window_width)    
crop_bottom = int(0.022 * window_height)  
crop_text = int(0.1731*window_width)

# Tọa độ tương đối cho vị trí nhấp chuột, ví dụ ở giữa cửa sổ
# click_x = left + int(window_width * 0.9087)   # 96.4
# click_y = top + int(window_height * 0.9262)   # 50% của chiều cao cửa sổ



system_template = "This is my data {data}:"
prmt_template="""
i want you to correct the spelling and calculate the percent hp boss, just return like the format below, not any more word from you, not "Here is the corrected and formatted data:"

Lv.105 Founder Elphaba (305,330,795/400,000,000) 75% 
Lv.105 Goblin Chief (55,413,567/400,000,000) 12% 
Lv.105 Nine-tailed Fox Garam (93,698,474/400,000,000) 25% 
Lv.105 Snowman General Gast (250,902,339/ 400,000,000) 55%

"""
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', prmt_template)
])

# 2. Create model
model = ChatGroq(model="llama3-8b-8192", api_key='')

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try: 
            guild = discord.Object(id=1134890205460041858)
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

GUILD_ID = discord.Object(id=1134890205460041858)


@client.tree.command(name="hello", description="Says hello", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')

@client.tree.command(name="bosscheck", description="Kiem tra dmg boss", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    # Thực hiện sự kiện nhấp chuột
    # pyautogui.click(click_x, click_y)
    # # Đợi một chút để cửa sổ phản ứng
    # time.sleep(1) 
    window = pyautogui.screenshot(region=(left, top, window_width, window_height))
    window = window.crop((crop_left, crop_top, window_width - crop_right, window_height - crop_bottom))
    window = np.array(window)
    height, width, _ = window.shape
    window[height-crop_text:height, width-crop_text:width] = [255, 255, 255]
    result = ocr.ocr(window, cls=False)
    text_output = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text_output += line[1][0] + "\n"
    final = chain.invoke(text_output)
    await interaction.response.send_message(final)



client.run("")



        