from PIL import Image


class TokenCountry:
    def __init__(self, name, front_color, back_color):
        self.name = name
        self.front_color = front_color
        self.back_color = back_color


def change_color(image, color):
    img_array = image.load()
    width, height = image.size
    (r, g, b) = color
    for x in range(0, width):
        for y in range(0, height):
            rgb = img_array[x, y]
            if rgb[3] > 30:
                img_array[x, y] = (r, g, b, rgb[3])
    return image


def create_token(country, type):

    back = Image.open("../resources/token/inner.png")
    front = Image.open("../resources/token/" + type + ".png")
    token = Image.new(front.mode, (front.width, front.height))
    front = change_color(front, country.front_color)
    back = change_color(back, country.back_color)
    if country.name in ['GR', 'ITA', 'JP']:
        front = front.transpose(Image.FLIP_LEFT_RIGHT)
    token.paste(back, ((front.width - back.width) // 2,
                       (front.height - back.height) // 2), back)
    token.paste(front, (0, 0), front)

    token.save("../Tokens/" + type + "_" + country.name + ".png")


country_list = []
country_list.append(TokenCountry('US', (15, 0, 125), (225, 225, 225)))
country_list.append(TokenCountry('USSR', (0, 0, 0), (170, 0, 0)))
country_list.append(TokenCountry('UK', (0, 0, 0), (220, 180, 0)))
country_list.append(TokenCountry('CN', (50, 30, 140), (235, 54, 54)))
country_list.append(TokenCountry('FR', (235, 235, 235), (65, 65, 235)))
country_list.append(TokenCountry('GR', (150, 150, 150), (0, 0, 0)))
country_list.append(TokenCountry('ITA', (15, 15, 15), (141, 15, 193)))
country_list.append(TokenCountry('JP', (190, 0, 38), (240, 240, 240)))
for country in country_list:
    for type in ['Airforce', 'Army', 'Navy']:
        create_token(country, type)
