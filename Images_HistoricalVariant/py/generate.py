# -*- coding: utf-8 -*-
from PIL import ImageFont, ImageDraw, Image
import json
import TextWrapper


class Card:
    title = ""
    country = ""
    type = ""
    dlc = ""
    text = ""
    sub_text = ""
    substituted = ""


class Country:
    name = ""
    base_basic_cards = {}
    ex_basic_cards = {}

    def __init__(self, name, base_basic_cards, ex_basic_cards):
        self.name = name
        self.base_basic_cards = base_basic_cards
        self.ex_basic_cards = ex_basic_cards


def draw_card(card):
    text_list = TextWrapper.fw_wrap(card.text, 51)

    img_pil = Image.open("../Cards/template/" + card.type + "_" +
                         card.country + ".png").resize((384, 512),
                                                       Image.BILINEAR)
    draw = ImageDraw.Draw(img_pil)

    # font
    fontpath_bold = "../resources/SourceHanMonoSC-Bold.otf"
    fontpath_medium = "../resources/SourceHanMonoSC-Medium.otf"
    font_title = ImageFont.truetype(fontpath_bold, 21)
    font_text = ImageFont.truetype(fontpath_medium, 19)
    font_sub_text = ImageFont.truetype(fontpath_medium, 19)

    # draw
    init_x, init_y, end_x, end_y, pad = 30, 340, 355, 485, 0

    title_w, title_h = draw.textsize(card.title, font=font_title)
    draw.text((init_x, init_y), card.title, font=font_title, fill=(0, 0, 0))

    current_y = init_y + title_h + pad + 2
    for line in text_list:
        text_w, text_h = draw.textsize(line, font=font_text)
        draw.text((init_x, current_y), line, font=font_text, fill=(0, 0, 0))
        current_y += text_h + pad

    if (card.sub_text):
        sub_text_w, sub_text_h = draw.textsize(card.sub_text, font=font_sub_text)
        sub_text_x, sub_text_y = end_x - sub_text_w, end_y - sub_text_h
        draw.text((sub_text_x, sub_text_y),
                  card.sub_text,
                  font=font_sub_text,
                  fill=(127, 127, 127))

    return img_pil


def splice_list(cards_list, list_name, country):
    mode, width, height = cards_list[0].mode, cards_list[0].width, cards_list[
        0].height
    spliced_base = Image.new(mode, (width * 10, height * 7))
    for i, image in enumerate(cards_list):
        spliced_base.paste(image, box=(width * (i % 10), height * (i // 10)))

    # append card back
    back_image = Image.open("../resources/back_" + country + ".png").resize(
        (width, height), Image.BILINEAR)
    spliced_base.paste(back_image, box=(width * 9, height * 6))

    # save file
    spliced_base.save("../Cards/QMG_cards_" + country + "_" + list_name +
                      ".png")

    return spliced_base


def generate(country):
    with open("../text/cards_" + country.name + ".json") as cards_info:
        cards_base = []
        cards_ex = []
        width, height = 384, 512

        # append basic cards
        for (type, num) in country.base_basic_cards.items():
            bc_img = Image.open("../Cards/template/" + type + "_" +
                                country.name + ".png").resize((width, height),
                                                              Image.BILINEAR)
            for i in range(num):
                cards_base.append(bc_img)
        for (type, num) in country.ex_basic_cards.items():
            bc_img = Image.open("../Cards/template/" + type + "_" +
                                country.name + ".png").resize((width, height),
                                                              Image.BILINEAR)
            for i in range(num):
                cards_ex.append(bc_img)

        # append special cards
        cards_data = json.load(cards_info)
        for card_dict in cards_data:
            card = Card()
            card.__dict__ = card_dict

            if card.substituted == "":
                if card.dlc == "base":
                    cards_base.append(draw_card(card))
                elif card.dlc == "am/ah":
                    cards_ex.append(draw_card(card))
                elif card.dlc == "base-substituted":
                    pass

        splice_list(cards_base, "base", country.name)
        splice_list(cards_ex, "amah", country.name)


uk = Country("UK", {"BA": 5, "LB": 4, "BN": 5, "SB": 5}, {"BN": 1, "AP": 4})
us = Country("US", {"BA": 5, "LB": 4, "BN": 5, "SB": 4}, {"AP": 6})
ussr = Country("USSR", {
    "BA": 8,
    "LB": 6,
    "BN": 1,
    "SB": 2
}, {
    "BA": 1,
    "LB": 1,
    "AP": 3
})
gr = Country("GR", {"BA": 6, "LB": 7, "BN": 2, "SB": 2}, {"LB": 1, "AP": 5})
ita = Country("ITA", {
    "BA": 4,
    "LB": 4,
    "BN": 3,
    "SB": 2
}, {
    "LB": 1,
    "BN": 1,
    "AP": 3
})
jp = Country("JP", {"BA": 4, "LB": 3, "BN": 6, "SB": 4}, {"BN": 1, "AP": 5})
all_countries = [uk, us, ussr, gr, ita, jp]

# generate(us)
for c in all_countries:
    generate(c)
