from re import sub, findall, S as RES
from Components.config import config
from Components.ConditionalWidget import BlinkingWidget
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Components.MenuList import MenuList
from enigma import eListboxPythonMultiContent, gFont
import xml.etree.ElementTree as ET
import six

MEDIAROOT = "/usr/lib/enigma2/python/Plugins/Extensions/TVSpielfilm/"
PICPATH = MEDIAROOT + "pic/"
ICONPATH = PICPATH + "icons/"
TVSPNG = PICPATH + "tvspielfilm.png"
TVSHDPNG = PICPATH + "tvspielfilmHD.png"


class serviceDB():

    def __init__(self, servicefile):
        self.servicefile = servicefile
        self.d = dict()
        try:
            for x in open(self.servicefile):
                key, val = x.split()
                self.d[key] = val

        except:
            pass

    def lookup(self, key):
        if key in self.d:
            return self.d[key]
        return 'nope'

    def close(self):
        pass


class BlinkingLabel(Label, BlinkingWidget):

    def __init__(self, text = ''):
        Label.__init__(self, text=text)
        BlinkingWidget.__init__(self)

class ItemList(MenuList):

    def __init__(self, items, enableWrapAround = True):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
#        if config.plugins.tvspielfilm.font.value == 'yes':
#            self.l.setFont(-2, gFont('Sans', 24))
#            if config.plugins.tvspielfilm.font_size.value == 'verylarge':
#                self.l.setFont(-1, gFont('Sans', 26))
#                self.l.setFont(0, gFont('Sans', 24))
#                self.l.setFont(1, gFont('Sans', 22))
#                self.l.setFont(2, gFont('Sans', 20))
#            elif config.plugins.tvspielfilm.font_size.value == 'large':
#                self.l.setFont(-1, gFont('Sans', 24))
#                self.l.setFont(0, gFont('Sans', 22))
#                self.l.setFont(1, gFont('Sans', 20))
#                self.l.setFont(2, gFont('Sans', 18))
#            else:
#                self.l.setFont(-1, gFont('Sans', 22))
#                self.l.setFont(0, gFont('Sans', 20))
#                self.l.setFont(1, gFont('Sans', 18))
#                self.l.setFont(2, gFont('Sans', 16))
#        else:
        self.l.setFont(-2, gFont('Regular', 24))
        if config.plugins.tvspielfilm.font_size.value == 'verylarge':
            self.l.setFont(-2, gFont('Regular', 28))
            self.l.setFont(-1, gFont('Regular', 28))
            self.l.setFont(0, gFont('Regular', 24))
            self.l.setFont(1, gFont('Regular', 22))
            self.l.setFont(2, gFont('Regular', 20))
        elif config.plugins.tvspielfilm.font_size.value == 'large':
            self.l.setFont(-1, gFont('Regular', 24))
            self.l.setFont(0, gFont('Regular', 22))
            self.l.setFont(1, gFont('Regular', 20))
            self.l.setFont(2, gFont('Regular', 18))
        else:
            self.l.setFont(-1, gFont('Regular', 22))
            self.l.setFont(0, gFont('Regular', 20))
            self.l.setFont(1, gFont('Regular', 18))
            self.l.setFont(2, gFont('Regular', 16))


def applySkinVars(skin, dict):
    for key in dict.keys():
        try:
            skin = skin.replace('{' + key + '}', dict[key])
        except Exception as e:
            print(e, '@key=', key)
    return skin

def makeWeekDay(weekday):
    if weekday == 0:
        _weekday = 'Montag'
    elif weekday == 1:
        _weekday = 'Dienstag'
    elif weekday == 2:
        _weekday = 'Mittwoch'
    elif weekday == 3:
        _weekday = 'Donnerstag'
    elif weekday == 4:
        _weekday = 'Freitag'
    elif weekday == 5:
        _weekday = 'Samstag'
    elif weekday == 6:
        _weekday = 'Sonntag'
    return _weekday

def scaleskin(skin, factor):
    if factor == 1:
        return skin

    def calc(old, factor):
        if ',' in old and '_' in old:
            _old = old.split(',')
            a = _old[0]
            if a[0] == '_':
                a = a[1:]
                a = int(int(a) * factor)
            b = _old[1]
            if b[0] == '_':
                b = b[1:]
                b = int(int(b) * factor)
            return "%s,%s" % (a,b)
        return old

    root = ET.fromstring(skin)    
    if 'position' in root.attrib:
        root.attrib['position'] = calc(root.attrib['position'], factor)
    if 'size' in root.attrib:
        root.attrib['size'] = calc(root.attrib['size'], factor)
    for child in root:
        if 'position' in child.attrib:
            child.attrib['position'] = calc(child.attrib['position'], factor)
        if 'size' in child.attrib:
            child.attrib['size'] = calc(child.attrib['size'], factor)
    return six.ensure_str(ET.tostring(root))

