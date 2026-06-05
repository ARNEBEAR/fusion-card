import os
import re
import random

BASE_DIR = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/images')

valid_images = [f for f in os.listdir(ASSETS_DIR) if f.endswith('.jpg')]

for root, _, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.css'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            original_content = content
            
            # Find and replace all duplicated native feed images:
            # .v.b1 .pic{background-image:url("...")}
            # Or <div class="pic" style="background-image:url('...')">
            
            # Replace all occurrences of `img_1520250497591-112f2f40a3f4.jpg` with a random image? No, let's just do a blanket regex search for ANY image url and if there are many of the same, replace them.
            # Actually, it's easier to just match ALL `img_[0-9a-f\-]+\.jpg` and keep a history. If we see it more than 2 times, replace it with a random one.
            # Except we want to preserve some logic. Let's just randomize all of them in `.v.b1`, `.v.b2`, `.v.b3`, `.v.b4`.
            
            def replacer(match):
                return match.group(1) + random.choice(valid_images) + match.group(2)

            # Match .v.bX .pic { background-image:url("...") }
            content = re.sub(r'(\.v\.b[1-4]\s*\.pic\s*\{\s*background-image:\s*url\([\'"]?(?:\.\./)*assets/images/)img_[a-zA-Z0-9\-]+\.jpg([\'"]?\)\s*\})', replacer, content)
            
            # Match <div class="pic" style="background-image:url('...')">
            content = re.sub(r'(<div[^>]*class="pic[^>]*style="[^"]*background-image:\s*url\([\'"]?(?:\.\./)*assets/images/)img_[a-zA-Z0-9\-]+\.jpg([\'"]?\)[^"]*"\s*>)', replacer, content)

            # Match <div class="product-card"><div class="photo" style="background-image:url('...')">
            content = re.sub(r'(<div[^>]*class="photo"[^>]*style="[^"]*background-image:\s*url\([\'"]?(?:\.\./)*assets/images/)img_[a-zA-Z0-9\-]+\.jpg([\'"]?\)[^"]*"\s*>)', replacer, content)
            
            # Match <div class="card cX" data-bg="...">
            content = re.sub(r'(<div[^>]*class="card\s+c[0-9]+[^"]*"[^>]*data-bg="[\'"]?(?:\.\./)*assets/images/)img_[a-zA-Z0-9\-]+\.jpg([\'"]?)', replacer, content)
            
            # Match <div class="bg-img" style="background-image:url('...')">
            content = re.sub(r'(<div[^>]*class="bg-img"[^>]*style="[^"]*background-image:\s*url\([\'"]?(?:\.\./)*assets/images/)img_[a-zA-Z0-9\-]+\.jpg([\'"]?\)[^"]*"\s*>)', replacer, content)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Randomized duplicates in {os.path.basename(filepath)}")
