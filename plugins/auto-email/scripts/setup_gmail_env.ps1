param(
    [Parameter(Mandatory = $true)]
    [string]$GmailAddress,

    [Parameter(Mandatory = $true)]
    [string]$AppPassword,

    [ValidateSet("Process", "User")]
    [string]$Scope = "User",

    [switch]$UseSSL
)

$target = if ($Scope -eq "Process") { "Process" } else { "User" }
$port = if ($UseSSL) { "465" } else { "587" }
$sslFlag = if ($UseSSL) { "true" } else { "false" }

[Environment]::SetEnvironmentVariable("AUTO_EMAIL_PROVIDER", "gmail", $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_HOST", "smtp.gmail.com", $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_PORT", $port, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_USER", $GmailAddress, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_SMTP_PASSWORD", $AppPassword, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_FROM", $GmailAddress, $target)
[Environment]::SetEnvironmentVariable("AUTO_EMAIL_USE_SSL", $sslFlag, $target)

Write-Host "Configured Gmail environment variables in scope: $target"
Write-Host "Provider: gmail"
Write-Host "SMTP host: smtp.gmail.com"
Write-Host "SMTP port: $port"
Write-Host "From address: $GmailAddress"
if ($target -eq "User") {
    Write-Host "Open a new terminal before testing so the persisted variables are loaded."
}
