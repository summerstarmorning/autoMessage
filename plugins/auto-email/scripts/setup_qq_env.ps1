param(
    [Parameter(Mandatory = $true)]
    [string]$QqAddress,

    [Parameter(Mandatory = $true)]
    [string]$AuthCode,

    [ValidateSet("Process", "User")]
    [string]$Scope = "User",

    [switch]$UseStartTls
)

$target = if ($Scope -eq "Process") { "Process" } else { "User" }
$useSsl = -not $UseStartTls
$port = if ($useSsl) { "465" } else { "587" }
$sslFlag = if ($useSsl) { "true" } else { "false" }

[Environment]::SetEnvironmentVariable("AUTO_EMAIL_PROVIDER", "qq", $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_HOST", "smtp.qq.com", $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_PORT", $port, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_USER", $QqAddress, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_PASSWORD", $AuthCode, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_FROM", $QqAddress, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_USE_SSL", $sslFlag, $target)

Write-Host "Configured QQ Mail environment variables in scope: $target"
Write-Host "Provider: qq"
Write-Host "SMTP host: smtp.qq.com"
Write-Host "SMTP port: $port"
Write-Host "From address: $QqAddress"
Write-Host "Auth: QQ Mail authorization code"
if ($target -eq "User") {
    Write-Host "Open a new terminal before testing so the persisted variables are loaded."
}
