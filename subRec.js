/**
 * 周报生成工具：扫描 Git 仓库提交记录，按需求号聚合并调用 JIRA API 获取详情，自动分配工时
 * 使用前请配置 .env 文件（参考 .env.example）
 */
try { require('dotenv').config() } catch { /* dotenv 未安装时可使用 export 设置环境变量 */ }

const fs = require('node:fs')
const path = require('node:path')
const { exec } = require('node:child_process')
const http = require('node:http')
const { promisify } = require('node:util')

const execAsync = promisify(exec)

const GITAUTHOR = process.env.GITAUTHOR || 'jifan'
const CNNAME = process.env.CNNAME || '杨吉繁'
const USERNAME = process.env.JIRA_USERNAME || 'jifan'
const PASSWORD = process.env.JIRA_PASSWORD
const JIRA_HOST = process.env.JIRA_HOST || '192.168.4.113'
const TOTALHOURS = Number(process.env.TOTALHOURS) || 80
const TOTALDAYS = Number(process.env.TOTALDAYS) || 14
const MINUNIT = Number(process.env.MINUNIT) || 0.1

/** 扫描 git 仓库（跳过 node_modules） */
function findGitRepos(dir, repos = []) {
    const files = fs.readdirSync(dir)

    for (const file of files) {
        const fullPath = path.join(dir, file)
        const stat = fs.statSync(fullPath)

        if (fullPath.includes('node_modules')) continue

        if (stat.isDirectory()) {
            if (file === '.git') {
                console.warn('已扫到仓库：', dir)
                repos.push(dir)
                break
            }
            findGitRepos(fullPath, repos)
        }
    }
    return repos
}

/** 获取 JIRA 需求详情 */
function getJIRA(id) {
    return new Promise((resolve) => {
        if (!PASSWORD) {
            console.error('未配置 JIRA_PASSWORD，请在 .env 中设置或 export JIRA_PASSWORD=xxx')
            resolve(null)
            return
        }

        const options = {
            hostname: JIRA_HOST,
            port: 80,
            path: `/rest/api/2/issue/${encodeURIComponent(id)}`,
            method: 'GET',
            headers: {
                Authorization: `Basic ${Buffer.from(`${USERNAME}:${PASSWORD}`).toString('base64')}`,
            },
        }

        const req = http.request(options, (res) => {
            let data = ''
            res.on('data', chunk => (data += chunk))
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const parsed = JSON.parse(data)
                        if (parsed.errorMessages) {
                            resolve(null)
                            return
                        }
                        const obj = {}
                        const fields = parsed.fields
                        if (fields) {
                            if (fields.summary) obj.title = fields.summary
                            if (fields.customfield_10400) obj.linkUsers = fields.customfield_10400.map(item => item.displayName)
                            if (fields.reporter && obj.linkUsers) obj.linkUsers.unshift(fields.reporter.displayName)
                            if (fields.priority) obj.priority = fields.priority.name
                            if (fields.description) obj.description = fields.description
                        }
                        resolve(obj)
                    }
                    catch (e) {
                        console.error('解析 JIRA 响应失败:', e.message)
                        resolve(null)
                    }
                }
                else {
                    console.error(`请求失败 status: ${res.statusCode}`)
                    resolve(null)
                }
            })
        })

        req.on('error', err => {
            console.error('JIRA 请求错误:', err.message)
            resolve(null)
        })
        req.end()
    })
}

/** 获取指定仓库的 Git 提交日志 */
async function getGitLogs(repoPath, author) {
    console.warn('进入列队：', repoPath)
    const gitCommand = `git log --since="${TOTALDAYS} days ago" --author="${author}" --pretty=format:"%s"`
    try {
        const { stdout } = await execAsync(gitCommand, { cwd: repoPath })
        return stdout?.trim() ? stdout.trim().split('\n') : []
    }
    catch (error) {
        console.error(`获取日志失败 [${repoPath}]:`, error.message)
        return []
    }
}

