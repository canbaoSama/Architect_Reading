#!/usr/bin/env python3
"""按分类将 skills 移动到子文件夹"""
import os
from pathlib import Path

# 分类映射：skill_name -> category_folder
CATEGORY_MAP = {
    # 1. 主智能体/编排
    "orchestration": [
        "proactive-agent", "proactive-agent-lite", "dispatching-parallel-agents",
        "agent-team-orchestration", "swarmclaw", "byterover", "remembering-conversations",
        "session-logs", "agent-autonomy-kit", "agent-governance", "agent-reach",
        "capability-evolver", "subagent-driven-development", "miniade-agent-lifecycle-manager",
    ],
    # 2. 需求分析
    "requirements": [
        "deep-research-pro", "academic-deep-research", "doc-coauthoring", "writing-plans",
        "breakdown-feature-implementation", "executing-plans", "data-analysis", "data-analyst",
        "competitor-alternatives", "offer-positioning-auditor", "pricing-strategy",
        "marketing-psychology", "architecture-blueprint-generator", "architecture-patterns",
        "brainstorming", "content-strategy", "launch-strategy", "product-marketing-context",
    ],
    # 3. 编码
    "coding": [
        "code", "coding", "git", "git-commit", "git-essentials", "github",
        "api-design-principles", "api-gateway", "nodejs-backend-patterns",
        "next-best-practices", "next-cache-components", "nextjs-app-router-patterns",
        "vercel-react-best-practices", "vercel-composition-patterns", "vercel-ai-sdk",
        "vue-jsx-best-practices", "vue-router-best-practices", "vue-router-best-practices-hyf0",
        "vue-best-practices", "vue-best-practices-hyf0", "vue-pinia-best-practices",
        "vue-debug-guides", "vue", "pinia", "react-doctor", "react-state-management",
        "typescript-advanced-types", "modern-javascript-patterns", "web-component-design",
        "frontend-design-ultimate", "vitepress", "vite", "pnpm", "turborepo", "unocss",
        "nuxt", "finishing-a-development-branch", "receiving-code-review", "requesting-code-review",
        "code-review", "microservices-patterns", "python-design-patterns",
        "better-auth-best-practices", "create-auth-skill", "postgresql-table-design",
        "supabase-postgres-best-practices", "mcp-builder", "rustchain-mcp",
        "responsive-design", "docker-essentials", "code-exemplars-blueprint-generator",
    ],
    # 4. 运维
    "devops": [
        "expo-deployment", "expo-cicd-workflows", "expo-api-routes", "expo-dev-client",
        "expo-building-native-ui", "expo-tailwind-setup", "expo-native-data-fetching",
        "expo-ui-jetpack-compose", "expo-ui-swift-ui", "expo-use-dom", "upgrading-expo",
        "upgrading-react-native", "openclaw-backup", "cron-mastery", "healthcheck",
        "auto-updater", "safe-exec", "n8n", "n8n-workflow-automation", "automation-workflows",
    ],
    # 5. 测试
    "testing": [
        "vue-testing-best-practices", "vue-testing-best-practices-hyf0", "playwright",
        "playwright-mcp", "python-testing-patterns", "web-design-guidelines",
        "agentic-eval", "webapp-testing", "test-driven-development",
        "audit-website", "security-auditor", "verification-before-completion",
    ],
    # 6. 日常/生产力
    "productivity": [
        "todoist", "apple-reminders", "trello", "linear", "notion",
        "google-calendar", "gcalcli-calendar", "caldav-calendar", "calendar",
        "outlook", "imap-smtp-email", "gmail", "himalaya",
        "obsidian", "apple-notes", "bear-notes", "slack", "discord",
        "summarize", "markdown-converter", "imsg", "blucli", "bluebubbles",
        "readgzh", "perplexity", "widget", "things-mac", "productivity",
    ],
    # 7. 搜索/研究
    "search": [
        "searxng", "openclaw-tavily-search", "tavily", "tavily-search-1-0-0",
        "yahoo-finance", "google-search", "brave-search", "baidu-search",
        "duckduckgo-search", "ddg-web-search", "desearch-web-search",
        "exa-web-search-free", "web-search-plus", "multi-search-engine",
        "firecrawl", "firecrawl-search", "stock-analysis", "stock-market-pro",
        "stock-watcher", "us-stock-analysis", "tushare-finance", "trader-daily",
    ],
    # 8. 文档/内容
    "docs-content": [
        "pptx", "pdf", "nano-pdf", "pdf-extract", "pdf-text-extractor",
        "microsoft-excel", "excel-xlsx", "xlsx", "docx", "word-docx",
        "slidev", "feishu-doc", "document-parser", "clean-content-fetch",
        "copywriting", "copy-editing", "writing-skills", "internal-comms",
        "communication-playbook", "citedy-content-ingestion", "citedy-content-writer",
        "citedy-lead-magnets", "citedy-trend-scout", "citedy-video-shorts",
    ],
    # 9. 技能管理
    "skill-mgmt": [
        "skill-vetter", "openclaw-skill-vetter", "skill-listing-polisher",
        "skill-creator", "skill-finder-cn", "skill-scanner", "skill-vetting",
        "find-skills", "template-skill", "clawdhub",
    ],
    # 10. 其他
    "other": [
        "browser", "browser-use", "agent-browser", "agent-browser-clawdbot",
        "memory-hygiene", "elite-longterm-memory", "agent-memory", "memory-manager", "memory-setup",
        "openai-whisper-api", "openai-whisper", "openai-image-gen", "image-generate",
        "video-frames", "camsnap", "algorithmic-art", "canvas-design", "canvas",
        "desktop-control", "computer-use", "1password", "clawsec", "openclaw-guardian",
        "clawdbot-filesystem", "clawddocs", "filesystem", "file-search",
        "1password", "ab-test-setup", "add-educational-comments", "agentmail",
        "ai-humanizer", "humanizer", "humanize-ai-text", "ai-ppt-generator", "ppt-generator",
        "ai-prompt-engineering-safety-review", "ai-prompt-generator", "ai-travel",
        "ai-web-automation", "amazon-price-tracker", "analytics-tracking",
        "answeroverflow", "apple-appstore-reviewer", "blucli", "bluebubbles",
        "boost-prompt", "brand-guidelines", "clankers-world", "compaction-ui-enhancements",
        "debug-pro", "edge-tts", "eightctl", "email-sequence", "erpclaw", "evomap",
        "form-cro", "free-ride", "free-tool-strategy", "gifgrep", "gog", "gogcli",
        "go-install", "go-install-zh", "goplaces", "home-assistant", "last30days",
        "linkedin", "local-places", "ltx-video", "marketing-ideas", "marketing-mode",
        "marketing-skills", "mcporter", "mindkeeper", "model-usage", "moltbook-interact",
        "nano-banana-pro", "news-summary", "openhue", "oracle", "ordercli",
        "page-cro", "paid-ads", "partnerships-ecosystem", "peekaboo",
        "personal-finish-notifier", "popup-cro", "programmatic-seo",
        "prompt-engineering-expert", "prompt-engineering-patterns",
        "python-performance-optimization", "qmd", "rag-implementation",
        "react-native-best-practices", "reddit", "reddit-readonly", "referral-program",
        "sag", "salesmate", "scrapling-official", "self-improving", "self-reflection",
        "seo-audit", "shopify-seo-bot", "shopify-seo-optimizer", "signup-flow-cro",
        "slack-gif-creator", "social-content", "songsee", "sonoscli", "spotify-player",
        "sql-toolkit", "superdesign", "systematic-debugging", "tech-data-playbook",
        "telegram", "theme-factory", "tiktok-viral-predictor", "tmux",
        "ui-ux-pro-max", "using-git-worktrees", "using-superpowers",
        "veadk-skills", "weibo-trending-bot", "xiaohongshu-mcp", "x-twitter",
        "xurl", "youtube-api-skill", "youtube-auto-captions", "youtube-transcript",
        "youtube-watcher", "onboarding-cro", "gemini",
    ],
}

def main():
    base = Path(__file__).parent
    # 构建反向映射
    skill_to_cat = {}
    for cat, skills in CATEGORY_MAP.items():
        for s in skills:
            skill_to_cat[s] = cat

    # 创建分类目录
    for cat in CATEGORY_MAP:
        (base / cat).mkdir(exist_ok=True)

    category_dirs = set(CATEGORY_MAP.keys()) | {"other"}
    moved = 0
    unmapped = []
    for d in sorted(base.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name in category_dirs:
            continue
        cat = skill_to_cat.get(d.name, "other")
        dest_dir = base / cat
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / d.name
        if d != dest and not dest.exists():
            d.rename(dest)
            moved += 1
        if d.name not in skill_to_cat:
            unmapped.append(d.name)

    print(f"Moved {moved} skills")
    if unmapped:
        print(f"Auto-placed in other ({len(unmapped)}): {unmapped[:15]}...")

if __name__ == "__main__":
    main()
