# -*- coding: utf-8 -*-
from PIL import ImageFont, ImageDraw, Image
import json
import TextWrapper
import Card


def draw_card(card):
    text_list = TextWrapper.fw_wrap(card.text, 49)

    # image 287*390
    img_pil = Image.open("../../resources/" + card.type + "_" + card.country +
                         ".png").resize((287, 390), Image.BILINEAR)
    draw = ImageDraw.Draw(img_pil)

    # font
    fontpath_bold = "../../resources/SourceHanMonoSC-Bold.otf"
    fontpath_medium = "../../resources/SourceHanMonoSC-Medium.otf"
    font_title = ImageFont.truetype(fontpath_bold, 15)
    font_text = ImageFont.truetype(fontpath_medium, 13)
    font_meme = ImageFont.truetype(fontpath_medium, 14)

    # draw
    init_x, init_y, pad = 36, 265, 0

    title_w, title_h = draw.textsize(card.title, font=font_title)
    draw.text((init_x, init_y), card.title, font=font_title, fill=(0, 0, 0))

    current_y = init_y + title_h + pad + 0
    for line in text_list:
        line_w, text_h = draw.textsize(line, font=font_text)
        draw.text((init_x, current_y), line, font=font_text, fill=(0, 0, 0))
        current_y += text_h + pad

    if (card.meme):
        meme_w, meme_h = draw.textsize(card.meme, font=font_meme)
        meme_x, meme_y = init_x + title_w + 10, init_y + title_h - meme_h
        draw.text((meme_x, meme_y),
                  card.meme,
                  font=font_meme,
                  fill=(127, 127, 127))
        line_y = init_y + 3 + meme_h / 2
        draw.line((meme_x, line_y, meme_x + meme_w, line_y),
                  fill=(127, 127, 127),
                  width=2)

    return img_pil


def splice_images(country, basic_cards):
    with open("../text/cards_" + country + ".json") as f:
        cards_base = []
        width, height = 287, 390

        # append basic cards
        for (type, num) in basic_cards.items():
            bc_img = Image.open("../../resources/" + type + "_" + country +
                                ".png").resize((width, height), Image.BILINEAR)
            for i in range(num):
                cards_base.append(bc_img)

        # append special cards
        cards_data = json.load(f)
        for card_dict in cards_data:
            card = Card.Card()
            card.__dict__ = card_dict

            if card.expansion == "base":
                cards_base.append(draw_card(card))
            elif card.expansion == "am/ah":
                cards_base.append(draw_card(card))
            elif card.expansion == "base-substituted":
                pass

        spliced_base = Image.new(cards_base[0].mode, (width * 10, height * 7))
        for i, image in enumerate(cards_base):
            spliced_base.paste(image,
                               box=(width * (i % 10), height * (i // 10)))

        # append card back
        back_image = Image.open("../../resources/back_" + country +
                                ".png").resize((width, height), Image.BILINEAR)
        spliced_base.paste(back_image, box=(width * 9, height * 6))

        # save file
        spliced_base.save("../QMG_cards_" + country + "_Ex.png")


def generate_ver_base():
    splice_images("UK", {"BA": 5, "LB": 4, "BN": 5, "SB": 5})
    splice_images("US", {"BA": 5, "LB": 4, "BN": 5, "SB": 4})
    splice_images("USSR", {"BA": 8, "LB": 6, "BN": 1, "SB": 2})
    splice_images("GR", {"BA": 6, "LB": 7, "BN": 2, "SB": 2})
    splice_images("ITA", {"BA": 4, "LB": 4, "BN": 3, "SB": 2})
    splice_images("JP", {"BA": 4, "LB": 3, "BN": 6, "SB": 4})


def generate_ver_amah():
    splice_images("UK", {"BA": 5, "LB": 4, "BN": 6, "SB": 5, "AP": 4})
    splice_images("US", {"BA": 5, "LB": 4, "BN": 5, "SB": 4, "AP": 6})
    splice_images("USSR", {"BA": 9, "LB": 7, "BN": 1, "SB": 2, "AP": 3})
    splice_images("GR", {"BA": 6, "LB": 8, "BN": 2, "SB": 2, "AP": 5})
    splice_images("ITA", {"BA": 4, "LB": 5, "BN": 4, "SB": 2, "AP": 3})
    splice_images("JP", {"BA": 4, "LB": 3, "BN": 7, "SB": 4, "AP": 5})


splice_images("USSR", {"BA": 9, "LB": 7, "BN": 1, "SB": 2, "AP": 3})
