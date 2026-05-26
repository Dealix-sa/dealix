# dealix-local-ai-env.ps1
# Helper script to load Ollama local AI environment settings

$env:OLLAMA_HOST = "http://localhost:11434"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " OLLAMA LOCAL AI ENVIRONMENT LOADER" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Primary model: qwen2.5-coder:7b"
Write-Host "Primary host:  $env:OLLAMA_HOST"

# Check if Ollama is running
$running = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($running) {
    Write-Host "[PASS] Ollama process is actively running locally." -ForegroundColor Green
} else {
    Write-Host "[WARN] Ollama process is NOT running. Please launch Ollama Desktop." -ForegroundColor Yellow
}
