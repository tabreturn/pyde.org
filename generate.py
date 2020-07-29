import os
import re
import shutil
from jinja2 import Environment, FileSystemLoader
from lexer import ProcessingPyLexer
from markdown2 import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pyp5js.commands import transcrypt_sketch

examples = {}

# create _site directory

if os.path.exists('_site'):
    shutil.rmtree('_site')

os.makedirs('_site')

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
