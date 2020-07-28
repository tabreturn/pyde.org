from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.lexer import RegexLexer, words
from pygments.token import *

class ProcessingPyLexer(PythonLexer):
    tokens = {
        'builtins': [
          (words((
            '__import__', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray',
            'bytes', 'chr', 'classmethod', 'cmp', 'compile', 'complex',
            'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'filter',
            'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
            'hash', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
            'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview',
            'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple',
            'type', 'vars', 'zip',
            # processing.py additions
            'abs', 'acos', 'alpha', 'ambient', 'ambientLight', 'applyMatrix',
            'arc', 'asin', 'atan', 'atan2', 'background', 'beginCamera',
            'beginContour', 'beginRaw', 'beginShape', 'bezier', 'bezierDetail',
            'bezierPoint', 'bezierTangent', 'bezierVertex', 'blend',
            'blendColor', 'blendMode', 'blue', 'box', 'brightness', 'camera',
            'ceil', 'circle', 'clear', 'clip', 'color', 'colorMode',
            'constrain', 'copy', 'cos', 'createFont', 'createGraphics',
            'createImage', 'createReader', 'createShape', 'createWriter', 
            'cursor', 'curve', 'curveDetail', 'curvePoint', 'curveTangent',
            'curveTightness', 'curveVertex', 'day', 'degrees',
            'directionalLight', 'dist', 'draw', 'ellipse', 'ellipseMode',
            'emissive', 'endCamera', 'endContour', 'endRaw', 'endShape',
            'exit', 'exp', 'fill', 'filter', 'floor', 'frameRate', 'frustum',
            'fullScreen', 'get', 'green', 'hour', 'hue', 'image', 'imageMode',
            'keyPressed', 'keyReleased', 'keyTyped', 'lerp', 'lerpColor',
            'lightFalloff', 'lightSpecular', 'lights', 'line', 'loadBytes',
            'loadFont', 'loadImage', 'loadPixels', 'loadShader', 'loadShape',
            'loadStrings', 'log', 'loop', 'mag', 'map', 'max', 'millis', 'min',
            'minute', 'modelX', 'modelY', 'modelZ', 'month', 'mouseButton',
            'mouseClicked', 'mouseDragged', 'mouseMoved', 'mousePressed',
            'mousePressed', 'mouseReleased', 'mouseWheel', 'noClip',
            'noCursor', 'noFill', 'noLights', 'noLoop', 'noSmooth', 'noStroke',
            'noTint', 'noise', 'noiseDetail', 'noiseSeed', 'norm', 'normal',
            'ortho', 'perspective', 'pixels', 'point', 'pointLight',
            'popMatrix', 'popStyle', 'pow', 'printCamera', 'printMatrix',
            'printProjection', 'pushMatrix', 'pushStyle', 'quad',
            'quadraticVertex', 'radians', 'random', 'randomGaussian',
            'randomSeed', 'range', 'rect', 'rectMode', 'red', 'redraw',
            'requestImage', 'resetMatrix', 'resetShader', 'rotate', 'rotateX',
            'rotateY', 'rotateZ', 'round', 'saturation', 'save', 'saveBytes',
            'saveFrame', 'saveStrings', 'scale', 'screenX', 'screenY',
            'screenZ', 'second', 'selectFolder', 'selectInput', 'selectOutput',
            'set', 'setup', 'shader', 'shape', 'shapeMode', 'shearX', 'shearY',
            'shininess', 'sin', 'size', 'smooth', 'specular', 'sphere',
            'sphereDetail', 'spotLight', 'sq', 'sqrt', 'square', 'stroke',
            'strokeCap', 'strokeJoin', 'strokeWeight', 'tan', 'text',
            'textAlign', 'textAscent', 'textDescent', 'textFont',
            'textLeading', 'textMode', 'textSize', 'textWidth', 'texture',
            'textureMode', 'textureWrap', 'tint', 'translate', 'triangle',
            'updatePixels', 'vertex', 'year'
            ), prefix=r'(?<!\.)', suffix=r'\b'), Name.Builtin)
        ],
    }
