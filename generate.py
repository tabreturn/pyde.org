import os
import shutil
import subprocess
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

# create _site directory

if os.path.exists('_site'):
    shutil.rmtree('_site')

os.makedirs('_site')

examples = {}

# load examples markdown into examples dictionary

for eg in os.listdir('examples'):

    if eg.endswith('.md'):

        with open(os.path.join('examples', eg), 'r') as file:
            extras = ['metadata', 'fenced-code-blocks']
            examples[eg] = markdown(file.read(), extras=extras)

# load templates

env = Environment(loader=FileSystemLoader('templates'))

templates = {
  'index': env.get_template('index.html'),
  'example': env.get_template('example.html'),
}

# generate landing page

metadata = [examples[eg].metadata for eg in examples]
index_html = templates['index'].render(contents=metadata)

with open('_site/index.html', 'w') as file:
    file.write(index_html)

# generate example pages

for eg in examples:
    metadata = examples[eg].metadata
    contents = {
      'content': examples[eg],
      'title': metadata['title'],
      'category': metadata['category'],
      'updated': metadata['updated'],
      'filename': metadata['title'].lower().replace(' ', '_')
    }
    example_html = templates['example'].render(contents=contents)
    path = '_site/{}.html'.format(contents['filename'])
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as file:
        file.write(example_html)

asset_paths = ['examples', 'templates']

# generate js sketches and copy into _site directory

for eg_filename in examples.keys():
    no_ext = eg_filename[0:-3]
    process = subprocess.Popen('pyp5js transcrypt {}'.format(no_ext).split())
    output, error = process.communicate()
    shutil.copytree('examples/{}'.format(no_ext), os.path.join('_site', no_ext))

# copy static assets into _site directory

for path in asset_paths:

    for asset in os.listdir(path):

        if asset.endswith(('.css', '.js', '.png')):
            site_path = os.path.join(path, asset)
            shutil.copy(site_path, os.path.join('_site', asset))
