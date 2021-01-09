from PIL import Image


def set_template(country, type):
    is_base = type in ['BA', 'BN', 'LB', 'SB', 'AP']

    card_width, card_height = 384, 512
    card = Image.open("../resources/template/background_" + country + ".png")
    type_image = Image.open("../resources/template/pic/" + country + "_" +
                            type + ".png").resize((384, 314), Image.BILINEAR)
    card.paste(type_image, (0, 99))
    text = Image.open("../resources/template/" + type + "_text.png")
    text_x = (card_width - text.width) // 2
    text_y = 42 if is_base else 148 - text.height
    card.paste(text, (text_x, text_y), text)
    if not is_base:
        card.paste(Image.open("../resources/template/textblock.png"),
                   ((card_width - 364) // 2, card_height - 172 - 10))
    card.save("../Cards/template/" + type + "_" + country + ".png")


def set_ah_template(country1, country2, type):
    card_width, card_height = 384, 512
    card = Image.open("../resources/template/background_" + country2 + ".png")
    type_image = Image.open("../resources/template/pic/" + country1 + "_" +
                            country2 + ".png").resize((384, 314),
                                                      Image.BILINEAR)
    card.paste(type_image, (0, 99))
    text = Image.open("../resources/template/" + type + "_text.png")
    text_x = (card_width - text.width) // 2
    text_y = 148 - text.height
    card.paste(text, (text_x, text_y), text)
    card.paste(Image.open("../resources/template/textblock.png"),
               ((card_width - 364) // 2, card_height - 172 - 10))
    card.save("../Cards/template/" + type + "_" + country2 + "_" + country1 +
              ".png")


country_list = ['US', 'USSR', 'UK', 'GR', 'ITA', 'JP']
type_list = [
    'BA', 'BN', 'LB', 'SB', 'AP', 'Stat', 'Event', 'EcoWar', 'Resp', 'Blst'
]

# for country in country_list:
#     for type in type_list:
#         set_template(country, type)

# for type in ['Stat', 'Event', 'Blst']:
#     set_ah_template('CN', 'USSR', type)
# for type in ['Stat', 'Event', 'EcoWar', 'Blst']:
#     set_ah_template('CN', 'US', type)
# for type in ['Stat', 'Event', 'Resp', 'Blst']:
#     set_ah_template('FR', 'UK', type)

set_template('ITA', 'Blst')

