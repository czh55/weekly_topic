# weekly_topic 执行规范

权威流程：每周一个主题，双轨产出，索引上墙。

## 产物

| 文件 | 必须 | 说明 |
|------|:----:|------|
| `docs/{slug}-总结.html` | ✅ | 问题 / 结论 / 证据 / 边界 / 行动 |
| `docs/{slug}-知识图.svg` | ✅ | 关系图 + 对比 + 坑点 + 行动 |
| `docs/index.json` 条目 | ✅ | 首页卡片数据源 |

## 命名

- `slug`：小写英文/数字/连字符，如 `attention-budget`
- HTML：`{slug}-总结.html`
- SVG：`{slug}-知识图.svg`
- `week`：ISO 周，如 `2026-W42`

## 发布检查

```bash
python3 scripts/generate.py --write
python3 -m http.server 8080 --directory docs
```

推送到 `main` 后由 Actions 部署 Pages。
