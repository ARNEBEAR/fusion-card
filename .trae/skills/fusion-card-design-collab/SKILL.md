---
name: "fusion-card-design-collab"
description: "TikTok 生服地点精搜融合卡专项 · 设计协作执行手册。包含项目记忆 / 文件结构 / 部署流水线 / 已踩过的坑 / 用户偏好 / 沟通模式。当用户在该项目下提任何"设计还原 / 修改 / 部署 / 跨设备恢复 / 描述文案校准"诉求时立即载入。"
---

# Fusion Card Design Collab · 协作执行手册

> **触发条件**：当用户工作目录是 `/Users/bytedance/Desktop/AI/Fusion card design/` 或讨论的 4 套策略（S1·A 单卡聚合 / S2·A 折叠分层 / S3·A 解耦排版 / S4·A 内容沉浸）时立即载入。

---

## 0 · 项目记忆快照（永远先读这一段）

| 维度 | 状态 |
|---|---|
| **角色** | 用户是 TikTok Local Services 资深 UX/UI 设计师；我是设计还原 + 前端实现执行方 |
| **领域** | POI Exact Search 融合卡 · Hotel 场景 · 4 套差异化策略 |
| **三段结构** | 识别 (Identify) → 理解 (Understand) → 交易 (Transact) |
| **横轴叙事** | commerce-first（最强收口）→ content-first（内容沉浸） |
| **画布** | iPhone 390 × 844，body width 390px，灰底 #F5F5F5 |
| **设计 token** | 全部在 `designs/_shared.css` `:root` 里，**不要硬编码颜色** |
| **代号 → 关键词** | S1=识别即转化 / S2=折叠分层 / S3=解耦排版 / S4=内容沉浸 |
| **永久外链** | `https://arnebear.github.io/fusion-card/` (GitHub Pages, repo: `ARNEBEAR/fusion-card`) |
| **代码同步** | 仅 `designs/standalone/` 目录是 git repo，整个工作目录尚未推 workspace repo |

### 文件拓扑（必须熟记）

```
Fusion card design/
├── index.html                      ← Overview 主分析页（也叫"全局页面"，含 hero/decision matrix/4 iframe）
├── designs/
│   ├── _shared.css                 ← 设计原子（cover/.brand-mark/.av-stack/.date-bar/...）
│   ├── s1-a-hotel-hero-stack.html  ← 源文件 · 完整 iPhone chrome
│   ├── s2-a-hotel-tabbed-card.html
│   ├── s3-a-hotel-modules-split.html
│   ├── s4-a-hotel-video-first.html
│   └── standalone/                 ← Git repo · 已部署到 Pages
│       ├── index.html              ← Landing 页（4 iframe + hero + 横轴）
│       ├── overview.html           ← = 项目根 index.html 的副本，iframe 重指向同目录
│       ├── prototypes/stage-1~4.html  ← lo-fi 线框图
│       └── s1-card.html ~ s4-card.html  ← 内联 _shared.css 后的可分享单页
├── prototypes/                     ← lo-fi 源
└── figma-refs/                     ← 设计参考截图
```

---

## 1 · 关键 Lessons Learned（每条都用真实代价换的）

### 1.1 部署链路坑

- **GitHub Push Protection 会拦 Mapbox demo token**（pk.eyJ1IjoibWFwYm94...）
  - 即使是公开 demo token 也会被拦
  - 解决：替换为 unsplash 图，或在 `_shared.css` 里彻底移除
- **GitHub Pages 部署延迟 30~60 秒**，需 `sleep 50 && curl` 探活
- **CDN 缓存**导致用户看到旧版本 → 提醒用户 `⌘+Shift+R` 强制刷新
- **Push 凭据**：用 GitHub PAT（用户名 `ARNEBEAR` + token），或改 SSH remote
- **不要污染全局 git config**：每次 commit 都用 `git -c user.email="arnebear@users.noreply.github.com" -c user.name="ARNEBEAR" commit`

### 1.2 standalone 文件再生成的标准流程

```bash
# 改源文件 → 重新生成 4 个 standalone（保留完整 iPhone chrome + 内联 _shared.css）
python3 <<'PY'
from pathlib import Path
root = Path("/Users/bytedance/Desktop/AI/Fusion card design/designs")
out_dir = root / "standalone"
shared_css = (root / "_shared.css").read_text(encoding="utf-8")
mapping = {
  "s1-card.html": "s1-a-hotel-hero-stack.html",
  "s2-card.html": "s2-a-hotel-tabbed-card.html",
  "s3-card.html": "s3-a-hotel-modules-split.html",
  "s4-card.html": "s4-a-hotel-video-first.html",
}
override = """
html{background:#0a0a0b;min-height:100vh}
body{background:#0a0a0b !important;width:auto !important;min-height:100vh !important;display:flex;align-items:center;justify-content:center;padding:24px 0 !important}
.iphone{flex:0 0 auto;width:390px !important;height:844px !important;border-radius:42px !important;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55),0 12px 28px rgba(0,0,0,.4),0 0 0 1px rgba(255,255,255,.04),inset 0 0 0 1px rgba(255,255,255,.04) !important}
.iphone .ios{border-radius:42px !important;overflow:hidden}
"""
for o, s in mapping.items():
    src = (root/s).read_text(encoding="utf-8")
    inlined = src.replace('<link rel="stylesheet" href="_shared.css">', f'<style>\n{shared_css}\n</style>')
    inlined = inlined.replace("</style>", override + "\n</style>", 1)
    (out_dir/o).write_text(inlined, encoding="utf-8")
PY

cd "designs/standalone" && \
  git add . && \
  git -c user.email="arnebear@users.noreply.github.com" -c user.name="ARNEBEAR" commit -m "<msg>" && \
  git push
```

