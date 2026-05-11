# Architect Reading

知识合集型文档，聚焦 **AI 学习**、**面试备战**、**常用技巧**，附带周报生成工具。

## 项目结构

```
├── docs/               # 文档目录
│   ├── AI工具/         # Cursor Rules、Skills、Prompt 工程、MCP 与 Agent
│   ├── 面试/           # 面试题与知识体系（基础、做题、工程化、AI 岗位趋势与题单）
│   ├── 常用技巧/       # CSS、缓存等业务技巧
│   ├── 项目经历/       # 自我介绍与项目亮点
│   ├── 项目解读/       # 项目优点、性能优化等
│   ├── 知识点/         # 旧结构（已迁移，见迁移映射）
│   └── 杂谈/           # 副业等
├── subRec.js           # 周报生成脚本
├── .env.example        # 环境变量示例（复制为 .env 后配置）
└── package.json
```

**文档入口**：[docs/README.md](docs/README.md)

## 周报生成工具 (subRec.js)

扫描当前目录下所有 Git 仓库，根据最近提交记录提取需求号，调用 JIRA API 获取需求详情，并自动按提交比例分配工时。

### 使用步骤

1. 复制环境变量配置并编辑：

   ```bash
   cp .env.example .env
   # 编辑 .env，填写 JIRA_USERNAME、JIRA_PASSWORD 等
   ```

2. 安装依赖并执行：

   ```bash
   npm install
   npm run report
   ```

### 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `JIRA_HOST` | JIRA 服务器地址 | 192.168.4.113 |
| `JIRA_USERNAME` | JIRA 用户名 | jifan |
| `JIRA_PASSWORD` | JIRA 密码（必填） | - |
| `GITAUTHOR` | Git 提交作者名（过滤用） | jifan |
| `CNNAME` | 中文姓名（过滤对接人） | 杨吉繁 |
| `TOTALHOURS` | 总工时 | 80 |
| `TOTALDAYS` | 拉取最近 N 天提交 | 14 |
| `MINUNIT` | 工时精度 | 0.1 |