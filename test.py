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

path = 'result_capture.jpg'
titles = pygetwindow.getAllTitles()

window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
left, top = window.topleft
right, bottom = window.bottomright
a = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
a.show()
