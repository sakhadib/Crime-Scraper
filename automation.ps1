# Crime Data Scraper - PowerShell Automation Script
# This script provides advanced automation features for Windows

param(
    [string]$Action = "help",
    [string]$Schedule = "daily",
    [string]$Time = "09:00",
    [int]$Hours = 6,
    [string]$TaskName = "CrimeDataScraper"
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = Join-Path $ScriptDir "venv\Scripts\python.exe"
$MainScript = Join-Path $ScriptDir "main.py"
$SchedulerScript = Join-Path $ScriptDir "scheduler.py"

function Write-Header {
    param([string]$Title)
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Cyan
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host
}

function Test-Installation {
    Write-Header "Testing Installation"
    
    if (!(Test-Path $PythonPath)) {
        Write-Host "ERROR: Python virtual environment not found!" -ForegroundColor Red
        Write-Host "Expected path: $PythonPath" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Running installation test..." -ForegroundColor Yellow
    $result = & $PythonPath (Join-Path $ScriptDir "test_installation.py")
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installation test passed!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "Installation test failed!" -ForegroundColor Red
        return $false
    }
}

function Create-ScheduledTask {
    param(
        [string]$Name,
        [string]$Schedule,
        [string]$Time,
        [int]$Hours
    )
    
    Write-Header "Creating Scheduled Task"
    
    # Check if task already exists
    $existingTask = Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Task '$Name' already exists. Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $Name -Confirm:$false
    }
    
    # Create action
    $action = New-ScheduledTaskAction -Execute $PythonPath -Argument "$MainScript --mode full" -WorkingDirectory $ScriptDir
    
    # Create trigger based on schedule
    switch ($Schedule.ToLower()) {
        "daily" {
            $trigger = New-ScheduledTaskTrigger -Daily -At $Time
            Write-Host "Creating daily task at $Time" -ForegroundColor Green
        }
        "hourly" {
            $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
            Write-Host "Creating hourly task" -ForegroundColor Green
        }
        "custom" {
            $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours $Hours)
            Write-Host "Creating custom task (every $Hours hours)" -ForegroundColor Green
        }
        default {
            Write-Host "Invalid schedule type: $Schedule" -ForegroundColor Red
            return $false
        }
    }
    
    # Create settings
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    # Register task
    try {
        Register-ScheduledTask -TaskName $Name -Action $action -Trigger $trigger -Settings $settings -Description "Automated crime data scraping"
        Write-Host "Successfully created scheduled task: $Name" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Remove-ScheduledTask {
    param([string]$Name)
    
    Write-Header "Removing Scheduled Task"
    
    $task = Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue
    if ($task) {
        Unregister-ScheduledTask -TaskName $Name -Confirm:$false
        Write-Host "Successfully removed task: $Name" -ForegroundColor Green
    } else {
        Write-Host "Task '$Name' not found" -ForegroundColor Yellow
    }
}

function Show-TaskStatus {
    param([string]$Name)
    
    Write-Header "Task Status"
    
    $task = Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue
    if ($task) {
        $info = Get-ScheduledTaskInfo -TaskName $Name
        
        Write-Host "Task Name: $($task.TaskName)" -ForegroundColor Green
        Write-Host "State: $($task.State)" -ForegroundColor Green
        Write-Host "Last Run Time: $($info.LastRunTime)" -ForegroundColor Green
        Write-Host "Last Result: $($info.LastTaskResult)" -ForegroundColor Green
        Write-Host "Next Run Time: $($info.NextRunTime)" -ForegroundColor Green
        
        # Show triggers
        Write-Host "`nTriggers:" -ForegroundColor Yellow
        foreach ($trigger in $task.Triggers) {
            Write-Host "  $($trigger.CimClass.CimClassName): $trigger" -ForegroundColor White
        }
    } else {
        Write-Host "Task '$Name' not found" -ForegroundColor Red
    }
}

function Run-Scraper {
    param([string]$Mode = "full")
    
    Write-Header "Running Crime Data Scraper"
    
    Write-Host "Running scraper in $Mode mode..." -ForegroundColor Yellow
    & $PythonPath $MainScript --mode $Mode
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Scraper completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Scraper failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
}

function Start-Scheduler {
    param(
        [string]$Schedule = "daily",
        [string]$Time = "09:00",
        [int]$Hours = 6
    )
    
    Write-Header "Starting Built-in Scheduler"
    
    $args = @("--schedule", $Schedule)
    
    if ($Schedule -eq "daily") {
        $args += @("--time", $Time)
        Write-Host "Starting daily scheduler at $Time" -ForegroundColor Green
    } elseif ($Schedule -eq "custom") {
        $args += @("--hours", $Hours)
        Write-Host "Starting custom scheduler (every $Hours hours)" -ForegroundColor Green
    } else {
        Write-Host "Starting hourly scheduler" -ForegroundColor Green
    }
    
    Write-Host "Press Ctrl+C to stop the scheduler" -ForegroundColor Yellow
    & $PythonPath $SchedulerScript @args
}

function Show-Help {
    Write-Header "Crime Data Scraper - PowerShell Automation"
    
    Write-Host "Usage: .\automation.ps1 -Action <action> [options]" -ForegroundColor White
    Write-Host
    Write-Host "Actions:" -ForegroundColor Yellow
    Write-Host "  test          - Test the installation" -ForegroundColor White
    Write-Host "  run           - Run the scraper once" -ForegroundColor White
    Write-Host "  create-task   - Create a Windows scheduled task" -ForegroundColor White
    Write-Host "  remove-task   - Remove the Windows scheduled task" -ForegroundColor White
    Write-Host "  task-status   - Show scheduled task status" -ForegroundColor White
    Write-Host "  scheduler     - Start the built-in Python scheduler" -ForegroundColor White
    Write-Host "  help          - Show this help message" -ForegroundColor White
    Write-Host
    Write-Host "Options for create-task:" -ForegroundColor Yellow
    Write-Host "  -Schedule     - daily, hourly, or custom (default: daily)" -ForegroundColor White
    Write-Host "  -Time         - Time for daily schedule (default: 09:00)" -ForegroundColor White
    Write-Host "  -Hours        - Hours for custom schedule (default: 6)" -ForegroundColor White
    Write-Host "  -TaskName     - Name for the scheduled task (default: CrimeDataScraper)" -ForegroundColor White
    Write-Host
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\automation.ps1 -Action test" -ForegroundColor White
    Write-Host "  .\automation.ps1 -Action run" -ForegroundColor White
    Write-Host "  .\automation.ps1 -Action create-task -Schedule daily -Time 09:00" -ForegroundColor White
    Write-Host "  .\automation.ps1 -Action create-task -Schedule custom -Hours 6" -ForegroundColor White
    Write-Host "  .\automation.ps1 -Action scheduler -Schedule daily -Time 09:00" -ForegroundColor White
    Write-Host
}

# Main execution
switch ($Action.ToLower()) {
    "test" {
        Test-Installation
    }
    "run" {
        if (Test-Installation) {
            Run-Scraper
        }
    }
    "create-task" {
        if (Test-Installation) {
            Create-ScheduledTask -Name $TaskName -Schedule $Schedule -Time $Time -Hours $Hours
        }
    }
    "remove-task" {
        Remove-ScheduledTask -Name $TaskName
    }
    "task-status" {
        Show-TaskStatus -Name $TaskName
    }
    "scheduler" {
        if (Test-Installation) {
            Start-Scheduler -Schedule $Schedule -Time $Time -Hours $Hours
        }
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Write-Host "Use -Action help for usage information" -ForegroundColor Yellow
    }
}
