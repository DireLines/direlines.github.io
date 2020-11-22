#fills the content into the template for each piece of content
#or, wraps a copy of the template around each piece of content
#if you prefer to think about it that way
#intended to be run before loading a page locally or committing
#(maybe eventually I'll tie it to a github action)
from pathlib import Path
import os
from copy import deepcopy

# filename('/path/to/cool-file.txt') = 'cool-file'
def filename(filepath):
    return os.path.splitext(os.path.basename(obj_filename))[0]

def all_files_of_types(filetypes, path=''):
    result = []
    for filetype in filetypes:
        result.extend(Path(path).rglob('*.'+filetype))
    return result

template_file = open("template/template.html",'r')
template = template_file.read()
template_file.close()
content_marker = "CONTENT SHOULD BE HERE"

input_dir = "blog-content/visible" #this folder is gitignored so that I can keep it separate and private
output_dir = "posts"
if not os.path.exists(input_dir):
    print(input_dir, "doesn't exist")
    exit()
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

special_cases = {
    "posts/index.html":"index.html",
    "posts/posts.html":"posts.html",
    "posts/about.html":"about.html",
    "posts/contact.html":"contact.html",
}
content_filenames = all_files_of_types(['html'], input_dir)
for content_filename in content_filenames:
    with open(content_filename, 'r') as content_file:
        content = content_file.read()
        output_filename = str(content_filename).replace(input_dir,output_dir,1)
        if(output_filename in special_cases):
            output_filename = special_cases[output_filename]
        out_dir = os.path.dirname(output_filename)
        if out_dir != '' and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(output_filename, 'w') as output_file:
            page_data = deepcopy(template).replace(content_marker,content)
            output_file.write(page_data)
        print(output_filename)