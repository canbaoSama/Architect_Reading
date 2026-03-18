# Skills 功能清单与智能体配置

本文档列出 `AI/skills/` 下每个 Skill 的功能，并按常用智能体类型推荐适用 Skills。

**目录结构**：Skills 已按分类存放于子文件夹：`orchestration/`、`requirements/`、`coding/`、`devops/`、`testing/`、`productivity/`、`search/`、`docs-content/`、`skill-mgmt/`、`other/`。详见 [AI/skills/README.md](./skills/README.md)。

---

## 一、Skills 功能清单

### 1. 主智能体 / 编排类

| Skill | 功能说明 |
|-------|----------|
| `proactive-agent` | 将 AI 从任务执行者转变为主动伙伴：WAL 协议、工作缓冲区、自主定时任务 |
| `dispatching-parallel-agents` | 面对 2+ 个可并行执行的任务时，分派给多个智能体协同工作 |
| `agent-team-orchestration` | 多智能体任务编排与协同 |
| `swarmclaw` | 管理 SwarmClaw 智能体舰队：创建任务、分配、查看状态、触发工作流 |
| `byterover` | 知识管理，用 `brv` 存储与检索项目模式、决策、架构规则（.brv/context-tree） |
| `remembering-conversations` | 在对话历史中检索过往探索、解决方案与工作流 |
| `session-logs` | 用 jq 搜索与分析自己的会话日志 |

### 2. 需求分析类

| Skill | 功能说明 |
|-------|----------|
| `deep-research-pro` | 多源深度研究：检索、综合、输出带引用的报告，无需 API Key |
| `academic-deep-research` | 学术向深度研究 |
| `doc-coauthoring` | 协作撰写文档、提案、技术规格、决策文档的结构化工作流 |
| `writing-plans` | 有规格或需求后，在执行多步骤任务前先写计划 |
| `breakdown-feature-implementation` | 根据 Epoch monorepo 结构拆解功能实现计划 |
| `executing-plans` | 在有书面实现计划时，在独立会话中按检查点执行 |
| `data-analysis` | 数据驱动决策：统计、方法论、常见分析陷阱 |
| `competitor-alternatives` | 竞品对比/替代方案页面的 SEO 与销售支持 |
| `offer-positioning-auditor` | 审核产品/服务定位：清晰度、差异化、购买摩擦 |
| `pricing-strategy` | 定价策略、套餐设计、变现研究 |
| `marketing-psychology` | 营销中的心理、心智模型、行为科学 |

### 3. 编码类

| Skill | 功能说明 |
|-------|----------|
| `code` | 编码工作流：规划、实现、验证、测试 |
| `git` | 版本控制：基础命令、工作流、分支策略、恢复 |
| `github` | 通过 `gh` CLI 操作 GitHub：issues、PRs、CI、API 查询 |
| `api-design-principles` | API 设计原则与最佳实践 |
| `nodejs-backend-patterns` | Node.js 后端模式：Express/Fastify、中间件、鉴权、数据库 |
| `next-best-practices` | Next.js 最佳实践：RSC、数据模式、路由、优化 |
| `vercel-react-best-practices` | Vercel 推荐的 React/Next.js 性能优化 |
| `vercel-composition-patterns` | Vercel 组合模式 |
| `vue-jsx-best-practices` | Vue 中 JSX 语法与配置 |
| `vue-router-best-practices` | Vue Router 最佳实践 |
| `pinia` | Vue 状态管理：Pinia 官方用法 |
| `react-doctor` | React 项目修改后的快速健康检查 |
| `react-state-management` | React 状态管理 |
| `typescript-advanced-types` | TypeScript 高级类型 |
| `web-component-design` | React/Vue/Svelte 组件模式、CSS-in-JS、可复用架构 |
| `frontend-design-ultimate` | 用 React + Tailwind + shadcn/ui 构建高质量静态站 |
| `vitepress` | VitePress 文档站点：主题、Markdown、Vue 组件 |
| `pnpm` | pnpm：工作区、catalog、patch、override |
| `turborepo` | 单仓工作流、任务与流水线 |
| `unocss` | UnoCSS 原子化 CSS |
| `finishing-a-development-branch` | 开发分支收尾流程 |
| `receiving-code-review` | 接收与处理 Code Review |
| `requesting-code-review` | 发起 Code Review 请求 |

