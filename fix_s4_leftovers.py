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
            
            # Remove any left-over static card elements:
            # <span class="dur">...</span>
            # <span class="sound"...></span>
            # <div class="play">...</div>
            
            content = re.sub(
                r'<span class="dur">[^<]*</span>\s*(?:<span class="sound"[^>]*>.*?</span>\s*)?<div class="play">.*?</svg></div>',
                album_svg,
                content,
                flags=re.DOTALL
            )
            
            # Clean up left over toggle listeners in scroll event
            content = re.sub(
                r"const mode=document\.querySelector\('\.toggle \.seg\.on'\)\?\.dataset\.mode\|\|'ugc';\s*const data=sets\[mode\];",
                r"const data=sets.ugc;",
                content
            )
            
            # Clean up left over "胶囊切换" block
            content = re.sub(r'// 胶囊切换.*?(?=\Z|//)', '', content, flags=re.DOTALL)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed remaining elements in {f}")
