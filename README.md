# weekly_topic

每周牵引自己完成一个特定主题的学习总结 → HTML 精读总结 + SVG 知识脉络图 → GitHub Pages。

结构对齐 [video-notes](https://github.com/czh55/video-notes)：`docs/` 为站点根目录，`index.json` 驱动首页时间线。

## 结构

```
weekly_topic/
├── .cursor/automations/     # Cursor Automation trigger + 完整 prompt
├── docs/                    # GitHub Pages 根目录
│   ├── index.html           # 每周主题墙
│   ├── index.json           # 周条目索引
│   ├── style.css
│   ├── .nojekyll
│   ├── archive/             # 可选归档
│   ├── *-总结.html
│   └── *-知识图.svg
├── scripts/generate.py      # 校验 / 排序 index.json
├── templates/week.html      # 周总结 HTML 骨架
├── data/config.json
├── .github/workflows/deploy-pages.yml
└── README.md
```

## 本地预览

```bash
cd ~/Projects/weekly_topic
python3 scripts/generate.py --check
python3 -m http.server 8080 --directory docs
# 打开 http://localhost:8080
```

## 新增一周

1. 写 `docs/{slug}-总结.html` 与 `docs/{slug}-知识图.svg`
2. 在 `docs/index.json` 插入条目（字段见下方）
3. 运行 `python3 scripts/generate.py --write`
4. 提交并推送到 `main`（Actions 会部署 Pages）

### index.json 条目

```json
{
  "week": "2026-W42",
  "date": "2026-10-13",
  "title": "主题标题",
  "summary": "一句话摘要",
  "tags": ["标签"],
  "slug": "my-topic",
  "outputs": {
    "html": "my-topic-总结.html",
    "svg": "my-topic-知识图.svg"
  }
}
```

## GitHub Pages

本仓库使用 **GitHub Actions** 部署 `docs/`（与 `daily-design` / `daily-lyric-learning` 相同）。

首次打通：

1. 创建 GitHub 仓库 `czh55/weekly_topic` 并推送 `main`
2. Settings → Pages → Build and deployment → Source 选 **GitHub Actions**
3. 访问：`https://czh55.github.io/weekly_topic/`

若已使用自定义域名 `chenzhiheng.cn`，可在个人站点仓库增加 `/weekly_topic/` 反向代理或子路径挂载（与其他子项目一致）。

## Automation（可选）

Cursor Automation 编辑器 prompt 填入：

```text
读取 .cursor/automations/weekly-prompt.md 并严格执行其中的所有步骤。
```

完整逻辑见 `.cursor/automations/weekly-prompt.md`。
