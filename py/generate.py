# -*- coding: utf-8 -*-
from PIL import ImageFont, ImageDraw, Image
import json
import TextWrapper
import os
import shutil
import traceback

template = "../Cards/template/"

class Card:
    def __init__(self, title="", country="", type="", dlc="", text="", sub_text="", substituted=False, cn_fr="", meme=""):
        self.title = title
        self.country = country
        self.type = type
        self.dlc = dlc
        self.text = text
        self.sub_text = sub_text
        self.substituted = substituted
        self.cn_fr = cn_fr
        self.meme = meme

class Country:
    name = ""
    base_basic_cards = {}
    ex_basic_cards = {}

    def __init__(self, name, base_basic_cards, ex_basic_cards):
        self.name = name
        self.base_basic_cards = base_basic_cards
        self.ex_basic_cards = ex_basic_cards
    
def draw_card(card, scale=2):
    text_list = TextWrapper.fw_wrap(card.text, 35)
    original_width, original_height = 384, 512
    new_width = original_width * scale
    new_height = original_height * scale

    try:
        if card.cn_fr:
            img_path = template + card.type + "_" + card.country + "_" + card.cn_fr + ".png"
        else:
            img_path = template + card.type + "_" + card.country + ".png"

        img_pil = Image.open(img_path).resize((new_width, new_height), Image.BILINEAR)
    except FileNotFoundError:
        print(f"Error: File not found for card type: {card.type}, country: {card.country}")
        return None

    draw = ImageDraw.Draw(img_pil)

    fontpath_bold = "../resources/msyhbd.ttc"
    fontpath_medium = "../resources/msyh.ttc"
    font_title = ImageFont.truetype(fontpath_bold, 21 * scale)
    font_text = ImageFont.truetype(fontpath_medium, 19 * scale)
    font_sub = ImageFont.truetype(fontpath_medium, 19 * scale)

    init_x, init_y = 30 * scale, 340 * scale
    end_x, end_y, pad = 359 * scale, 487 * scale, 5 * scale

    title_bbox = draw.textbbox((0, 0), card.title, font=font_title)
    title_w, title_h = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    draw.text((init_x, init_y), card.title, font=font_title, fill=(0, 0, 0))

    current_y = init_y + title_h + pad + 2 * scale
    for line in text_list:
        line_bbox = draw.textbbox((0, 0), line, font=font_text)
        text_w, text_h = line_bbox[2] - line_bbox[0], line_bbox[3] - line_bbox[1]
        draw.text((init_x, current_y), line, font=font_text, fill=(0, 0, 0))
        current_y += text_h + pad

    if card.sub_text:
        sub_bbox = draw.textbbox((0, 0), card.sub_text, font=font_sub)
        sub_w, sub_h = sub_bbox[2] - sub_bbox[0], sub_bbox[3] - sub_bbox[1]
        sub_x, sub_y = end_x - sub_w, end_y - sub_h
        draw.text((sub_x, sub_y), card.sub_text, font=font_sub, fill=(127, 127, 127))

    return img_pil


def splice_list(cards_list, list_name, country):
    mode, width, height = cards_list[0].mode, cards_list[0].width, cards_list[
        0].height
    spliced_base = Image.new(mode, (width * 10, height * 7))
    for i, image in enumerate(cards_list):
        spliced_base.paste(image, box=(width * (i % 10), height * (i // 10)))

    # append card back
    back_image = Image.open("../resources/QMG_back_" + country +
                            ".png").resize((width, height), Image.BILINEAR)
    spliced_base.paste(back_image, box=(width * 9, height * 6))

    # save file
    spliced_base.save("../Cards/QMG_cards_" + country + "_" + list_name +
                      ".png")

    return spliced_base


def generate_sprite(country):
    with open("../text/cards_" + country.name + ".json") as cards_info:
        cards_base = []
        cards_ex = []
        width, height = 384, 512

        # append basic cards
        for (type, num) in country.base_basic_cards.items():
            bc_img = Image.open(template + type + "_" + country.name +
                                ".png").resize((width, height), Image.BILINEAR)
            for _ in range(num):
                cards_base.append(bc_img)
        for (type, num) in country.ex_basic_cards.items():
            bc_img = Image.open(template + type + "_" + country.name +
                                ".png").resize((width, height), Image.BILINEAR)
            for _ in range(num):
                cards_ex.append(bc_img)

        # append special cards
        cards_data = json.load(cards_info)
        for card_dict in cards_data:
            card = Card()
            card.__dict__ = card_dict

            if not card.substituted:
                if card.dlc == "base":
                    cards_base.append(draw_card(card))
                elif card.dlc == "am/ah":
                    cards_ex.append(draw_card(card))

        splice_list(cards_base, "base", country.name)
        splice_list(cards_ex, "amah", country.name)

def export_individual_cards(country):
    base_output_dir = "../Cards/Individual/"
    country_output_dir = os.path.join(base_output_dir, country.name)
    basic_output_dir = os.path.join(country_output_dir, "basic")
    special_output_dir = os.path.join(country_output_dir, "special")

    if os.path.exists(country_output_dir):
        shutil.rmtree(country_output_dir)
    os.makedirs(basic_output_dir)
    os.makedirs(special_output_dir)
    
    scale = 2

    total_basic_cards = {}
    for card_type, num in country.base_basic_cards.items():
        total_basic_cards[card_type] = num
    for card_type, num in country.ex_basic_cards.items():
        if card_type in total_basic_cards:
            total_basic_cards[card_type] += num
        else:
            total_basic_cards[card_type] = num

    for card_type, total_num in total_basic_cards.items():
        card_image = draw_card(Card(type=card_type, country=country.name), scale=scale)
        if card_image:
            output_path = os.path.join(basic_output_dir, f"[{total_num}]{card_type}.png")
            card_image.save(output_path, format="PNG")
    
    with open(f"../text/cards_{country.name}.json", encoding='utf-8') as cards_info:
        cards_data = json.load(cards_info)
        for card_dict in cards_data:
            card = Card(**card_dict)
            if not getattr(card, 'substituted', False):
                try:
                    card_image = draw_card(card, scale=scale)
                    if card_image:
                        output_path = os.path.join(special_output_dir, f"{card.title}.png")
                        card_image.save(output_path, format="PNG")
                except Exception as e:
                    print(f"Error processing card: {card.title}")
                    print(f"Error details: {str(e)}")
                    traceback.print_exc()
                                               
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
# all_countries = [uk]

# main
for country in all_countries:
    # generate_sprite(country)
    export_individual_cards(country)

