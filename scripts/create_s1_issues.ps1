param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [hashtable]$AssigneeMap = @{}
)

$ErrorActionPreference = "Stop"

$issues = @(
    @{ 
        Title = "[S1][rules] 冻结首版规则边界与优先级";
        Owner = "徐志翔";
        Due = "2026-04-16";
        Labels = "type:feature,stage:S1,module:rules,priority:P0";
        Body = "目标：形成规则台账V0.1，明确P0/P1规则项。`nDoD：规则项清单评审通过并归档。"
    },
    @{ 
        Title = "[S1][management] M1验收标准发布";
        Owner = "徐志翔";
        Due = "2026-04-17";
        Labels = "type:docs,stage:S1,module:docs,priority:P0";
        Body = "目标：发布里程碑M1验收清单。`nDoD：团队确认并签收。"
    },
    @{ 
        Title = "[S1][model] 语义归一化输入输出协议草案";
        Owner = "刘文旭";
        Due = "2026-04-17";
        Labels = "type:feature,stage:S1,module:model,priority:P1";
        Body = "目标：定义模型输入输出字段与约束。`nDoD：接口文档合并到docs/architecture。"
    },
    @{ 
        Title = "[S1][web] 后端接口初版定义";
        Owner = "刘文旭";
        Due = "2026-04-19";
        Labels = "type:feature,stage:S1,module:web,priority:P1";
        Body = "目标：完成上传、任务查询、结果查询接口草案。`nDoD：OpenAPI草案提交。"
    },
    @{ 
        Title = "[S1][rules] 字段映射与别名表 V0.1";
        Owner = "邱馨甜";
        Due = "2026-04-16";
        Labels = "type:feature,stage:S1,module:rules,priority:P0";
        Body = "目标：建立核心字段映射关系。`nDoD：字段映射文档审阅通过。"
    },
    @{ 
        Title = "[S1][test] 样本用例设计 V0.1";
        Owner = "邱馨甜";
        Due = "2026-04-19";
        Labels = "type:test,stage:S1,module:docs,priority:P1";
        Body = "目标：覆盖核心规则样本用例。`nDoD：不少于20条测试样本说明。"
    },
    @{ 
        Title = "[S1][parser] PDF文本与截图分离最小可运行链路";
        Owner = "叶泽东";
        Due = "2026-04-18";
        Labels = "type:feature,stage:S1,module:parser,priority:P0";
        Body = "目标：单PDF可提取文本与图片。`nDoD：输出文件可用于后续OCR。"
    },
    @{ 
        Title = "[S1][deploy] 本地开发环境脚本初版";
        Owner = "叶泽东";
        Due = "2026-04-20";
        Labels = "type:chore,stage:S1,module:deploy,priority:P1";
        Body = "目标：实现一键安装依赖与启动。`nDoD：新成员30分钟内完成环境搭建。"
    },
    @{ 
        Title = "[S1][ocr] OCR后处理策略文档";
        Owner = "王牧秋";
        Due = "2026-04-17";
        Labels = "type:feature,stage:S1,module:ocr,priority:P1";
        Body = "目标：定义降噪、纠错、关键字段提取策略。`nDoD：策略文档合并。"
    },
    @{ 
        Title = "[S1][evidence] 证据映射数据结构 V0.1";
        Owner = "王牧秋";
        Due = "2026-04-19";
        Labels = "type:feature,stage:S1,module:evidence,priority:P1";
        Body = "目标：定义字段命中与页码/截图关联模型。`nDoD：结构定义文件提交。"
    },
    @{ 
        Title = "[S1][ci] 最小CI流程搭建";
        Owner = "吴世豪";
        Due = "2026-04-17";
        Labels = "type:test,stage:S1,module:ci,priority:P0";
        Body = "目标：PR触发基础检查。`nDoD：CI执行语法与测试。"
    },
    @{ 
        Title = "[S1][test] 测试规范与回归模板";
        Owner = "吴世豪";
        Due = "2026-04-20";
        Labels = "type:docs,stage:S1,module:docs,priority:P1";
        Body = "目标：发布缺陷记录模板与回归流程。`nDoD：团队按模板提测。"
    }
)

foreach ($issue in $issues) {
    $owner = $issue.Owner
    $assignee = $null

    if ($AssigneeMap.ContainsKey($owner)) {
        $assignee = $AssigneeMap[$owner]
    }

    $body = "负责人：$owner`n截止日期：$($issue.Due)`n`n$($issue.Body)"

    if ([string]::IsNullOrWhiteSpace($assignee)) {
        gh issue create --repo $Repo --title $issue.Title --body $body --label $issue.Labels | Out-Null
    }
    else {
        gh issue create --repo $Repo --title $issue.Title --body $body --label $issue.Labels --assignee $assignee | Out-Null
    }

    Write-Host "Created issue: $($issue.Title)"
}

Write-Host "Done. S1 issues created."
