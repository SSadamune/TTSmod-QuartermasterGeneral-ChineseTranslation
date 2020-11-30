# -*- coding: utf-8 -*-
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import TextWrapper

# image
card_img = cv2.imread("test.png")

# font
fontpath_heavy = "C:\WINDOWS\Fonts\SourceHanSansSC-Heavy.otf"
fontpath_bold = "C:\WINDOWS\Fonts\SourceHanSansSC-Bold.otf"
fontpath_medium = "C:\WINDOWS\Fonts\SourceHanSansSC-Medium.otf"
fontpath_regular = "C:\WINDOWS\Fonts\SourceHanSansSC-Regular.otf"
font_title = ImageFont.truetype(fontpath_bold, 15)
font_meme = ImageFont.truetype(fontpath_regular, 15)
font_text = ImageFont.truetype(fontpath_medium, 13)
img_pil = Image.fromarray(card_img)
draw = ImageDraw.Draw(img_pil)

# text
card_title = "自由法国"
text1line = "每回合限一次，当你发起海战时发动：你可弃置 2 张手牌，在发起海战的海域或另一个海域发起海战。"
card_text = TextWrapper.fw_wrap(text1line, 51)
card_meme = "戴高乐领导法国"

# draw
init_x, init_y, pad = 32, 265, 0
title_w, title_h = draw.textsize(card_title, font=font_title)
draw.text((init_x, init_y), card_title, font=font_title, fill=0)
current_y = init_y + title_h + pad
for line in card_text:
    char_w, char_h = draw.textsize(line, font=font_text)
    draw.text((init_x, current_y), line, font=font_text, fill=0)
    current_y += char_h + pad
if (card_meme):
    meme_w, meme_h = draw.textsize(card_meme, font=font_meme)
    meme_x, line_y = init_x + title_w + 10, init_y + 2 + meme_h / 2
    draw.text((meme_x, init_y), card_meme, font=font_meme, fill=(127, 127, 127))
    draw.line((meme_x, line_y, meme_x + meme_w, line_y), fill=(127, 127, 127))
card_img = np.array(img_pil)

cv2.imshow("add_text", card_img)
cv2.waitKey()
cv2.imwrite("add_text.jpg", card_img)
