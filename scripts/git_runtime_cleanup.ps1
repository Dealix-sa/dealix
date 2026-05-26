# Git Runtime Cleanup Script

# Remove runtime folders from git cache if they were accidentally added
$foldersToClean = @(
    "local_ai/queue",
    "local_ai/followups",
    "reports/launch",
    "reports/board",
    "reports/operator",
    "local_ai/outputs",
    "local_ai/cache"
)

foreach ($folder in $foldersToClean) {
    if (Test-Path $folder) {
        Write-Host "Cleaning $folder from git index..."
        git rm -r --cached $folder 2>$null
    }
}

Write-Host "Done. Check git status to verify." -ForegroundColor Green
git status
