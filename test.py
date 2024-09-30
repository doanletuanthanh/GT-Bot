# from paddleocr import PaddleOCR
# # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# # You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# # to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=True, det_model_dir="en_number_mobile_v2.0_rec_infer.tar") # need to run only once to download and load model into memory
# img_path = 'test-image.jpg'
# result = ocr.ocr(img_path, cls=False)
# for idx in range(len(result)):
#     res = result[idx]
#     for line in res:
#         print(line)


import pygetwindow
import pyautogui
from PIL import Image
import numpy as np

path = 'result_capture.jpg'
titles = pygetwindow.getAllTitles()

window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
left, top = window.topleft
right, bottom = window.bottomright
a = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

a = a.crop((50, 220, right - left - 100, bottom - top - 10))
a = np.array(a)
height, width, _ = a.shape
a[height-130:height, width-130:width] = [255, 255, 255]
a = Image.fromarray(a)
a.show()
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_groq import ChatGroq

# system_template = "This is my data {data}:"
# prmt_template="""
# i want you to correct the spelling and calculate the percent hp boss, just return like the format below, not any more word from you, not "Here is the corrected and formatted data:"

# Lv.105 Founder Elphaba (305,330,795/400,000,000) 75% 
# Lv.105 Goblin Chief (55,413,567/400,000,000) 12% 
# Lv.105 Nine-tailed Fox Garam (93,698,474/400,000,000) 25% 
# Lv.105 Snowman General Gast (250,902,339/ 400,000,000) 55%

# """
# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', system_template),
#     ('user', prmt_template)
# ])

# # 2. Create model
# model = ChatGroq(model="llama3-8b-8192", api_key='')

# # 3. Create parser
# parser = StrOutputParser()

# # 4. Create chain
# chain = prompt_template | model | parser

# print(chain.invoke("""100.000.000/400,000,000 
# Ly.105 FounderFlphaba
# 20.000000/400,000,000 
# Lv.105 Goblin Chief
# 90.000.000/400,000,000 
# Ly.105 Nine-talled Fox Garam
# 100.000.000/ 400,000,000 
# Lv.105Snowman GeneralGast"""))
