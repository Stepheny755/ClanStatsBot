import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import string

from random import randint
from util import Util

TEXT_HEIGHT = 60
TEXT_WIDTH = 300
TEXT_SCALE = 4
TEXT_FONTSIZE = 60
TEXT_FONTFACE = "fonts/Roboto-Regular.ttf"
TEXT_FONTFACE_HEADDING = "fonts/Roboto-Regular.ttf"
# TEXT_COLOUR = (32, 102, 148)
TEXT_COLOUR_HEADDING = (240, 80, 0)
TEXT_BACKGROUND = (0, 0, 0, 0)
LINE_SPACING = 5

WHT = (255,255,255)
RED = (255,0,0)
GRN = (0,255,0)

gencolor = lambda : (randint(50, 255), randint(50, 255), randint(50,255))

class Front():

    printable = " ".join(string.printable)
    gcl = None
    wcl = None
    rcl = None


    def __init__(self):
        A = self.printable

        image = PIL.Image.new("RGB", (1200,20), (0,0,0))
        draw = PIL.ImageDraw.Draw(image)

        # make a dictionary of character images
        xcuts = [draw.textsize(A[:i+1])[0] for i in range(len(A))]
        xcuts = [0]+xcuts
        ycut = draw.textsize(A)[1]
        draw.text((0,0), A, WHT)
        self.wcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])
        draw.text((0,0), A, GRN)
        self.gcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])
        draw.text((0,0), A, RED)
        self.rcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])

    # UNUSED FUNCTION, TO BE DELETED
    def textimage(self,txt,format='RGBA'):
        print(len(txt))
        self.txtpos = 0

        image = PIL.Image.new(format, (TEXT_SCALE * TEXT_WIDTH, TEXT_HEIGHT * TEXT_SCALE), TEXT_BACKGROUND)
        draw = PIL.ImageDraw.Draw(image)
        font = PIL.ImageFont.truetype(TEXT_FONTFACE, TEXT_FONTSIZE)
        draw = draw.multiline_text((0,0),txt,gencolor(),font,LINE_SPACING,align="left")
    	#draw.text((2, 0), txt, TEXT_COLOUR, font = font)
        return image.resize((TEXT_WIDTH, TEXT_HEIGHT), PIL.Image.ANTIALIAS)

    def make_color(self,text):
        print("yeet")
        u = Util()
        lines = u.countNL(txt)
        length = u.countLen(txt)
        return GRN

    def testimage(self,format = 'RGB'):
        # Test it...
        image = PIL.Image.new(format, (TEXT_SCALE * TEXT_WIDTH, TEXT_HEIGHT * TEXT_SCALE), TEXT_BACKGROUND)

        x = 0
        y = 0

        temp = self.wcl
        for c in "This is just a nifty text string+22 -341 d\n asdasdasdadsasdasd":
            if(c == '+'):
                temp = self.gcl
            elif(c == '-'):
                temp = self.rcl
            elif(c == ' '):
                temp = self.wcl

            w, char_image = temp[c]
            image.paste(char_image, xy)
            x += w

        #image2.show()
        return image

if(__name__=="__main__"):
    f = Front()
    #f.textimage("what is gonig on\n+123123 asd\nyeet -12344\nyike").save('texttest.png')
    f.testimage().save('yeet.png')
