import os
import re

BASE_DIR = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'

targets = ['verticals/s3-mall.html','verticals/s3-fnb.html','verticals/s3-attraction.html']

for rel in targets:
    path=os.path.join(BASE_DIR,rel)
    with open(path,'r',encoding='utf-8') as f: c=f.read()
    orig=c
    # wrap each `<div class="clip..." style=...>...</div>` with a clip-stack wrapper
    def wrap(m):
        inner=m.group(0)
        return ('<div class="clip-stack"><div class="stack-layer l2"></div>'
                '<div class="stack-layer l1"></div>'+inner+'</div>')
    # match the clip div line (clip with style attr), non-greedy until its closing </div>
    c=re.sub(r'<div class="clip(?: photo)?" style="[^"]*">(?:(?!</div>).)*?</span><span class="like">[^<]*</span></div>',
             wrap, c)
    if c!=orig:
        with open(path,'w',encoding='utf-8') as f: f.write(c)
        print('wrapped clips in', rel)
    else:
        print('NO CHANGE', rel)
