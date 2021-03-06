#fills the content into the template for each piece of content
#or, wraps a copy of the template around each piece of content
#if you prefer to think about it that way
#intended to be run before loading a page locally or committing
#(maybe eventually I'll tie it to a github action)
from pathlib import Path
import os
from copy import deepcopy
import posts

def all_files_of_types(filetypes, path=''):
    result = []
    for filetype in filetypes:
        result.extend(Path(path).rglob('*.'+filetype))
    return result

template_file = open("template/template.html",'r')
template = template_file.read()
template_file.close()
content_marker = "CONTENT SHOULD BE HERE"

input_dir = "blog-content" #this folder is gitignored so that I can keep it separate and private
output_dir = "."
if not os.path.exists(input_dir):
    print(input_dir, "doesn't exist")
    exit()
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


#special additional processing
special_cases = {
    #arbitrary remapping of urls
    #"path/to/file.html": "the/actual/url.html"
}
skip_marker = "SKIP"
title_marker = "<title>"
template_title_marker = "PAGE TITLE"

posts_dir = os.path.join(input_dir, 'posts')
all_posts = posts.all_posts_html(posts_dir)
most_recent = posts.most_recent_post(posts_dir)
other_recent = posts.other_recent_posts(posts_dir,5)
content_filenames = all_files_of_types(['html'], input_dir)
all_posts_marker = "ALL POSTS"
most_recent_marker = "MOST RECENT POST"
other_recent_marker = "OTHER RECENT POSTS"

for content_filename in content_filenames:
    with open(content_filename, 'r') as content_file:
        content = content_file.read()
        output_filename = str(content_filename).replace(input_dir,output_dir,1)
        if(output_filename in special_cases):
            output_filename = special_cases[output_filename]
        if skip_marker in content:
            if os.path.exists(output_filename):
                os.remove(output_filename)
            continue
        title = "Nathaniel Saxe"
        if title_marker in content:
            title_begin = content.find('>',content.find(title_marker))
            title_end = content.find('<',title_begin+1)
            page_title = content[title_begin+1:title_end]
            if page_title != '':
                title = page_title + " | " + title
        content = content.replace("\n\n", "\n</p><p>\n")
        out_dir = os.path.dirname(output_filename)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(output_filename, 'w') as output_file:
            page_data = deepcopy(template).replace(template_title_marker, title).replace(content_marker,content)
            page_data = page_data.replace(most_recent_marker,most_recent).replace(other_recent_marker,other_recent).replace(all_posts_marker,all_posts)
            output_file.write(page_data)
        print(output_filename)
