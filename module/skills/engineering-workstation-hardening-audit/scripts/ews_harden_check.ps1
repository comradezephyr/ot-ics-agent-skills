#Requires -Version 5.1
<#
.SYNOPSIS
Collect EWS hardening state as JSON. Read-only.
#>
param(
    [string]$Out = "ews-audit.json"
)

function Get-AuditState {
    $state = [ordered]@{}
    $state.collected_at = (Get-Date).ToUniversalTime().ToString("o")

    $hf = Get-HotFix | Sort-Object InstalledOn -Descending
    $state.hotfix_count = @($hf).Count
    $state.newest_hotfix = if ($hf) { "$($hf[0].HotFixID) installed $($hf[0].InstalledOn)" } else { "none" }

    $usbPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\RemovableStorageDevices"
    $usb = Get-ItemProperty -Path $usbPath -ErrorAction SilentlyContinue
    $state.usb_deny_all = if ($usb -and $usb.Deny_All -eq 1) { 1 } else { 0 }

    try {
        $al = Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop
        $state.applocker_enforced = if ($al -match "<RuleCollection") { "Enforced" } else { "NotConfigured" }
    } catch {
        $state.applocker_enforced = "NotConfigured"
    }

    try {
        $mp = Get-MpPreference -ErrorAction Stop
        $state.av_exclusion_paths = @($mp.ExclusionPath)
        $state.av_exclusion_processes = @($mp.ExclusionProcess)
    } catch {
        $state.av_exclusion_paths = @("av-state-unknown")
        $state.av_exclusion_processes = @()
    }

    $state.local_admins = @(
        Get-LocalGroupMember -Group "Administrators" -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty Name
    )

    $agentNames = @("TeamViewer", "AnyDesk", "VNC", "GoToMyPC", "LogMeIn", "RustDesk", "Splashtop", "Ammyy")
    $state.remote_agents = @(
        Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $n = $_.ProcessName; $agentNames | Where-Object { $n -match $_ } } |
        Select-Object -Unique -ExpandProperty ProcessName
    )

    $uninstall = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    $state.installed_software = @(
        Get-ItemProperty $uninstall -ErrorAction SilentlyContinue |
        Where-Object DisplayName |
        Select-Object DisplayName, DisplayVersion, InstallDate |
        Sort-Object DisplayName -Unique
    )

    $state.listening_ports = @(
        Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
        Select-Object LocalAddress, LocalPort, OwningProcess -Unique
    )

    $state.routes = @(
        Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue |
        Select-Object InterfaceAlias, NextHop
    )

    $state
}

Get-AuditState | ConvertTo-Json -Depth 4 | Set-Content -Path $Out -Encoding UTF8
Write-Output "wrote $Out"

