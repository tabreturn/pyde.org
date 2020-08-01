'''
The example sketch files are retrieved from:
https://github.com/jdf/processing.py/tree/master/mode/examples and placed in 
the "examples" directory.

There are some sketches that are problematic that you'll need to delete. Many 
of fail because of the way they're organized (directory structure) which 
shouldn't be difficult to fix at some point in the future. This program expects
sketch to be organized as:

*category > sub-category > sketch*

For example:

*Basics > Camera > MoveEye*

Delete the directories:
* Advanced (directory structure incompatible)
* Contributed Libraries in Python (I still need to look at libraries)
* Python Mode Differences (directory structure incompatible)

Also, delete:
* Topics/ContinuousLines (directory structure incompatible)
* Topics/Pattern (directory structure incompatible)
* Topics/Pulses (directory structure incompatible)
* Topics/File IO/LoadFile2 (can't import from module 'collections')
'''

import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader
from lexer import ProcessingPyLexer
from markdown2 import markdown
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
    
    category_dir = os.path.join(EXAMPLES_DIR, category)
    
    for sub_category in os.listdir(category_dir):
        # rename any sub-category paths incompatible with pyp5js
        sc_words = sub_category.split()
        sc_title = ' '.join(word[0].upper() + word[1:] for word in sc_words)
        sc_final =  sc_title.replace(' ', '').replace('-', '_')
        
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

# transcribe sketches using pyp5js

for temp_sketch in os.listdir(SKETCHBOOK_DIR):
    transcrypt_sketch(temp_sketch)

# move transcribed sketches to _site directory

for temp_sketch in os.listdir(SKETCHBOOK_DIR):
    source_dir = os.path.join(SKETCHBOOK_DIR, temp_sketch, 'target')
    target_dir = os.path.join(SITE_DIR, temp_sketch)
    shutil.move(source_dir, target_dir)

shutil.rmtree(SKETCHBOOK_DIR)


'''
# load templates

env = Environment(loader=FileSystemLoader('templates'))

templates = {
  'index': env.get_template('index.html'),
  'example': env.get_template('example.html'),
}

# generate landing page

metadata_all = [eg['metadata'] for eg in examples.values()]
index_html = templates['index'].render(metadata=metadata_all)

with open('_site/index.html', 'w') as file:
    file.write(index_html)
'''

'''


for group in os.listdir(category_directory):
    group_directory = os.path.join(examples_directory, category)
    examples[category][group] = {}


category_directory = os.path.join(examples_directory, category)

for group in os.listdir(category_directory):
    group_directory = os.path.join(examples_directory, category)
    examples[category][group] = {}
      
        for sketch in os.listdir(group_directory):
            print(category + '|' + group + '|' + sketch)
            sketch_file = os.path.join(group_directory, sketch, sketch+'.pde')
            examples[category][group][sketch] = {}
            
            #print(sketch_file)
            #with open(sketch_file, 'r') as f:
            #    print(f.read())
 
            
        
file='.env'
with open(file, 'w') as filetowrite:
    filetowrite.write("SKETCHBOOK_DIR = './examples/Basics/Structure'") 

eg_name = 'Coordinates'
transcrypt_sketch(eg_name)

# load examples markdown into examples dictionary

for eg in sorted(os.listdir('examples')):
    eg_directory = os.path.join('examples', eg)
    eg_description = os.path.join(eg_directory, 'description.md')
    eg_sketch = os.path.join(eg_directory, eg+'.py')

    with open(eg_description, 'r') as file:
        metadata = {
          'file_name': eg,
          'category': eg.split('__')[0].replace('_', ' '),
          'index': eg.split('__')[1].replace('_', ' ')[:2],
          'title': eg.split('__')[1].replace('_', ' ')[3:],
          'image': 'canvas.png'
        }
        sketch_code = open(eg_sketch, 'r').read()
        sketch_code = re.sub('from pyp5js import .*\n*', '', sketch_code)
        sketch_code = re.sub('createCanvas', 'size', sketch_code)
        sketch_code = highlight(sketch_code, ProcessingPyLexer(), HtmlFormatter())
        description = markdown(file.read())
        examples[eg] = {
          'metadata': metadata,
          'sketch_code': sketch_code,
          'description': description
        }



# generate example pages and js sketches

for eg_page in examples.values():
    eg_html = templates['example'].render(contents=eg_page)
    eg_name = eg_page['metadata']['file_name']
    eg_path = os.path.join('_site', eg_name)
    os.makedirs(eg_path)
    png_source = os.path.join('examples', eg_name, 'canvas.png')
    png_destination = os.path.join('_site', eg_name, 'canvas.png')
    shutil.copyfile(png_source, png_destination)

    with open(os.path.join(eg_path, eg_name+'.html'), 'w') as file:
        file.write(eg_html)

    transcrypt_sketch(eg_name)
    js_source = os.path.join('examples', eg_name, 'target')
    js_destination = os.path.join('_site', eg_name, 'target')
    shutil.copytree(js_source, js_destination)
    shutil.rmtree(js_source)

# copy static assets into _site directory

for asset in os.listdir('static'):
    asset_source = os.path.join('static', asset)
    asset_destination = os.path.join('_site', asset)
    shutil.copyfile(asset_source, asset_destination)
'''
