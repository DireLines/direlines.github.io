#used by build script to generate html for list of all posts
from pathlib import Path
import os
import datetime
from datetime import date

def all_files_of_types(filetypes, path=''):
    result = []
    for filetype in filetypes:
        result.extend(Path(path).rglob('*.'+filetype))
    return result

def to_html(title, desc, date, link):
    maybe_desc = f' - {desc}' if desc != "" else ""
    return f'{date}: <a href="{link}">{title}</a>{maybe_desc}'

def inside_first_div(div,text):
    div_start = text.find('>',text.find(div))+1
    div_end = text.find('<',div_start)
    return text[div_start:div_end]

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

    date_fmt = "%b %d, %Y"
    
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
            date_text = inside_first_div(date_marker, content)
            try:
                datetime.datetime.strptime(date_text, date_fmt)
            except ValueError:
                today = date.today().strftime(date_fmt)
                content = content.replace(
                    f'<div class="date">{date_text}</div>', 
                    f'<div class="date">{today}</div>')
                date_text = today
                with open(post_filename, 'w') as f:
                    f.write(content)
                print(f'added date {today} to {post_filename}')
            result.append((to_html(title, desc, date_text, url_path(post_filename)),date_text,title))
    #sort newest posts first, then alphabetically for posts published on the same day
    result = reversed(sorted(result, key=lambda x: x[2]))
    result = reversed(sorted(result, key=lambda x: datetime.datetime.strptime(x[1], date_fmt)))
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
