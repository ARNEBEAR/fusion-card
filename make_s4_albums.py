import os
import re

BASE_DIR = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'

album_svg = r'<div class="album-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 6h2v14H4zm4-2h2v16H8zm4-2h8v18h-8z"/></svg> <span style="font-size:12px;font-weight:bold;margin-left:4px">Album</span></div>'

for root, _, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith('.html') and ('s4' in f or 's4' in root):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            original = content
            
            # Remove toggle wrap
            content = re.sub(r'<div class="toggle-wrap">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
            
            # Change renderSwipe JS logic
            # from: renderSwipe(mode) { const data=sets[mode];
            # to: renderSwipe() { const data=sets.ugc; data[0].badge="Official"; data[0].album=true; for(let i=1;i<data.length;i++) data[i].album=true;
            
            content = re.sub(
                r'function renderSwipe\(mode\)\s*\{\s*const data=sets\[mode\];', 
                r'function renderSwipe(){\n    const data=sets.ugc;\n    data[0].badge = "Official";',
                content
            )
            
            # Change JS template
            # find the block:
            # <span class="dur">${d.dur}</span>
            # <span class="sound" data-sound="on">${SOUND_ON_SVG}${SOUND_OFF_SVG}</span>
            # <div class="play"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></div>
            # <div class="progress"></div>
            # Replace it with album_svg
            
            content = re.sub(
                r'<span class="dur">\$\{d\.dur\}</span>\s*<span class="sound".*?</svg></div>\s*<div class="progress"></div>',
                album_svg,
                content,
                flags=re.DOTALL
            )
            
            # Change the hardcoded static cards in the HTML:
            # They have `<span class="dur">...</span>`, `<div class="play">...</div>`, maybe no sound or progress in static HTML.
            content = re.sub(
                r'<span class="dur">[^<]*</span>\s*<div class="play">.*?</svg></div>',
                album_svg,
                content,
                flags=re.DOTALL
            )
            
            # Change badge class from `${mode==='ugc'?'brand':''}` to `${i===0?'brand':''}`
            content = content.replace("${mode==='ugc'?'brand':''}", "${i===0?'brand':''}")
            
            # Also update static cards to have Official badge for first one
            content = content.replace('<span class="badge brand">Updated recently</span>', '<span class="badge brand">Official</span>')
            
            # Change initialization
            content = content.replace("renderSwipe('ugc')", "renderSwipe()")
            content = content.replace('renderSwipe("ugc")', 'renderSwipe()')
            
            # Remove JS toggle listener
            content = re.sub(r'// 胶囊切换.*?(// view details 跳详情)', r'\1', content, flags=re.DOTALL)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated S4 to album mode: {f}")
