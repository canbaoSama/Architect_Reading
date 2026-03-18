# Skills 分类说明

Skills 已按功能分类存放于子文件夹，便于查找与智能体配置。

## 分类目录

| 目录 | 说明 | 数量 |
|------|------|------|
| `orchestration/` | 主智能体/编排：任务分派、知识管理、多智能体协同 | ~14 |
| `requirements/` | 需求分析：深度研究、文档协作、数据与竞品分析 | ~18 |
| `coding/` | 编码：Git、框架、API、前后端最佳实践 | ~56 |
| `devops/` | 运维：部署、CI/CD、备份、定时、自动化 | ~20 |
| `testing/` | 测试：Playwright、Vue 测试、安全审查 | ~13 |
| `productivity/` | 日常/生产力：任务、日历、邮件、笔记、协作 | ~41 |
| `search/` | 搜索/研究：多引擎搜索、金融数据 | ~22 |
| `docs-content/` | 文档/内容：PPT、PDF、Excel、写作 | ~24 |
| `skill-mgmt/` | 技能管理：安全审核、Skill 创建与发布 | ~10 |
| `other/` | 其他：浏览器、记忆、图像、未明确分类 | ~139 |

## 使用方式

Cursor/Claw 等工具通常从扁平目录加载 Skills。若需保持扁平结构，可：

- 使用符号链接或复制脚本将子目录内容展平
- 或在工具配置中指定多个搜索路径（如 `AI/skills/coding`, `AI/skills/productivity`）

## 分类脚本

`_categorize.py` 用于按映射重新分类。修改 `CATEGORY_MAP` 后运行：

```bash
python3 _categorize.py
```
