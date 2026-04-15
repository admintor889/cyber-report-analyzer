param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [string]$DefaultBranch = "main",
    [string]$DevelopBranch = "develop"
)

$ErrorActionPreference = "Stop"

Write-Host "Checking GitHub CLI..."
gh --version | Out-Null

Write-Host "Setting default branch to $DefaultBranch"
gh repo edit $Repo --default-branch $DefaultBranch

Write-Host "Creating develop branch"
git checkout $DefaultBranch
git pull
git checkout -b $DevelopBranch
git push -u origin $DevelopBranch

Write-Host "Creating labels"
$labels = @(
    "type:feature|0e8a16|Feature task",
    "type:bug|d73a4a|Bug report",
    "type:test|1d76db|Test task",
    "type:docs|5319e7|Docs task",
    "type:refactor|fbca04|Refactor task",
    "type:chore|c5def5|Chore task",
    "stage:S1|bfdadc|Stage 1",
    "stage:S2|bfdadc|Stage 2",
    "stage:S3|bfdadc|Stage 3",
    "stage:S4|bfdadc|Stage 4",
    "stage:S5|bfdadc|Stage 5",
    "module:parser|0366d6|Parser module",
    "module:ocr|0366d6|OCR module",
    "module:rules|0366d6|Rules module",
    "module:model|0366d6|Model module",
    "module:web|0366d6|Web module",
    "module:evidence|0366d6|Evidence module",
    "module:deploy|0366d6|Deploy module",
    "module:ci|0366d6|CI module",
    "module:docs|0366d6|Docs module",
    "priority:P0|b60205|Blocker",
    "priority:P1|d93f0b|High",
    "priority:P2|fbca04|Medium",
    "priority:P3|0e8a16|Low",
    "status:blocked|d93f0b|Blocked",
    "status:need-review|1d76db|Need review",
    "status:ready-for-test|0e8a16|Ready for test",
    "status:ready-for-release|5319e7|Ready for release"
)

foreach ($item in $labels) {
    $parts = $item.Split("|")
    $name = $parts[0]
    $color = $parts[1]
    $desc = $parts[2]

    gh label create $name --repo $Repo --color $color --description $desc 2>$null
    if ($LASTEXITCODE -ne 0) {
        gh label edit $name --repo $Repo --color $color --description $desc | Out-Null
    }
}

Write-Host "Applying branch protections"
$payload = @'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["quality"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
'@

$tmp = New-TemporaryFile
Set-Content -Path $tmp -Value $payload -Encoding UTF8
gh api -X PUT repos/$Repo/branches/$DefaultBranch/protection --input $tmp
Remove-Item $tmp -Force

Write-Host "Done. Next: create S1 issues from docs/github/S1-issue-backlog.md"