/** 解析提交记录，提取需求号并统计次数 */
function parseLogsToDict(logs) {
    const matched = logs
        .map(item => item.match(/^[a-z]+:\s.+/g))
        .filter(Boolean)
        .flat()
    const dict = {}
    for (const item of matched) {
        dict[item] = (dict[item] || 0) + 1
    }
    return dict
}

/** 分配工时（按提交比例） */
function allocateHours(submissions, totalHours, minUnit) {
    const total = Object.values(submissions).reduce((a, b) => a + b, 0)
    const allocated = {}
    let remaining = totalHours

    for (const key of Object.keys(submissions)) {
        const proportion = submissions[key] / total
        const hours = Math.round((proportion * totalHours) / minUnit) * minUnit
        allocated[key] = hours
        remaining -= hours
    }

    const keys = Object.keys(allocated)
    let i = 0
    while (remaining > 0 && i < keys.length) {
        allocated[keys[i]] += minUnit
        remaining -= minUnit
        i++
    }
    return allocated
}

/** 主流程 */
async function main() {
    const repos = findGitRepos('./')
    if (repos.length === 0) {
        console.warn('未找到 Git 仓库')
        return
    }

    console.warn(`找到 ${repos.length} 个仓库，提取最近 ${TOTALDAYS} 天提交`)

    const allLogs = []
    for (const repo of repos) {
        const logs = await getGitLogs(repo, GITAUTHOR)
        if (logs.length) {
            console.warn(`${repo} --- ${logs.length} 条日志`)
            allLogs.push(...logs)
        }
        else {
            console.warn(`${repo} --- 无日志`)
        }
    }

    const logsDict = parseLogsToDict(allLogs)
    const keys = Object.keys(logsDict)

    if (keys.length === 0) {
        console.warn('没有匹配的需求提交记录')
        return
    }

    console.warn('\n需求提交次数：', logsDict)
    console.warn('\n开始获取 JIRA 需求内容...')

    const jiraResults = await Promise.all(keys.map(id => getJIRA(id)))
    const successKeys = []
    const failKeys = []

    keys.forEach((key, index) => {
        const info = jiraResults[index]
        if (info) {
            successKeys.push({
                key,
                title: info.title,
                linkUsers: info.linkUsers,
                priority: info.priority,
                description: info.description,
            })
        }
        else {
            failKeys.push({ key })
        }
    })

    console.warn('\n成功需求：', successKeys.map(i => i.key))
    if (failKeys.length) console.error('\n失败需求：', failKeys.map(i => i.key))

    if (successKeys.length === 0) {
        console.warn('无成功获取的需求，无法生成周报')
        return
    }

    const submissions = {}
    successKeys.forEach(item => (submissions[item.key] = logsDict[item.key]))
    const allocatedHours = allocateHours(submissions, TOTALHOURS, MINUNIT)

    const simpleReport = successKeys.map(item => {
        const users = (item.linkUsers || []).filter(u => !u.includes(CNNAME)).join(', ') || '---'
        return `${item.key}  ${item.title}   对接人：${users}      工时：${+(allocatedHours[item.key] || 0).toFixed(1)}h`
    })

    const detailReport = successKeys.map(item => ({
        content: `${item.key}  ${item.title}`,
        linkUsers: (item.linkUsers || []).filter(u => !u.includes(CNNAME)).join(', ') || '---',
        time: `${+(allocatedHours[item.key] || 0).toFixed(1)}h`,
        priority: item.priority,
        description: item.description || '----',
    }))

    console.warn('\n\n========== 简单报告 ==========\n')
    console.warn(simpleReport.join('\n'))

    console.warn('\n\n========== 详细报告 ==========\n')
    console.warn(JSON.stringify(detailReport, null, 2))
}

main().catch(err => {
    console.error('执行失败:', err)
    process.exit(1)
})
