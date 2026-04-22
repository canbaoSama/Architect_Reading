# OpenClaw + OpenAI 抖音国际新闻自动化方案（可落地）

## 1. 项目目标与边界

### 1.1 目标
- 搭建一套可持续运行的自动化流程：定时发现国际大新闻、核验、多模态素材准备、自动生成短视频素材包、发布与复盘。
- 初期目标产能：每天 3-6 条短视频（快讯为主）。
- 初期目标时效：从事件发现到可发布视频包，控制在 20-40 分钟。

### 1.2 边界
- OpenAI 负责智能处理（搜索策略、抽取、去重、核验辅助、文案、素材匹配、审校）。
- 原始新闻事实必须来自权威外部站点（白名单），不可将模型输出当作一手事实来源。
- 战争/冲突类内容默认高风险，需要更严格审核门禁。

---

## 2. 总体架构（AI 主导的自动化流水线）

```text
Cron Scheduler
  -> ScoutAgent (智能采集)
  -> NormalizeAgent (结构化抽取)
  -> ClusterAgent (语义去重聚类)
  -> VerifyAgent (多源事实核验)
  -> ScriptAgent (30s/60s 脚本生成)
  -> AssetAgent (素材检索、匹配、补生成)
  -> VoiceSubAgent (配音 + 字幕)
  -> JianyingPackAgent (剪映输入包)
  -> ComplianceAgent (合规门禁)
  -> PublishAgent (发布执行)
  -> AnalyticsAgent (数据复盘闭环)
```

---

## 3. 权威信源体系（白名单制）

## 3.1 站点分级

### Tier-1（必须）
- 官方/国际组织：UN、WHO、各国外交部与政府官网、欧盟/NATO 等
- 通讯社：Reuters、AP

### Tier-2（可用于补充）
- BBC、FT、WSJ、NYT、Al Jazeera

### Tier-3（专题数据）
- 能源/冲突/航运等机构数据源（IEA、OPEC、ACLED 等）

## 3.2 发布门禁规则（硬规则）
- 每个事件最少 2 个独立来源。
- 其中至少 1 个来源必须来自 Tier-1。
- 如来源存在关键冲突（时间、地点、伤亡规模等核心字段不一致）：标记待核实，禁止自动发布。
- 单一来源事件不进发布流，只进入监控池。

---

## 4. 详细流程设计（每一步怎么实现）

## 4.1 ScoutAgent（智能采集）

### 输入
- 主题集合：如“伊朗冲突、停火、制裁、油价、军援、联合国声明”
- 时间窗：最近 2 小时

### 实现
- 使用 LLM 先生成多语言检索词（中文/英文/区域语言）。
- 用 MCP/HTTP 工具访问白名单站点 RSS/API/网页。
- 输出原始候选：
```json
{
  "id": "raw_xxx",
  "url": "...",
  "domain": "reuters.com",
  "publishedAt": "2026-03-18T08:10:00Z",
  "title": "...",
  "rawText": "..."
}
```

## 4.2 NormalizeAgent（结构化抽取）

### 目标
- 把非结构化新闻正文抽为统一字段（5W1H + claim 列表）。

### 输出
```json
{
  "eventHint": "伊朗相关地区冲突升级",
  "time": "...",
  "location": "...",
  "actors": ["..."],
  "claims": [
    "A 在 B 时间表示...",
    "C 地区发生..."
  ],
  "sourceMeta": {
    "domain": "...",
    "tier": "tier1"
  }
}
```

## 4.3 ClusterAgent（语义去重聚类）

### 实现
- 对标题+核心 claims 生成 embeddings（OpenAI）。
- 相似度阈值建议：0.84~0.88。
- 按“主题近似 + 时间窗口 + 实体重叠”聚合为 event cluster。

### 规则
- 同一事件的更新（新进展）并入原 cluster，追加阶段号。
- 噪声条目（低文本质量、实体不完整）进入隔离队列。

## 4.4 VerifyAgent（事实核验）

### 目标
- 对每条 claim 做“支持/冲突/未知”判定。

### 实现
- Claim 级反向检索：在白名单中寻找独立证据。
- 计算：
  - `confidenceScore`（可信度）
  - `conflictScore`（冲突度）
  - `publishable`（是否可发布）

### 建议阈值
- `confidenceScore >= 75` 且 `conflictScore <= 25` 才可进入脚本环节。

## 4.5 ScriptAgent（脚本生成）

### 产出
- 30 秒快讯版
- 60 秒解读版

### 格式约束
- 开头 3 秒：结论
- 中段：3 个事实点（每点一句）
- 结尾：影响 + 来源 + 时间戳
- 对未确认内容必须显式标注“待核实”

## 4.6 AssetAgent（素材智能准备）

### 目标
- 按脚本自动匹配镜头，缺失素材自动补生成信息图/地图图层。