### 4. 运维 / DevOps 类

| Skill | 功能说明 |
|-------|----------|
| `expo-deployment` | Expo 应用部署：iOS/Android 商店、Web、API 路由 |
| `expo-cicd-workflows` | EAS 工作流 YAML、CI/CD、构建流水线 |
| `openclaw-backup` | OpenClaw 数据备份与恢复、排程 |
| `cron-mastery` | OpenClaw 定时：提醒、定期维护、Cron vs Heartbeat |
| `healthcheck` | 水、睡眠等健康数据追踪（JSON 存储） |
| `auto-updater` | 自动更新相关流程 |
| `safe-exec` | 安全执行 Shell：危险模式检测、风险分级、审批流程、审计 |

### 5. 测试类

| Skill | 功能说明 |
|-------|----------|
| `vue-testing-best-practices` | Vue 测试：Vitest、Vue Test Utils、组件测试、E2E |
| `playwright` | Playwright 自动化与 E2E |
| `python-testing-patterns` | Python 测试模式 |
| `react-doctor` | React 项目改动后快速检查 |
| `web-design-guidelines` | 按 Web 规范审查 UI：可访问性、设计、UX |
| `agentic-eval` | Agent 行为与输出评估 |

### 6. 日常 / 生产力类

| Skill | 功能说明 |
|-------|----------|
| `todoist` | Todoist 任务与项目管理 |
| `apple-reminders` | 通过 `remindctl` 管理 Apple 提醒 |
| `trello` | Trello 看板、列表、卡片 |
| `linear` | Linear Issues、项目、工作流 |
| `google-calendar` | 读写 Google Calendar 事件 |
| `outlook` | Outlook 邮件与日历（Microsoft Graph） |
| `imap-smtp-email` | IMAP/SMTP 邮件收发（支持 Gmail、163 等） |
| `obsidian` | Obsidian 仓库与 obsidian-cli 自动化 |
| `slack` | Slack 消息、反应、置顶等操作 |
| `discord` | Discord 集成 |
| `summarize` | summarize CLI：网页、PDF、图片、音频、YouTube 摘要 |
| `markdown-converter` | 将 PDF/Word/PPT/Excel 等转为 Markdown（markitdown） |
| `imsg` | iMessage/SMS 的 CLI：历史、发送、监听 |
| `readgzh` | 阅读微信公众号全文（含图片帖） |
| `perplexity` | Perplexity 搜索与问答 |
| `google-search` | Google 搜索 |

### 7. 搜索 / 研究类

| Skill | 功能说明 |
|-------|----------|
| `deep-research-pro` | 多源深度研究、综合报告 |
| `searxng` | 本地 SearXNG  metasearch（隐私优先） |
| `openclaw-tavily-search` | Tavily 搜索集成 |
| `yahoo-finance` | 股票、报价、基本面（yfinance，无需 API Key） |

### 8. 文档 / 内容类

| Skill | 功能说明 |
|-------|----------|
| `doc-coauthoring` | 协作写作：需求收集、迭代、读者视角测试 |
| `pptx` | PowerPoint 文档处理 |
| `pdf` | PDF 处理 |
| `nano-pdf` | 轻量 PDF 工具 |
| `microsoft-excel` | Excel 表格操作 |
| `excel-xlsx` | xlsx 读写 |
| `slidev` | Slidev 幻灯片 |
| `feishu-doc` | 飞书文档 |

### 9. 技能 / 智能体管理类

| Skill | 功能说明 |
|-------|----------|
| `skill-vetter` | 安装前安全审核：ClawHub/GitHub 等来源 |
| `openclaw-skill-vetter` | 安全审核协议：凭证窃取、混淆、外泄风险分级 |
| `skill-listing-polisher` | 优化 Skill 公开列表：标题、描述、标签、changelog |

### 10. 其他专用类

| Skill | 功能说明 |
|-------|----------|
| `browser` | 浏览器操作 |
| `browser-use` | 基于浏览器的自动化 |
| `agent-browser-clawdbot` | 为 AI 优化的无头浏览器 CLI |
| `memory-hygiene` | 审计与优化 Clawdbot 向量内存（LanceDB） |
| `elite-longterm-memory` | 长期记忆：WAL + 向量 + git-notes + 云端备份 |
| `agent-memory` | Agent 记忆能力 |
| `openai-whisper-api` | Whisper 语音转写 |
| `openai-image-gen` | OpenAI 图像批量生成 |
| `video-frames` | ffmpeg 截取视频帧/片段 |
| `camsnap` | RTSP/ONVIF 摄像头抓帧 |
| `algorithmic-art` | p5.js 算法艺术 |
| `canvas-design` | 设计类静态图生成（PNG/PDF） |
| `copywriting` | 营销文案撰写与优化 |
| `widget` | macOS Übersicht 桌面组件 |

