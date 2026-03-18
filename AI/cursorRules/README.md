# Cursor Rules

本目录包含 Cursor IDE 的 Rules 配置，来源于 [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) 等热门仓库，已转换为 `.mdc` 格式。

## 规则列表

| 文件 | 说明 | 触发方式 |
|------|------|----------|
| `core-coding.mdc` | 核心编码规范（DRY、SOLID、最小改动） | 始终应用 |
| `project-structure.mdc` | Vue/Vite 项目结构规范 | 始终应用 |
| `git-commits.mdc` | Conventional Commits 规范 | 编写 commit 时 |
| `typescript-quality.mdc` | TS/JS 代码质量 | \*.ts, \*.tsx, \*.js, \*.vue |
| `vue-composition.mdc` | Vue 3 Composition API | \*.vue |
| `react-nextjs.mdc` | React / Next.js 组件 | \*.tsx, \*.jsx |
| `python-fastapi.mdc` | Python FastAPI 后端 | \*.py |
| `markdown-docs.mdc` | Markdown 文档规范 | \*.md, docs/\*\* |

## 使用方式

Cursor 默认从 `.cursor/rules/` 读取规则。若要让 Cursor 使用本目录的规则，可：

1. **建立软链接**：`ln -sf ../../AI/rules .cursor/rules`（在项目根目录下执行）
2. **复制到 .cursor**：`cp -r AI/rules/* .cursor/rules/`

## 来源

- [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)（38k+ stars）
- [survivorforge/cursor-rules](https://github.com/survivorforge/cursor-rules)
