# Cursor Rules 规则编写

Cursor 的 Rules 用于定义**编码标准**、**项目约定**、**AI 行为模式**，让 AI 按既定规范生成和修改代码。

## 1. 规则体系演进

- **旧版**：单一 `.cursorrules` 文件
- **新版**：`.cursor/rules/*.mdc`，支持 YAML frontmatter 与动态激活

推荐使用 `.mdc` 格式，便于按领域拆分和维护。

## 2. 目录组织建议

```
.cursor/rules/
├── core.mdc          # 全局规则
├── architecture.mdc  # 架构约束
├── frontend.mdc      # 前端规范
├── backend.mdc       # 后端规范
├── testing.mdc       # 测试规范
└── security.mdc      # 安全规则（优先级最高）
```

按**单一职责**拆分，避免单个文件过大（建议 <500 行）。

## 3. 规则编写原则

| 原则 | 说明 |
|------|------|
| **窄范围** | 用 `apply_when` 限定文件 glob、路径或问题模式 |
| **短指令** | 简短、直接，优先用列表和小示例 |
| **小示例驱动** | 带示例的规则更容易被模型遵守 |
| **优先级** | 用 1–100 控制冲突，安全类规则建议设 100 |

## 4. MDC 结构示例

```yaml
---
description: 前端组件规范
globs: ["**/*.vue", "**/*.tsx"]
alwaysApply: false
---
# 规则内容
- 使用函数组件
- 添加 PropTypes 或 TypeScript 类型
- 包含错误边界
```

## 5. 规则 vs Skills

| 类型 | 作用 |
|------|------|
| **Rules** | 常驻生效，定义风格和约束 |
| **Skills** | 任务型指令，针对特定工作流，按需加载 |

## 6. 常见问题

- **规则不生效**：检查 glob 是否匹配当前文件，以及 Settings → Indexing 是否包含规则目录
- **规则冲突**：通过 priority 控制优先级
- **过于复杂**：拆分规则、减少条件、多用示例

## 7. 参考资料

- [Cursor MDC 规则最佳实践](https://cursor.fan/zh/tutorial/HowTo/mdc-rules-best-practices)
- [Cursor Rules Guide](https://design.dev/guides/cursor-rules/)
