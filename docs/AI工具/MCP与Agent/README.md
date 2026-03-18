# MCP 与 Agent

MCP（Model Context Protocol）与 Agent 的关系与协同方式。

## 1. 概念区分

| 概念 | 定义 |
|------|------|
| **Prompt** | 最初级人机接口，分 system / user prompt |
| **Agent** | 从问答升级为自主执行：拆任务、调工具、多轮迭代 |
| **Agent Skills** | 可复用的工作流包，固化经验与流程 |
| **MCP** | 统一协议，让 AI 安全、标准化地接入外部工具和资源 |

## 2. MCP 的作用

- 提供**标准化**的工具接入协议（JSON-RPC 2.0）
- 解决「能不能做」—— 连接数据库、API、文件系统等
- 支持多服务编排，一个 Skill 可调用多个 MCP

## 3. Skills 与 MCP 协同

```
用户请求 → Agent 选择 Skill → Skill 编排 MCP 调用 → 返回结果
```

- **MCP**：提供「能做」的能力（读写、查询、调用等）
- **Skills**：规定「怎么稳定做对」的流程与约束

## 4. 工程化思路

1. **定义 Skill 边界**：单职责，复杂任务拆分为多 Skill
2. **接入 MCP**：将 Skills 注册到 MCP，处理并发、重试、熔断
3. **版本与安全**：对 Skill 做版本管理、依赖与权限控制

## 5. 参考资料

- [Prompt、Agent、MCP 和 Skills：大模型时代的工具栈](https://www.mornai.cn/news/ai-agent/prompt-agent-mcp-and-skills/)
- [Agent Skills 究竟是什么？](https://developer.aliyun.com/article/1711574)
