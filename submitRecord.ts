//@ts-ignore
const fs = require('fs')
//@ts-ignore
const path = require('path')
//@ts-ignore
const { exec } = require('child_process')
//@ts-ignore
const http = require('http')

let allLogs = []

const GITAUTHOR = ''   //git显示的用户名，用于分离出自己的提交记录
const CNNAME = ''      //阁下大名，中文，需求参与人员可以把自己过滤掉
const USERNAME = ''  //jira 用户名，根据需求号用API去获取需求详情
const PASSWORD = '' //jira 密码，同上
const TOTALHOURS = 80  //总工时, 建议适当向上浮动
const TOTALDAYS = 14  //拉取git的最近n天的提交记录
const MINUNIT = 0.1   //工时精度

const findGitRepos = (dir, repos = []) => {
    const files = fs.readdirSync(dir)

    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (fullPath.includes('node_modules')) return

        if (stat.isDirectory()) {
            if (file === '.git') {
                console.log('已扫到仓库：', dir)
                repos.push(dir)
                break
            } else {
                findGitRepos(fullPath, repos)
            }
        }
    }
    return repos
}

const getJIRA = id => new Promise((resolve, reject) => {
    const options = {
        hostname: '10.xxx.80.xxx',
        port: 8080,
        path: '/rest/api/2/issue/' + id,
        method: 'GET',
        headers: { 'Authorization': 'Basic ' + Buffer.from(USERNAME + ':' + PASSWORD).toString('base64') }
    }

    const req = http.request(options, res => {
        let data = ''

        res.on('data', chunk => data += chunk)

        res.on('end', () => {
            const res = JSON.parse(data)
            if (res.errorMessages) {
                resolve(null)
            } else {
                let obj = {}
                const fields = res.fields

                if (fields) {
                    if (fields.summary) {
                        obj.title = fields.summary
                    }
                    if (fields.customfield_10400) {
                        obj.linkUsers = fields.customfield_10400.map(item => item.displayName)
                    }
                    if (fields.reporter && obj.linkUsers) {
                        obj.linkUsers.unshift(fields.reporter.displayName)
                    }
                    if (fields.priority) {
                        obj.priority = fields.priority.name
                    }
                    if (fields.description) {
                        obj.description = fields.description
                    }
                }

                resolve(obj)
            }
        })
    })

    req.on('error', error => console.error('Error:', error))
    req.end()
})

const getGitLogs = (repoPath, author, callback) => {
    console.log('进入列队：', repoPath)
    const gitCommand = `git log --since="${TOTALDAYS} days ago" --author="${author}" --pretty=format:"%s"`;
    exec(gitCommand, { cwd: repoPath }, (error, stdout, stderr) => {
        if (error) {
            console.error(`获取日志时出错: ${error}`);
            return;
        }

        if (stderr) {
            console.error(`标准错误: ${stderr}`);
            return;
        }

        if (stdout && stdout.trim()) {
            const arr = stdout.trim().split('\n')
            console.log(`${repoPath} --- ${arr.length} 条日志`)
            allLogs = allLogs.concat(arr)
        } else {
            console.log(`${repoPath} --- 没有日志`)
        }

        callback && callback()
    });
}

const handleLog = () => {
    allLogs = allLogs.map(item => item.match(/[A-Z]+-\d+/g)).filter(Boolean).flat()

    const logsDict = {}

    allLogs.forEach(item => {
        if (!logsDict[item]) {
            logsDict[item] = 1
        } else {
            logsDict[item] = logsDict[item] += 1
        }
    })

    console.log('\n\n\n\n\n需求提交次数：', logsDict, '\n\n\n\n\n开始获需求内容')

    let keys = Object.keys(logsDict)
    let keysRes = []
    let successKeys = []
    let failKeys = []

    Promise.all(keys.map(item => getJIRA(item))).then(values => {
        keysRes = values

        keys.forEach((key, index) => {
            if (keysRes[index]) {
                successKeys.push({
                    key: key,
                    title: keysRes[index].title,
                    linkUsers: keysRes[index].linkUsers,
                    priority: keysRes[index].priority,
                    description: keysRes[index].description
                })
            } else {
                failKeys.push({ key: key })
            }
        })

        console.log('\n\n\n\n\n成功需求：', successKeys.map(i => i.key))

        if (failKeys.length) {
            console.error('\n\n\失败需求：', failKeys.map(i => i.key))
        }

        if (successKeys.length) {
            console.error('\n\n\n\n\n最终周报：\n')
            const submissions = {}
            successKeys.forEach(item => submissions[item.key] = logsDict[item.key])
            const totalHours = TOTALHOURS
            const minUnit = MINUNIT
            const totalSubmissions = Object.values(submissions).reduce((a, b) => a + b, 0)

            const allocatedHours = {};
            let remainingHours = totalHours

            Object.keys(submissions).forEach(key => {
                const proportion = submissions[key] / totalSubmissions
                let hours = Math.round((proportion * totalHours) / minUnit) * minUnit
                allocatedHours[key] = hours
                remainingHours -= hours
            })

            const keys = Object.keys(allocatedHours)
            let i = 0
            while (remainingHours > 0 && i < keys.length) {
                allocatedHours[keys[i]] += minUnit
                remainingHours -= minUnit
                i++
            }

            const sortReport = successKeys.map(i => {
                return i.key + '  ' + i.title + '   对接人：' + ((i.linkUsers || []).filter(u => !u.includes(CNNAME)).join(', ') || '---') + '      工时：' + (+(allocatedHours[i.key] || 0).toFixed(1)) + 'h'
            })

            console.log('\n\n简单报告：\n')
            console.log(sortReport)

            const report = successKeys.map(i => {

                return {
                    content: i.key + '  ' + i.title,
                    linkUsers: (i.linkUsers || []).filter(u => !u.includes(CNNAME)).join(', ') || '---',
                    time: +(allocatedHours[i.key] || 0).toFixed(1) + 'h',
                    priority: i.priority,
                    description: i.description || '----'
                }

            })

            console.log('\n\n详细报告：\n')
            console.log(report)
        }
    })
}

const scanGitRepos = (rootDir, author) => {
    const repos = findGitRepos(rootDir)

    if (repos.length === 0) {
        return console.log('未找到 Git 仓库')
    }

    console.log(`总共找到 ${repos.length} 个仓库，开始提取最近${TOTALDAYS}天的提交日志`)

    repos.forEach((repo, i) => {
        if (i < repos.length - 1) {
            getGitLogs(repo, author)
        } else {
            getGitLogs(repo, author, handleLog)
        }

    })
}

scanGitRepos('./', GITAUTHOR) // 扫描./ 目录下的所有git 仓库，并读取 GITAUTHOR = 14 天内

