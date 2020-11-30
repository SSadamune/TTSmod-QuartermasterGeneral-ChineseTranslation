# -*- coding: utf-8 -*-
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import TextWrapper
import json
import Card


def draw_card(card):
    text_list = TextWrapper.fw_wrap(card.text, 50)

    # image
    card_img = cv2.imread("test.png")

    # font
    fontpath_bold = "C:\WINDOWS\Fonts\SourceHanSansSC-Bold.otf"
    fontpath_medium = "C:\WINDOWS\Fonts\SourceHanSansSC-Medium.otf"
    fontpath_regular = "C:\WINDOWS\Fonts\SourceHanSansSC-Regular.otf"
    font_title = ImageFont.truetype(fontpath_bold, 15)
    font_text = ImageFont.truetype(fontpath_medium, 13)
    font_meme = ImageFont.truetype(fontpath_regular, 13)
    img_pil = Image.fromarray(card_img)
    draw = ImageDraw.Draw(img_pil)

    # draw
    init_x, init_y, pad = 32, 265, 0

    title_w, title_h = draw.textsize(card.title, font=font_title)
    draw.text((init_x, init_y), card.title, font=font_title, fill=0)

    current_y = init_y + title_h + pad
    for line in text_list:
        char_w, char_h = draw.textsize(line, font=font_text)
        draw.text((init_x, current_y), line, font=font_text, fill=0)
        current_y += char_h + pad

    if (card.meme):
        meme_w, meme_h = draw.textsize(card.meme, font=font_meme)
        meme_x, meme_y = init_x + title_w + 5, init_y + title_h - meme_h
        line_y = init_y + 3 + meme_h / 2
        draw.text((meme_x, meme_y),
                  card.meme,
                  font=font_meme,
                  fill=(127, 127, 127))
        draw.line((meme_x, line_y, meme_x + meme_w, line_y),
                  fill=(127, 127, 127))

    card_img = np.array(img_pil)

    cv2.imshow("add_text", card_img)
    cv2.waitKey()
    cv2.imwrite("add_text.jpg", card_img)


# text
with open("test.json") as f:
    cards_data = json.load(f)
    for card_dict in cards_data:
        card = Card.Card()
        card.__dict__ = card_dict
        draw_card(card)
