import os
import re

BASE_DIR = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'

s2_files = ['s2-a-hotel-tabbed-card.html','s2-card.html',
            'verticals/s2-attraction.html','verticals/s2-fnb.html','verticals/s2-mall.html']
s3_files = ['s3-a-hotel-modules-split.html','s3-card.html',
            'verticals/s3-attraction.html','verticals/s3-fnb.html','verticals/s3-mall.html']

S2_STACK_CSS = """
  /* cover-stack（专辑堆叠感，与 S4 一致） */
  .says-card .stack-layer{position:absolute;top:0;left:0;width:100%;aspect-ratio:3/4;border-radius:8px;z-index:-1;background:#D6D6D6;border:1px solid rgba(0,0,0,.05)}
  .says-card .stack-layer.l1{transform:rotate(-3deg) translate(-2px,3px);background:#D6D6D6}
  .says-card .stack-layer.l2{transform:rotate(2.6deg) translate(2px,7px);background:#C9C9C9;box-shadow:0 8px 14px rgba(0,0,0,.18)}
  .says-card{padding-bottom:2px}
"""

S3_STACK_CSS = """
  /* cover-stack（专辑堆叠感，与 S4 一致） */
  .m-rev .clip-stack{position:relative;flex:0 0 auto;width:160px;aspect-ratio:3/4;scroll-snap-align:start}
  .m-rev .clip-stack .clip{width:100%;height:100%;flex:0 0 auto}
  .m-rev .clip-stack .stack-layer{position:absolute;top:0;left:0;width:100%;height:100%;border-radius:8px;z-index:-1;background:#D6D6D6;border:1px solid rgba(0,0,0,.05)}
  .m-rev .clip-stack .stack-layer.l1{transform:rotate(-3deg) translate(-2px,3px);background:#D6D6D6}
  .m-rev .clip-stack .stack-layer.l2{transform:rotate(2.6deg) translate(2px,7px);background:#C9C9C9;box-shadow:0 8px 14px rgba(0,0,0,.18)}
"""

def process_s2(path):
    with open(path,'r',encoding='utf-8') as f: c=f.read()
    orig=c
    # inject CSS once, right after the `.says-card{...}` base rule
    if '.says-card .stack-layer' not in c:
        c=re.sub(r'(\.says-card\{flex:0 0 auto;width:160px;scroll-snap-align:start;cursor:pointer;position:relative\})',
                 r'\1'+S2_STACK_CSS, c, count=1)
    # give rail bottom room so rotated layers aren't clipped
    c=c.replace('padding:10px 0 6px 14px;margin:0 -14px;scroll-padding-left:14px;',
                'padding:10px 0 14px 14px;margin:0 -14px;scroll-padding-left:14px;')
    # inject stack layers as first children of each says-card (JS template + static)
    # JS template line:
    c=re.sub(r'(<div class="says-card" data-topic="\$\{d\.topic\}">)(?!\s*<div class="stack-layer)',
             r'\1<div class="stack-layer l2"></div><div class="stack-layer l1"></div>', c)
    # static says-card (no data-topic or different) — generic
    c=re.sub(r'(<div class="says-card"[^>]*>)(?!\s*<div class="stack-layer)(\s*<div class="pic")',
             r'\1<div class="stack-layer l2"></div><div class="stack-layer l1"></div>\2', c)
    if c!=orig:
        with open(path,'w',encoding='utf-8') as f: f.write(c)
        print('S2 stacked:', os.path.relpath(path,BASE_DIR))
    else:
        print('S2 no change:', os.path.relpath(path,BASE_DIR))

def process_s3(path):
    with open(path,'r',encoding='utf-8') as f: c=f.read()
    orig=c
    if '.clip-stack' not in c:
        # inject CSS after `.m-rev .clip{...}` base rule
        c=re.sub(r'(\.m-rev \.clip\{[^}]*\})', r'\1'+S3_STACK_CSS, c, count=1)
    # bottom room for rail
    c=c.replace('padding:0 0 4px 14px;margin:12px -14px 0 -14px;',
                'padding:0 0 14px 14px;margin:12px -14px 0 -14px;')
    # wrap each clip element with clip-stack (avoid double-wrapping)
    def wrap(m):
        return ('<div class="clip-stack"><div class="stack-layer l2"></div>'
                '<div class="stack-layer l1"></div>'
                '<div class="clip '+m.group(1)+'">'+m.group(2)+'</div></div>')
    c=re.sub(r'(?<!stack">)<div class="clip ([^"]*)">((?:(?!</div>).)*?)</div>', wrap, c)
    if c!=orig:
        with open(path,'w',encoding='utf-8') as f: f.write(c)
        print('S3 stacked:', os.path.relpath(path,BASE_DIR))
    else:
        print('S3 no change:', os.path.relpath(path,BASE_DIR))

for rel in s2_files:
    process_s2(os.path.join(BASE_DIR,rel))
for rel in s3_files:
    process_s3(os.path.join(BASE_DIR,rel))