---

## 二、智能体与推荐 Skills 映射

### 主智能体（General / Orchestrator）

负责统筹、分派、上下文管理，建议技能：

| 推荐 Skills | 用途 |
|-------------|------|
| `proactive-agent` | 主动协作与自主任务 |
| `dispatching-parallel-agents` | 并行任务分派 |
| `byterover` | 项目知识检索与写入 |
| `remembering-conversations` | 从历史会话获取上下文 |
| `session-logs` | 分析自身会话日志 |
| `agent-team-orchestration` | 多智能体协同 |

---

### 需求分析智能体（Requirements Analysis）

负责需求收集、研究、拆解与文档协作：

| 推荐 Skills | 用途 |
|-------------|------|
| `deep-research-pro` | 多源深度研究 |
| `doc-coauthoring` | 文档/规格协作写作 |
| `writing-plans` | 多步骤任务前置规划 |
| `breakdown-feature-implementation` | 功能拆解与实现计划 |
| `executing-plans` | 按计划执行并检查 |
| `data-analysis` | 数据与决策分析 |
| `competitor-alternatives` | 竞品与替代方案研究 |

---

### 编码智能体（Coding）

负责实现、规范与协作流程：

| 推荐 Skills | 用途 |
|-------------|------|
| `code` | 编码工作流 |
| `git` | 版本控制 |
| `github` | GitHub 操作 |
| `api-design-principles` | API 设计 |
| `nodejs-backend-patterns` | Node.js 后端 |
| `next-best-practices` | Next.js 实践 |
| `vercel-react-best-practices` | React/Next 性能 |
| `vue-jsx-best-practices` | Vue JSX |
| `pinia` | Vue 状态管理 |
| `typescript-advanced-types` | TS 高级类型 |
| `requesting-code-review` | 发起 Code Review |
| `finishing-a-development-branch` | 分支收尾 |

---

### 运维智能体（DevOps / Ops）

负责部署、CI/CD、备份与定时任务：

| 推荐 Skills | 用途 |
|-------------|------|
| `expo-deployment` | Expo 部署 |
| `expo-cicd-workflows` | EAS 工作流与 CI/CD |
| `openclaw-backup` | 备份与恢复 |
| `cron-mastery` | 定时与维护任务 |
| `safe-exec` | 安全命令执行 |
| `turborepo` | 单仓流水线 |

---

### 测试智能体（Testing）

负责测试设计与质量检查：

| 推荐 Skills | 用途 |
|-------------|------|
| `vue-testing-best-practices` | Vue 测试 |
| `playwright` | E2E 自动化 |
| `python-testing-patterns` | Python 测试 |
| `react-doctor` | React 快速检查 |
| `web-design-guidelines` | UI/可访问性审查 |
| `agentic-eval` | Agent 输出评估 |

---

### 日常智能体（Daily / Productivity）

负责日程、邮件、任务与信息整理：

| 推荐 Skills | 用途 |
|-------------|------|
| `todoist` | 任务管理 |
| `apple-reminders` | 提醒 |
| `google-calendar` | 日程 |
| `outlook` | 邮件与日历 |
| `obsidian` | 笔记与知识库 |
| `summarize` | 内容摘要 |
| `markdown-converter` | 文档转 Markdown |
| `slack` | 团队协作 |
| `linear` / `trello` | 项目管理 |

---

## 三、快速配置参考

按智能体类型配置时，可在对应 Agent 的 Skills 配置中引用上表。示例：

```
主智能体：     proactive-agent, dispatching-parallel-agents, byterover
需求分析：     deep-research-pro, doc-coauthoring, writing-plans
编码：         code, git, github, api-design-principles
运维：         expo-deployment, cron-mastery, safe-exec
测试：         vue-testing-best-practices, playwright, react-doctor
日常：         todoist, google-calendar, obsidian, summarize
```

---