### 实现
1. LLM 把脚本拆为 shotlist。
2. 调用素材库 API（授权站点/自建库）检索候选。
3. 多模态相关性打分（文案-画面匹配）。
4. 低匹配素材剔除；缺口由 AI 生成图表素材补齐。

### 输出
```json
{
  "shots": [
    {"line": 1, "asset": "assets/a.mp4", "start": 0.0, "end": 3.5},
    {"line": 2, "asset": "assets/map_1.png", "start": 3.5, "end": 7.0}
  ],
  "sourceTrace": [...]
}
```

## 4.7 VoiceSubAgent（配音与字幕）

### 实现
- TTS 生成旁白音轨（语速统一，支持多音色 A/B 测试）。
- ASR 或 forced alignment 生成字幕时间轴。

### 输出
- `voice.mp3`
- `subtitle.srt`

## 4.8 JianyingPackAgent（剪映素材包）

### 目的
- 把自动化成果组织为剪映可快速套模板的输入包。

### 目录规范
```text
video_job_YYYYMMDD_HHMM/
  script.txt
  voice.mp3
  subtitle.srt
  cover.txt
  timeline.csv
  assets/
  sources.json
  verify_report.json
```

## 4.9 ComplianceAgent（发布门禁）

### 检查项
- 是否缺来源/时间标注
- 是否存在绝对化、煽动性、未证实断言
- 素材授权是否可追溯
- 高风险词是否触发人工复核

### 门禁结果
- pass：进入发布
- reject：回退脚本/素材环节
- manual_review：人工确认后发布

## 4.10 PublishAgent + AnalyticsAgent（发布与闭环）

### 发布
- 初期半自动上传抖音（更稳）。
- 稳定后再做自动发布执行器。

### 复盘
- 每条采集：曝光、3 秒留存、完播率、互动率、转粉率。
- 每日产出策略建议：
  - 题材优先级
  - 开头 3 秒模板
  - 标题与封面对照实验

---

## 5. 数据结构设计（最小可用）

### 核心表
- `raw_news`：原始新闻抓取
- `events`：聚类事件
- `claims`：事件断言
- `claim_evidence`：断言证据链
- `video_jobs`：视频任务状态
- `publish_logs`：发布日志
- `metrics_daily`：效果数据

### 关键字段建议
- `events.status`: monitoring / verified / blocked / published
- `video_jobs.status`: pending / rendering / reviewed / published / failed

---

## 6. OpenClaw Workflow 示例（伪配置）

```json
{
  "workflows": [
    {
      "id": "intl-news-2h",
      "trigger": {"cron": "0 */2 * * *"},
      "steps": [
        {"agentId": "scout"},
        {"agentId": "normalize"},
        {"agentId": "cluster"},
        {"agentId": "verify"},
        {"agentId": "script"},
        {"agentId": "asset"},
        {"agentId": "voicesub"},
        {"agentId": "jianying-pack"},
        {"agentId": "compliance"},
        {"agentId": "publish"},
        {"agentId": "analytics"}
      ]
    }
  ]
}
```

---

## 7. 技术栈建议

- 编排：OpenClaw
- 模型：OpenAI（LLM + Embeddings + TTS/ASR）
- 存储：PostgreSQL + pgvector
- 缓存/队列：Redis
- 媒体处理：FFmpeg
- 剪映：模板化生产（输入包驱动）
- 监控：Prometheus/Grafana（可选）

---

## 8. 两周落地计划（可执行）

## Week 1（MVP）
- D1-D2：信源白名单 + Scout + Normalize
- D3：Cluster + Verify（双来源门禁）
- D4：Script + Compliance
- D5：Asset + VoiceSub + JianyingPack
- D6-D7：人工发布试运行（每天 3 条）

## Week 2（稳定与提效）
- 加强冲突检测与人工复核机制
- 上线封面/标题 A/B 测试
- 优化素材匹配评分
- 形成每日自动复盘报告

---

## 9. 关键 KPI 与验收标准

- 时效：事件到视频包 <= 40 分钟
- 准确：重大事实错误率 = 0（必须）
- 产能：稳定 3-6 条/天
- 内容质量：30 秒视频完播率 >= 20%
- 增长：7 天粉丝净增与互动率持续上行

---

## 10. 风险控制与应急

- 红线题材默认人工审核
- 出现事实反转：1 小时内发布澄清/更新
- 自动发布失败：降级人工发布
- 素材版权风险：无授权素材不进发布流

---

## 11. 首批执行清单（今天即可开始）

1. 建立白名单（先 15 个域名）。
2. 配置 OpenClaw 定时任务（每 2 小时）。
3. 完成 VerifyAgent 的双来源门禁逻辑。
4. 固化 30 秒快讯模板（剪映）。
5. 跑通第一条“从采集到剪映包”的端到端链路。

---

## 附录：建议输出文件命名规范

- `event_<date>_<topic>_<seq>.json`
- `video_<date>_<eventId>_v1.mp4`
- `verify_<eventId>.json`
- `publish_<platform>_<eventId>.json`

