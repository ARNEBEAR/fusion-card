import os
import re

standalone_dir = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'

for root, _, files in os.walk(standalone_dir):
    if '.git' in root or 'node_modules' in root:
        continue
        
    for f in files:
        if f.endswith('.html') or f.endswith('.css'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Determine how many levels deep we are relative to standalone_dir
            rel_dir = os.path.relpath(root, standalone_dir)
            if rel_dir == '.':
                # We are at standalone_dir root
                # The correct path to images is 'assets/images/...'
                # The current wrong path is probably '../assets/images/...'
                # Let's just use regex to replace any (../)*assets/images/ with assets/images/
                # Wait, if there are multiple ../, just replace them all.
                content = re.sub(r'(\.\./)+assets/images/', r'assets/images/', content)
            else:
                # We are in a subdirectory like 'verticals' or 'mini'
                # The correct path is '../assets/images/...'
                # Current wrong path is probably '../../assets/images/...'
                depth = len(rel_dir.split(os.sep))
                correct_prefix = '../' * depth + 'assets/images/'
                content = re.sub(r'(\.\./)+assets/images/', correct_prefix, content)
                
            # One edge case: maybe it was 'assets/images/' without ../ but we still want to make sure it's correct?
            # Actually, `(\.\./)+` requires at least one `../`. What if it's currently `assets/images/`?
            # Let's just normalize all paths to assets/images.
            # Find all `assets/images/...` and `../assets/images/...` and `../../assets/images/...`
            # and replace them with the correct relative path.
            
            # Match `[any number of ../]assets/images/img_XXX.jpg`
            # Replace with `correct_prefix + img_XXX.jpg`
            if rel_dir == '.':
                correct_prefix = 'assets/images/'
            else:
                depth = len(rel_dir.split(os.sep))
                correct_prefix = '../' * depth + 'assets/images/'
                
            # regex: matches optional ../ then assets/images/
            content = re.sub(r'(?:\.\./)*assets/images/', correct_prefix, content)
                
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Fixed paths in {os.path.relpath(filepath, standalone_dir)}")
