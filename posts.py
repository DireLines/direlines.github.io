#used by build script to generate html for list of all posts
from pathlib import Path
import os
import datetime

def all_files_of_types(filetypes, path=''):
    result = []
    for filetype in filetypes:
        result.extend(Path(path).rglob('*.'+filetype))
    return result

def to_html(title, desc, date, link):
    return f'{date}: <a href="{link}">{title}</a> - {desc}'

def inside_first_div(div,text):
    div_start = text.find('>',text.find(div))
    div_end = text.find('<',div_start+1)
    return text[div_start+1:div_end]

# filename('/path/to/cool-file.txt') = 'cool-file.txt'
def filename(filepath):
    return os.path.basename(filepath)
def url_path(filepath):
    return os.path.join('posts',filename(filepath))

#python list of all posts' html
#I return this instead of the html <ul> list
#so that I can slice it 
def all_posts(posts_dir):
    if not os.path.exists(posts_dir):
        print(posts_dir, "doesn't exist")
        return
    title_marker = '<div class="title">'
    desc_marker = '<div class="subtitle">'
    date_marker = '<div class="date">'
    skip_marker = "SKIP"
    
    result = []
    
    post_filenames = all_files_of_types(['html'], posts_dir)
    for post_filename in post_filenames:
        with open(post_filename, 'r') as post_file:
            content = post_file.read()
            if skip_marker in content:
                continue
            if date_marker not in content:
                print(post_filename,"has no date - excluding from list")
                continue
            title = inside_first_div(title_marker,content)
            desc = inside_first_div(desc_marker, content)
            date = inside_first_div(date_marker, content)
            try:
                datetime.datetime.strptime(date,"%b %d, %Y")
            except ValueError:
                print(post_filename,"has date written in wrong format - excluding from list")
                continue
            result.append((to_html(title, desc, date, url_path(post_filename)),date))
    #sort newest posts first
    result = reversed(sorted(result, key=lambda x: datetime.datetime.strptime(x[1],"%b %d, %Y")))
    #discard dates after sort
    return list(map(lambda x: x[0], result))
def to_html_list(strings):
    result = "<ul>\n"
    for s in strings:
        result += f"  <li>{s}</li>\n"
    result += "</ul>\n"
    return result
def most_recent_post(posts_dir):
    return all_posts(posts_dir)[0]
def other_recent_posts(posts_dir, how_many):
    all = all_posts(posts_dir)
    if(len(all) <= 1):
        return "None yet! :)"
    return to_html_list(all_posts(posts_dir)[1:how_many+1])
def all_posts_html(posts_dir):
    return to_html_list(all_posts(posts_dir))