### 1.3 高保真设计还原的硬性要求（用户多次校准过的偏好）

1. **用户指 "完整界面"** = iPhone chrome 全保留（statusbar / searchbar / tabs / 卡片 / native feed）
   不是只有卡片！第一次我误删 chrome，被纠正过
2. **用户指 "可互动"** = 所有 JS 交互保留：tab 切换 / see-more 展开 / Ken Burns 自动播放 / 横滑 dots 联动
3. **画布永远 390×844** —— body 必须 `width:390px;margin:0 auto`
4. **margin 不要 shorthand**，要用 4 值，避免 IDE 自动重排破坏布局
5. **图片永远用 unsplash + auto=format&fit=crop&w=*&q=80** 格式，不要换源（会破坏色调）
6. **bleed-edge 设计**：`.cover` 不要加圆角，让图贴边

### 1.4 描述文案校准的"硬规则"

每条策略的描述必须做到：
- ✅ **直接对应到具体实现元素**（"16:9 banner" / "4 段 segment" / "9:13 视频" / "白色聚合卡"）
- ✅ **点出与其它策略的差异化**（不只是描述自己，是描述"为什么是这个策略"）
- ✅ **用核心动词收尾**（收口 / 折叠 / 解耦 / 沉浸 ←→ 横轴叙事）
- ❌ 不要写"沿用 S1 的识别头" —— 实现一旦改动，这种相对描述会立即失效
- ❌ 不要漏掉 S1 的"原声"、S4 的"UGC ↔ Official 切换"等核心差异化元素

每次改完源文件 → **同步更新 `index.html` 和 `overview.html`** 里的对应描述，否则会"实现 vs. 文案"漂移。

---

## 2 · 用户表述模式（识别 → 翻译）

| 用户原话 | 真正意图 | 我应该做什么 |
|---|---|---|
| "去掉吧，太突兀了" | 删除该 UI 元素，且一并清理孤立 CSS | SearchReplace 删 markup + 检查 CSS 是否有遗留 |
| "搞好看点" | 不是开放式探索，是"按你专业判断升级视觉" | 加大字号 / 加渐变 / 加阴影 / 用 SF Pro Display；**不要问用户**，直接做 |
| "再视觉化一点" / "有 X 的感觉" | 现在的形态太抽象/太文字 → 要图形化、节点化、轨道化 | 用 timeline / track / dots / gradient 替代纯色块 |
| "校准/精准/精简" | 描述与实现错位 → 全文逐句对照实现修正 | 先列出"实际实现 vs. 当前文案"对照表再改 |
| "我可能后面要随时唤出来" | 保留资产 + 提供持久化访问 | 部署到永久外链 + 保留所有历史版本 |
| "直接搞" / "执行" | 已批准，立即跑命令 | 不再追问，直接执行 |
| "我成功了，但是效果有问题" | 大方向 OK，需要回退一步重做细节 | 不要从零开始，找到"哪里偏离原意" |
| 给截图 | 截图就是 ground truth，对照截图改 | 先描述截图里看到了什么，再说怎么改 |

---

## 3 · 我（AI）的常见执行问题（自我警示）

### 3.1 "假理解"的高频场景
- **简化没说要简化的东西**：例如第一次把 standalone 误读为"只要卡，删掉 chrome"。**永远默认"完整保留"**，除非用户明确说"只要卡片本身"
- **过度发明术语**：用 "Stage 1/2/3/4" 而用户已说要 "策略 1/2/3/4"。**沿用用户的命名，不要自创**
- **改完源文件忘记同步 standalone**：必须每次 git push 前都跑 `python3` 再生成脚本

### 3.2 工具调用纪律
- **Skill 触发**：每次用户消息开头都要先扫一遍 available_skills，相关就立即调用
- **并行调用**：读多个文件 / 多个 grep 时永远在同一个响应里并行发起
- **不要 `Read` 整个文件**：除非明确需要，否则只读相关行段（`offset` + `limit`）
- **commit message** 用 conventional 格式：`feat(s2):` / `fix:` / `docs:` / `tweak(s2):`
- **永远不要主动 commit**：除非用户说"提交 / push / 上传"

