# Cursor Agent Skills 技能创建

Agent Skills 是可复用的**工作流包**，把经验、流程、规则沉淀成标准化能力，供 AI 在特定任务中按需加载。

## 1. Skills 与 Rules 的区别

| 维度 | Rules | Skills |
|------|-------|--------|
| 作用 | 常驻约束、风格与规范 | 任务型、流程固化 |
| 加载 | 按文件/路径自动加载 | 按任务需求调用 |
| 内容 | 简短指令、示例 | 工作流步骤、配置、脚本 |

## 2. 标准 Skills 目录结构

```
skill-name/
├── SKILL.md        # 自描述指令 + 工作流步骤
├── config.yaml     # 硬约束与参数
├── scripts/        # 确定性脚本（Python/Shell）
└── references/     # 模板、规范、示例
```

- **SKILL.md**：自然语言描述技能目标与步骤
- **config.yaml**：参数、约束、阈值
- **scripts/**：可执行的辅助脚本
- **references/**：示例、模板、文档

## 3. Skills 与 MCP 的协同

| 维度 | MCP | Agent Skills |
|------|-----|--------------|
| 功能 | 连接协议、工具接入 | 流程固化、工作标准 |
| 解决的问题 | 「能不能做」—— 外部系统接入 | 「怎么稳定做对」—— 流程复用 |
| 通信 | JSON-RPC 2.0 | SKILL.md + config |

一个 Skill 可以编排多个 MCP 服务；MCP 提供能力，Skills 规定用法。

## 4. 工程化落地建议

1. **边界清晰**：单一职责，复杂任务拆成多个 Skill
2. **标准化描述**：尽量用 JSON Schema，减少自然语言歧义
3. **MCP 接入**：将 Skills 注册到 MCP，处理并发、重试、熔断
4. **版本与安全**：像微服务一样管理技能迭代、依赖与权限

## 5. 参考资料

- [Agent Skills 与 MCP 选型指南](https://claw.csdn.net/69b3fe860a2f6a37c597111e.html)
- [Prompt、Skill、Agent、MCP 区别](https://developer.aliyun.com/article/1714690)
