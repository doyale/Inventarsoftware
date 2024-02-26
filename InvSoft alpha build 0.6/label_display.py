from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os


#placeholder variables

def chemLabel(label_title):
    label_title = str(label_title)
    GHS_dim = 140
    GHS_left_spacer = 0
    title_font = ImageFont.truetype("arial.ttf", 48)
    title_font_medium = ImageFont.truetype("arial.ttf", 32)
    title_font_long = ImageFont.truetype("arial.ttf", 24)
    haz_prec_font = ImageFont.truetype("arial.ttf", 16)


    #variables and image init
    absolute_path = os.path.dirname(__file__)
    GHS_pictograms = []
    background = Image.open(absolute_path + "/Label/default_bg.png") #load the background

    #GHS section
    GHS_image_names = ["GHS01.png", "GHS02.png", "GHS03.png", "GHS04.png", "GHS05.png", "GHS06.png", "GHS07.png", "GHS08.png", "GHS09.png"]
    GHS_position_iteration = [(0 + GHS_left_spacer, 0), (GHS_dim/2 + GHS_left_spacer, GHS_dim/2), (0 + GHS_left_spacer, GHS_dim),
                            (GHS_dim/2 + GHS_left_spacer, GHS_dim*3/2), (0 + GHS_left_spacer, GHS_dim*2), (GHS_dim/2 + GHS_left_spacer, GHS_dim*5/2),
                            (0 + GHS_left_spacer, GHS_dim*3), (GHS_dim/2 + GHS_left_spacer, GHS_dim*7/2), (0 + GHS_left_spacer, GHS_dim*4)]
    GHS_position_iteration = list(tuple(map(int, tup)) for tup in GHS_position_iteration) #convert all floats to int
    for image in GHS_image_names: #load all GHS pictograms into memory
        GHS_pictograms.append(Image.open(f"{absolute_path}/GHS/{image}").resize((GHS_dim, GHS_dim)))
    for index, pictogram in enumerate(GHS_pictograms):
        if index > 4:
            break
        background.paste(pictogram, GHS_position_iteration[index], pictogram)

    # Text section
    label_draw = ImageDraw.Draw(background)
    if len(label_title) <= 25:
        label_draw.text((GHS_dim + GHS_left_spacer + 5, 0), label_title, (0, 0, 0), font=title_font)
    elif len(label_title) <= 35:
            label_draw.text((GHS_dim + GHS_left_spacer + 5, 0), label_title, (0, 0, 0), font=title_font_medium)
    else:
        label_draw.text((GHS_dim + GHS_left_spacer + 5, 0), label_title[:46], (0, 0, 0), font=title_font_long)
        label_draw.text((GHS_dim + GHS_left_spacer + 5, 28), label_title[46:], (0, 0, 0), font=title_font_long)
    return background

if __name__ == "__main__":
    chemLabel("Palladium(II)- chloride").show()

#background.convert("RGB")
#background.save("test.jpg")
#background.show()