### 3.3 沟通节奏
- **少用 emoji**：用户从未在自己消息里用 emoji，我的回复也应当克制
- **不要重复前文**：用户能滚屏看到，避免把"修改总结"写得过于冗长
- **代码引用用 `[文件名](file://...)`**：用户偏好可点击的引用
- **响应语言跟随用户**：用户说中文我说中文（除非他贴英文 paragraph 才切英文）
- **不要"假问"**：用户给了足够上下文就直接做，别为了显示谨慎而每次都问选择

### 3.4 视觉判断的常见失误
- **比例**：4:3 在 390 宽 = 292px，**偏高**；16:9 = 219px 才是 banner 感
- **大标题字号**：landing 页 hero 至少 60-84px，不要 24px（被用户吐槽过"太小不好看"）
- **横轴/timeline**：用户说"视觉化" = 要轨道（gradient track）+ 节点（带光晕的 dots），不是 4 个并排的 box
- **导航行**：用户嫌弃过"那一整行 chip 导航太突兀" → 默认用极简文字链接放 footer

---

## 4 · 协作动作清单（用户每个意图对应的执行模板）

### 4.1 "改 SX 的某部分" 模板
```
1. SearchCodebase / Grep 定位源文件（s{N}-a-*.html）和 _shared.css
2. SearchReplace 改源文件
3. 跑 standalone 再生成脚本（见 §1.2）
4. 检查 index.html / overview.html 是否需要同步描述
5. git add . && commit -m "feat(s{N}): <change>" && push
6. 等 50s + curl 探活
7. 给用户：单独链接 + 总览链接 + ⌘+Shift+R 提示
```

### 4.2 "校准描述文案" 模板
```
1. 列出"实际实现 vs. 当前文案"对照表（文字版）
2. 逐条标记 ❌ 不准确 / ✅ 已准确
3. SearchReplace 修正每个 ❌
4. 同步 index.html + overview.html + decision matrix
5. push
```

### 4.3 "新增视觉元素" 模板
- **不要只用 CSS box**，优先用 SVG / gradient / pseudo-element
- **颜色用 HSL 渐变**：粉 #fe2c55 / #ff7898 → 紫 #a59bff → 蓝 #5b9eff（已建立的策略色谱）
- **必须有阴影或光晕**：`box-shadow:0 0 24px rgba(<accent>,.4)` 是基本款
- **mono 字体**用 SF Mono 给 label / meta，display 字体用 SF Pro Display 给 hero

---

## 5 · 跨设备恢复 onboarding（粘到新 Trae 第一条消息即可）

```
我是 TikTok Local Services 资深 UX/UI 设计师。
项目：POI Exact Search 融合卡 · Hotel 场景 · 4 套策略。
工作目录：/Users/bytedance/Desktop/AI/Fusion card design/
请先 @SKILL.md（如果有）/ 读 .trae/skills/fusion-card-design-collab/SKILL.md，
然后我们继续 [当前任务]。
```

---

## 6 · 已交付清单（防止重复劳动）

- [x] S1·A 完整 iPhone HTML（带 native feed）
- [x] S2·A 完整 iPhone HTML（**16:9 banner 识别头** + 4 段 segment + native feed）
- [x] S3·A 完整 iPhone HTML（4 张独立 mod + native feed）
- [x] S4·A 完整 iPhone HTML（9:13 横滑视频 + UGC↔Official + 反挂载 mount）
- [x] Standalone × 4（内联 CSS 可单独分享 / 飞书贴）
- [x] Landing 页（hero + 横轴 timeline + 4 iframe + 描述）
- [x] Overview 完整文字分析页（4 列 + decision matrix）
- [x] Lo-fi prototypes（stage-1 ~ 4）
- [x] GitHub Pages 部署（`https://arnebear.github.io/fusion-card/`）
- [ ] Workspace 整目录 private repo 同步（待用户决定）
- [ ] 字体本地化 / Inter 字体内嵌（如有外网封禁场景）

---

## 7 · 我会对自己反复 grep 的关键词（防止重复犯错）

每次开工前在脑子里 grep：
- `voice` → S1 还有原声块 / S2 已删
- `aspect-ratio` → S2 hero=16/9, S4 swipe card=9/13
- `cover.hotel-night` → S2 banner 用的就是这张夜景
- `_shared.css` → 改这个会影响 4 个 standalone，必须重新生成
- `iphone` 类 → 完整 chrome 标识，**不能删**
- `Stage` 字符串 → 用户已淘汰这个词，应该是"策略 N"

---

## 8 · 当用户的需求与我的判断冲突时

**优先级**：
1. 用户明确指令 ＞ 我对设计的偏好
2. 用户既定的命名（如"策略 N"）＞ 业内通用术语
3. 已经迭代多轮的现状（如 S2 banner）＞ 历史描述里的旧表述
4. 实际实现 ＞ 文案描述（描述要追实现，不是反过来）

**永远不要**：擅自加 emoji / 自创策略名 / 跳过 standalone 再生成 / 直接 push 不验证 / 修改文件不同步描述
