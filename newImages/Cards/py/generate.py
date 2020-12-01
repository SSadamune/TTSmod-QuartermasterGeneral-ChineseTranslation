# -*- coding: utf-8 -*-
from PIL import ImageFont, ImageDraw, Image
import json
import TextWrapper
import Card


def draw_card(card):
    text_list = TextWrapper.fw_wrap(card.text, 50)

    # image 287*390
    img_pil = Image.open("../../resources/" + card.type + "_" + card.country +
                         ".png").resize((287, 390), Image.BILINEAR)
    draw = ImageDraw.Draw(img_pil)

    # font
    fontpath_bold = "C:\WINDOWS\Fonts\SourceHanSansSC-Bold.otf"
    fontpath_medium = "C:\WINDOWS\Fonts\SourceHanSansSC-Medium.otf"
    fontpath_regular = "C:\WINDOWS\Fonts\SourceHanSansSC-Regular.otf"
    font_title = ImageFont.truetype(fontpath_bold, 15)
    font_text = ImageFont.truetype(fontpath_medium, 13)
    font_meme = ImageFont.truetype(fontpath_regular, 13)

    # draw
    init_x, init_y, pad = 32, 265, 0

    title_w, title_h = draw.textsize(card.title, font=font_title)
    draw.text((init_x, init_y), card.title, font=font_title, fill=(0, 0, 0))

    current_y = init_y + title_h + pad
    for line in text_list:
        line_w, text_h = draw.textsize(line, font=font_text)
        draw.text((init_x, current_y), line, font=font_text, fill=(0, 0, 0))
        current_y += text_h + pad

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

    return img_pil


def splice_images(country):
    with open("../text/cards_" + country + ".json") as f:
        cards_images = []
        width, height = 287, 390

        # append basic cards
        basic_cards = {"BA": 5, "LB": 4, "BN": 5, "SB": 5}
        for (type, num) in basic_cards.items():
            bc_img = Image.open("../../resources/" + type + "_" + country +
                                ".png").resize((width, height), Image.BILINEAR)
            for i in range(num):
                cards_images.append(bc_img)
        
        # append special cards
        cards_data = json.load(f)
        for card_dict in cards_data:
            card = Card.Card()
            card.__dict__ = card_dict
            cards_images.append(draw_card(card))
        spliced_image = Image.new(cards_images[0].mode,
                                  (width * 10, height * 7))
        for i, image in enumerate(cards_images):
            spliced_image.paste(image,
                                box=(width * (i % 10), height * (i // 10)))

        # append card back
        back_image = Image.open("../../resources/back_" + country +
                                ".png").resize((width, height), Image.BILINEAR)
        spliced_image.paste(back_image, box=(width * 9, height * 6))

        # save file
        spliced_image.save("test_spliced_" + country + ".png")


splice_images("UK")
