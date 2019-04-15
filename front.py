import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import string

from random import randint
from util import Util

CHAR_HEIGHT = 38
CHAR_WIDTH  = 16

TEXT_HEIGHT = 10
TEXT_WIDTH = 100
TEXT_SCALE = 4

TEXT_FONTFACE = "fonts/Roboto-Regular.ttf"
TEXT_FONTFACE_HEADDING = "fonts/Roboto-Regular.ttf"
TEXT_FONTSIZE = 30
TEXT_BACKGROUND = (0, 0, 0, 0)
LINE_SPACING = 5

WHT = (255,255,255,255)
RED = (255,0,0,255)
GRN = (0,255,0,255)
YLW = (245,230,83,255)

POS_CHAR = '.'
NEG_CHAR = ','
NEU_CHAR = '/'

class Front():

    printable = " ".join(string.printable)
    gcl = None
    wcl = None
    rcl = None
    ycl = None

    def __init__(self,format='RGBA'):
        A = self.printable
        print(string.printable)
        image = PIL.Image.new(format, (len(A)*CHAR_WIDTH,CHAR_HEIGHT),TEXT_BACKGROUND)
        draw = PIL.ImageDraw.Draw(image)
        font = PIL.ImageFont.truetype(TEXT_FONTFACE, TEXT_FONTSIZE)

        xcuts = [draw.textsize(A[:i+1],font)[0] for i in range(len(A))]
        xcuts = [0]+xcuts
        ycut = draw.textsize(A,font)[1]
        draw.text((0,0), A, WHT, font)
        self.wcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])
        draw.text((0,0), A, GRN, font)
        self.gcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])
        draw.text((0,0), A, RED, font)
        self.rcl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])
        draw.text((0,0), A, YLW, font)
        self.ycl = dict([(A[i], (xcuts[i+1]-xcuts[i]+1, image.crop((xcuts[i]-1, 0, xcuts[i+1], ycut)))) for i in range(len(xcuts)-1)])


    def testimage(self,txt,format = 'RGBA'):

        txt,width,height = self.formatString(txt)

        image = PIL.Image.new(format, (width,height), TEXT_BACKGROUND)

        x = 5
        y = 0

        temp = self.wcl

        for c in txt:
            if(c == ' '):
                x = x + CHAR_WIDTH
            elif(c == POS_CHAR):
                temp = self.gcl
            elif(c == NEG_CHAR):
                temp = self.rcl
            elif(c == NEU_CHAR):
                temp = self.ycl
            elif(c == ' '):
                temp = self.wcl
            if(c == '\\'):
                y = y + CHAR_HEIGHT
                x = 5
                continue

            w, char_image = temp[c]
            image.paste(char_image,(x,y))
            x += w

        image.show()
        return image.resize((width, height), PIL.Image.ANTIALIAS)

    def formatString(self,txt):
        #Format:
        #Overall | PR: xxxx.xx Battles: xxxx DMG: xxxxx.xx WR: xx.xx% Kills: x.xx
        #Weekly  | PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x
        #Monthly | PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x

        u = Util()

        ostats = "Overall | PR: xxxx.xx Battles: xxxx DMG: xxxxx.xx WR: xx.xx% Kills: x.xx"
        wstats = "Weekly | PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x"
        mstats = "Monthly | PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x"

        a = str.splitlines(txt)
        print(a)

        #max(lambda x : x = len())

        formatted = "\\".join(a)
        width = (CHAR_WIDTH * u.countLen(a[0]))
        print(width)
        height = (CHAR_HEIGHT * (u.countNL(formatted)+1))

        return (formatted,width,height)


if(__name__=="__main__"):
    f = Front()
    f.testimage("Overall | PR: xxxx.xx Battles: xxxx DMG: xxxxx.xx WR: xx.xx% Kills: x.xx\nWeekly | PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x\nMonthly| PR: +xxxx.x Battles: +xxx DMG: +xxxxx.x WR: +xx.x% Kills: +x.x").save('yeet.png')
    #f.testimage("what is gonig on\\+123123 asd\\yeet -12344\\yike").save('yeet.png')
