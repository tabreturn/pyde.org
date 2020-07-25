import os, shutil
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

# create _site directory
if not os.path.exists('_site'):
    os.makedirs('_site')

EXAMPLES = {}

for markdown_post in os.listdir('examples'):
    
    if markdown_post.endswith(".md"):
  
        file_path = os.path.join('examples', markdown_post)

        with open(file_path, 'r') as file:
            EXAMPLES[markdown_post] = markdown(file.read(), extras=['metadata'])

EXAMPLES = {
    post: EXAMPLES[post] for post in sorted(EXAMPLES, key=lambda post: datetime.strptime(EXAMPLES[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

env = Environment(loader=PackageLoader('generate', 'templates'))
home_template = env.get_template('index.html')
post_template = env.get_template('example.html')

posts_metadata = [EXAMPLES[post].metadata for post in EXAMPLES]
home_html = home_template.render(posts=posts_metadata)

with open('_site/index.html', 'w') as file:
    file.write(home_html)

for post in EXAMPLES:
    post_metadata = EXAMPLES[post].metadata

    post_data = {
        'content': EXAMPLES[post],
        'title': post_metadata['title'],
        'date': post_metadata['date']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = '_site/examples/{}.html'.format(post_metadata['title'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)



for markdown_post in os.listdir('templates'):
                
    if markdown_post.endswith(('.css', '.js')):
        
        file_path = os.path.join('templates', markdown_post)
        source = file_path
        
        destination = os.path.join('_site', markdown_post)
        shutil.copy(source, destination) 




for markdown_post in os.listdir('examples'):
    
            
    if markdown_post.endswith(".png"):
        
        file_path = os.path.join('examples', markdown_post)
        source = file_path
        
        destination = os.path.join('_site/examples', markdown_post)
        shutil.copy(source, destination) 
