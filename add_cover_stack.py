import os
import re

BASE_DIR = '/Users/bytedance/Desktop/AI/Fusion card design/designs/standalone'

for root, _, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith('.html') and ('s4' in f or 's4' in root):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            original = content
            
            # 1. Update .swipe .card CSS
            # Remove overflow:hidden, background:#222, box-shadow
            content = re.sub(
                r'\.swipe \.card\s*\{[^}]*\}',
                r'.swipe .card{\n    position:relative;flex:0 0 auto;width:240px;aspect-ratio:9/13.5;border-radius:12px;\n    scroll-snap-align:start;cursor:pointer;\n  }',
                content
            )
            
            # 2. Update .swipe .card .bg-img CSS
            # Add border-radius, box-shadow, background-color
            content = re.sub(
                r'\.swipe \.card \.bg-img\s*\{([^}]*)\}',
                r'.swipe .card .bg-img{\1    border-radius:12px;\n    box-shadow:0 6px 18px rgba(0,0,0,.32);\n    background-color:#E2E2E2;\n  }',
                content
            )
            
            # 3. Update .swipe .card::after CSS
            # Add border-radius:12px
            content = re.sub(
                r'\.swipe \.card::after\s*\{([^}]*)\}',
                r'.swipe .card::after{\1    border-radius:12px;\n  }',
                content
            )
            
            # 4. Remove .swipe .card.photo::before if exists
            content = re.sub(r'\.swipe \.card\.photo::before\s*\{[^}]*\}', '', content)
            
            # 5. Add .stack-layer CSS right after .swipe .card::after
            stack_css = r"""
  .swipe .stack-layer {
    position: absolute; inset: 0; border-radius: 12px;
    background: #E2E2E2; z-index: -1;
    border: 1px solid rgba(0,0,0,0.08);
  }
  .swipe .stack-layer.l1 {
    transform: rotate(-3.5deg) translate(-2px, 4px);
    z-index: -1; background: #D1D1D1;
  }
  .swipe .stack-layer.l2 {
    transform: rotate(3deg) translate(2px, 8px);
    z-index: -2; background: #C0C0C0;
    box-shadow: 0 8px 16px rgba(0,0,0,0.25);
  }"""
            if '.stack-layer' not in content:
                content = re.sub(
                    r'(\.swipe \.card::after\s*\{[^}]*\})',
                    r'\1' + stack_css,
                    content
                )
                
            # 6. Update .swipe padding to accommodate shadows
            content = re.sub(
                r'padding:0 12px 4px;',
                r'padding:0 12px 24px;',
                content
            )
            
            # 7. Inject <div class="stack-layer l2"></div><div class="stack-layer l1"></div> into HTML cards
            # We look for `<div class="bg-img"` and replace it
            content = re.sub(
                r'(<div class="bg-img")',
                r'<div class="stack-layer l2"></div><div class="stack-layer l1"></div>\1',
                content
            )
            
            # Since the script might run multiple times, avoid double injecting
            content = content.replace(
                '<div class="stack-layer l2"></div><div class="stack-layer l1"></div><div class="stack-layer l2"></div><div class="stack-layer l1"></div>',
                '<div class="stack-layer l2"></div><div class="stack-layer l1"></div>'
            )
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Added cover stack to {f}")
