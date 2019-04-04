import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

TEXT_HEIGHT = 19
TEXT_WIDTH = 300
TEXT_SCALE = 3
TEXT_FONTSIZE = 60
TEXT_FONTFACE = "fonts/Calibri.ttf"
TEXT_FONTFACE_HEADDING = "fonts/Calibri.ttf"
# TEXT_COLOUR = (32, 102, 148)
TEXT_COLOUR = (255,255,255)
TEXT_COLOUR_HEADDING = (240, 80, 0)
TEXT_BACKGROUND = (0, 0, 0, 0)


def textimage(txt, format = 'RGBA'):
	image = PIL.Image.new(format, (TEXT_WIDTH * TEXT_SCALE, TEXT_HEIGHT * TEXT_SCALE), TEXT_BACKGROUND)
	draw = PIL.ImageDraw.Draw(image)
	font = PIL.ImageFont.truetype(TEXT_FONTFACE, TEXT_FONTSIZE)
	draw.text((2, 0), txt, TEXT_COLOUR, font = font)
	return image.resize((TEXT_WIDTH, TEXT_HEIGHT), PIL.Image.ANTIALIAS)



textimage("test123").save('testtext.png')
