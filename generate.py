'''
Instructions:
https://github.com/tabreturn/tabreturn.pyde/blob/master/README.md
'''

import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader
from lexer import ProcessingPyLexer
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pyp5js.commands import transcrypt_sketch
from pyp5js.config import SKETCHBOOK_DIR

EXAMPLES_DIR = os.path.abspath(os.path.join(SKETCHBOOK_DIR, os.pardir))

# delete any partially transcribed files from a previous run

if os.path.exists(SKETCHBOOK_DIR):
    shutil.rmtree(SKETCHBOOK_DIR)

# create _site directory

SITE_DIR = '_site'

if os.path.exists(SITE_DIR):
    shutil.rmtree(SITE_DIR)

os.makedirs(SITE_DIR)

# rename and copy sketches to _temp directory

for category in os.listdir(EXAMPLES_DIR):

    if category == '.gitignore':
        continue

    category_dir = os.path.join(EXAMPLES_DIR, category)

    for sub_category in os.listdir(category_dir):
        # rename any sub-category paths incompatible with pyp5js
        sc_words = sub_category.split()
        sc_title = ' '.join(word[0].upper() + word[1:] for word in sc_words)
        sc_final = sc_title.replace(' ', '').replace('-', '_')
        sub_category_dir = os.path.join(EXAMPLES_DIR, category, sub_category)

        for sketch in os.listdir(sub_category_dir):
            sketch_path = os.path.join(sub_category_dir, sketch)
            new_name = '{}__{}__{}'.format(category, sc_final, sketch)
            shutil.copytree(sketch_path, os.path.join(SKETCHBOOK_DIR, new_name))

# rename .pyde extensions (in _temp directory) to .py

for temp_sketch in os.listdir(SKETCHBOOK_DIR):
    temp_sketch_dir = os.path.join(SKETCHBOOK_DIR, temp_sketch)

    for sketch_file in os.listdir(temp_sketch_dir):

        if sketch_file[-5:] == '.pyde':
            os.rename(
              os.path.join(temp_sketch_dir, sketch_file),
              os.path.join(temp_sketch_dir, temp_sketch + '.py')
            )


def addDrawAndSetupFunctions(code):
    """Add setup() and draw() functions for pyp5js compatibility"""
    flush_size_function = re.compile(r'(^size\()(.*)', flags=re.MULTILINE)
    indent_size_function = r'def setup():\n    \1\2\n\ndef draw():'
    code = flush_size_function.sub(indent_size_function, code)
    result = ''
    indent_mode = False
    def_draw = 'def draw():'

    for line in code.split('\n'):

        if not indent_mode and line[0:len(def_draw)] == def_draw:
            indent_mode = True
            result += line
            continue

        if indent_mode and line[:4] == 'def ':
            indent_mode = False

        if indent_mode:
            result += '    {}\n'.format(line)

        else:
            result += line + '\n'

    return result


# transcribe sketches using pyp5js

for temp_sketch in os.listdir(SKETCHBOOK_DIR):
    sketch_file = os.path.join(SKETCHBOOK_DIR, temp_sketch, temp_sketch+'.py')
    sketch_read = open(sketch_file, 'rt')
    sketch_content = sketch_read.read()
    # if size isn't indented, there's no setup() and draw() function
    if sketch_content.find('    size(') < 0:
        sketch_content = addDrawAndSetupFunctions(sketch_content)
    # replace size() function for pyp5js compatibility
    sketch_content = sketch_content.replace('size(', 'createCanvas(')
    sketch_content = 'from pyp5js import *\n' + sketch_content
    sketch_read.close()
    sketch_write = open(sketch_file, 'wt')
    sketch_write.write(sketch_content)
    sketch_write.close()
    transcrypt_sketch(temp_sketch)

# move transcribed sketches to _site directory

for temp_sketch in os.listdir(SKETCHBOOK_DIR):
    source_dir = os.path.join(SKETCHBOOK_DIR, temp_sketch, 'target')
    target_dir = os.path.join(SITE_DIR, temp_sketch)
    shutil.move(source_dir, target_dir)

# load templates

env = Environment(loader=FileSystemLoader('templates'))

templates = {
  'index': env.get_template('index.html'),
  'example': env.get_template('example.html'),
}

# read all sketch data into a list

sketches_data = []

for temp_sketch in os.listdir(SITE_DIR):
    temp_sketch_path = os.path.join(SKETCHBOOK_DIR, temp_sketch)
    temp_sketch_path = os.path.join(temp_sketch_path, temp_sketch + '.py')
    # undo pyp5js amends (convert back to processing.py code)
    sketch_read = open(sketch_file, 'rt')
    sketch_content = sketch_read.read()
    sketch_content = sketch_content.replace('from pyp5js import *\n', '')
    sketch_content = sketch_content.replace('createCanvas(', 'size(')
    # separate out description code and metadata
    sketch_description = re.findall('"""[\s\S]*?"""', sketch_content)[0]
    sketch_code = sketch_content.replace(sketch_description, '')
    sketch_description = sketch_description.replace('"""', '')
    sketch_description = sketch_description.split('\n', 2)[2]
    sketch_code = highlight(sketch_code, ProcessingPyLexer(), HtmlFormatter())
    cat_subcat_sketch = temp_sketch.split('__')
    sketches_data.append({
      'file_name': temp_sketch,
      'category': cat_subcat_sketch[0],
      'sub_category': cat_subcat_sketch[1],
      'title': cat_subcat_sketch[2],
      'description': sketch_description,
      'code': sketch_code
    })

# generate landing page

index_html = templates['index'].render(metadata=sketches_data)

with open(os.path.join(SITE_DIR, 'index.html'), 'w') as file:
    file.write(index_html)

# copy static assets into _site directory

for asset in os.listdir('static'):
    asset_source = os.path.join('static', asset)
    asset_destination = os.path.join(SITE_DIR, asset)
    shutil.copyfile(asset_source, asset_destination)

# generate example pages

for sketch in sketches_data:
    example_html = templates['example'].render(contents=sketch)
    example_dir = os.path.join(SITE_DIR, sketch['file_name'])

    with open(os.path.join(example_dir, 'index.html'), 'w') as file:
        file.write(example_html)
