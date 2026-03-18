# AI 工具栈

AI 辅助编程相关文档，涵盖 Cursor IDE 规则与技能、Prompt 工程、MCP 与 Agent 等。

## 四层工具栈关系（2025）

| 层级 | 概念 | 作用 |
|------|------|------|
| **Prompt** | 人机接口 | System prompt（角色/风格）+ User prompt（具体任务） |
| **Agent** | 自主执行 | 拆分任务、调用工具、多轮迭代 |
| **Agent Skills** | 可复用工作流 | 将经验、流程、规则沉淀为标准能力包 |
| **MCP** | 模型上下文协议 | 统一、安全地接入外部工具与资源 |

> Prompt 是起点，Agent 是升级，Skills 固化流程，MCP 提供接入能力。

## 模块导航

- **[Cursor Rules](./Cursor/Rules规则编写.md)**：`.mdc` 规则、`apply_when`、最佳实践
- **[Cursor Skills](./Cursor/Skills技能创建.md)**：Agent Skills 目录结构与编写规范
- **[Prompt 工程](./Prompt工程/结构化Prompt.md)**：结构化 Prompt、常用技巧、模板
- **[MCP 与 Agent](./MCP与Agent/README.md)**：MCP 协议、Skills 与 MCP 协同
