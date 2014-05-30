from cStringIO import StringIO
from itertools import count

from ampy import ampy as amp


import Image

from mediawindows import exceptions

# oh jeez we need a unique port on windows. On *nix we could use domain sockets
PORT = 31337

####################------------------------------------------------------------
## AMP Protocol / related things
####################------------------------------------------------------------

# BigString is stolen from the AMP docs. Turns out you can't pass
# things larger than 64k...
# http://amp-protocol.net/Types/BigString

CHUNK_MAX = 0xffff
class BigString(amp.Argument):
    def fromBox(self, name, strings, objects, proto):
        value = StringIO()
        value.write(strings.get(name))
        for counter in count(2):
            chunk = strings.get("%s.%d" % (name, counter))
            if chunk is None:
                break
            value.write(chunk)
        objects[name] = self.buildvalue(value.getvalue())
 
    def buildvalue(self, value):
        return value
 
    def toBox(self, name, strings, objects, proto):
        value = StringIO(self.fromvalue(objects[name]))
        firstChunk = value.read(CHUNK_MAX)
        strings[name] = firstChunk
        counter = 2
        while True:
            nextChunk = value.read(CHUNK_MAX)
            if not nextChunk:
                break
            strings["%s.%d" % (name, counter)] = nextChunk
            counter += 1
 
    def fromvalue(self, value):
        return value
 
class BigUnicode(BigString):
    def buildvalue(self, value):
        return value.decode('utf-8')
    
    def fromvalue(self, value):
        return value.encode('utf-8')


class PILImage(object):
    """
    This is an AMP argument converter that transforms PIL Image objects to and
    from four string key-value pairs in the AMP message.
    
    keys are of the form <name>.<subkey>, and the subkeys are as follows:
        
        data
            the binary blob containing the image data
        width
            the integer width
        height
            the integer height
        mode
            the string image mode
    
    """
    # I'm a bit iffy about creating new keys... in theory they could conflict
    # with other keys. The alternative is packing this with json or something,
    # but that's slow and I'm lazy.
    
    bigstring = BigString()
    
    def toBox(self, name, strings, objects, proto):
        img = objects[name]
        w, h = img.size
        strings.update({
            '%s.width' % name: str(w),
            '%s.height' % name: str(h),
            '%s.mode' % name: img.mode})
        
        dataname = "%s.data" % name
        self.bigstring.toBox(
            dataname, strings, {dataname:img.tostring()}, proto)
    
    def fromBox(self, name, strings, objects, proto):
        dataname = "%s.data" % name
        tempd = {}
        self.bigstring.fromBox(dataname, strings, tempd, proto)
        
        objects[name] = Image.fromstring(
            strings['%s.mode' % name],
            (
                int(strings['%s.width' % name]),
                int(strings['%s.height' % name])),
            tempd['%s.data' % name])


class StartInspect(amp.Command):
    """Start a new inspect window.

    This command returns an inspector handle that may be used to invoke
    further operations on the inspector window.

    """
    arguments = [
        ('img', PILImage()),
        ('inspectable', amp.Boolean())]
    response = [('inspector_id', amp.Integer())]

class UpdateInspect(amp.Command):
    """Update an inspect window.
    
    This command may return an error indicating that no such window exists.
    
    """
    arguments = [
        ('inspector_id', amp.Integer()),
        ('img', PILImage())]
    response = []
    errors = {exceptions.WindowDoesNotExistError: 'WINDOW_DOES_NOT_EXIST'}

class StopInspect(amp.Command):
    """Close an inspect window.
    
    This command may return an error indicating that no such window exists.
    
    """
    arguments = [
        ('inspector_id', amp.Integer())]
    response = []
    errors = {exceptions.WindowDoesNotExistError: 'WINDOW_DOES_NOT_EXIST'}

class PollInspect(amp.Command):
    """Poll an inspect window to see if it's still open.
    
    The result of this command may be invalid as soon as it is given.
    Relying on the return value will result in race conditions.
    
    """
    arguments = [
        ('inspector_id', amp.Integer())]
    response = [('is_closed', amp.Boolean())]

class _Ask(amp.Command):
    arguments = [('initialdir', amp.String())]
    response = [("path", amp.Unicode())]
    errors = {exceptions.DialogCanceledException: 'DIALOG_CANCELED'}

class AskSaveasFilename(_Ask):
    """Amp command for executing tkFileDialog.asksaveasfilename"""
    pass

class AskOpenFilename(_Ask):
    """Amp command for executing tkFileDialog.askopenfilename"""
    pass

class AskDirectory(_Ask):
    """Amp command for executing tkFileDialog.askdirectory"""
    pass

class AskColor(_Ask):
    """Amp command for executing tkFileDialog.askcolor"""
    arguments = [
        ("r", amp.Integer()),
        ("g", amp.Integer()),
        ("b", amp.Integer())]
    response = arguments # asks with start color, returns color

class Say(amp.Command):
    arguments = [
        ('text', BigString())]
    response = []
