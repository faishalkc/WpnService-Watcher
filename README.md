# WpnService Watcher

A lightweight Windows utility that continuously monitors and stops **WpnService** and **WpnUserService** to prevent notification-related freezes on Windows 11.

This tool was inspired by community reports where Windows notification services caused **taskbar freezes and system instability**.

## Background

Some users reported that Windows notification services could cause system issues such as:

* Taskbar freezing
* Notification service instability
* Explorer becoming unresponsive

Discussions that inspired this project:

* https://www.reddit.com/r/WindowsHelp/comments/1obplv6/taskbar_randomly_freezing_on_windows_11_25h2/
* https://www.reddit.com/r/techsupport/comments/1ppmd2g/win11_notifications_and_wpnuserservice_issues/

This watcher continuously ensures these services remain stopped.

## Features

* Monitors `WpnService`
* Monitors `WpnUserService*` (user-session instances)
* Stops services immediately when detected running
* Automatic log rotation (10MB)
* Silent execution (no console window)
* Automatic admin elevation
* Single-instance protection
* Error logging

## Log Location

```
C:\Windows\Logs\wpn_watcher.log
```

## Log Output

```
2026-04-01 10:15:02.118 [ENFORCE] Watcher started. IntervalSeconds=2
2026-04-01 10:15:02.173 [ENFORCE] RUNNING: WpnService PID=1936 HostedServices=[Appinfo, BITS, IpHlpSvc, LanmanServer, PushToInstall, Schedule, ShellHWDetection, Themes, TokenBroker, UserManager, Winmgmt, wlidsvc, WpnService, wuauserv] Action=STOPPING
2026-04-01 10:15:02.175 [ENFORCE] STOPPED: WpnService
2026-04-01 10:15:02.198 [ENFORCE] RUNNING: WpnUserService_7df85 PID=6916 HostedServices=[CDPUserSvc_7df85, PimIndexMaintenanceSvc_7df85, UnistoreSvc_7df85, UserDataSvc_7df85, WpnUserService_7df85] Action=STOPPING
2026-04-01 10:15:02.200 [ENFORCE] STOPPED: WpnUserService_7df85
```

## Build

Requires Python and PyInstaller.

```
pip install pywin32 pyinstaller
```

Build executable:

```
pyinstaller --clean --onefile --noconsole --uac-admin --icon=icon.ico main.py
```

## Run Automatically (Task Scheduler)

For best results, run **WpnService Watcher** automatically using **Windows Task Scheduler**.

### Recommended configuration

1. Open **Task Scheduler**

2. Click **Create Task**

3. In **General**

   * Name: `WpnService Watcher`
   * Select **Run only when user is logged on**
   * Enable **Run with highest privileges**

4. In **Triggers**

   * Add trigger: **At log on of any user**

5. In **Actions**

   * Action: **Start a program**
   * Program/script:

```
WpnService-Watcher.exe
```

6. In **Conditions**

   * Disable **Start the task only if the computer is on AC power**

7. In **Settings**

   * Enable **Allow task to be run on demand**
   * Enable **Run task as soon as possible after a scheduled start is missed**

This ensures the watcher starts automatically every time Windows boots.

## Disclaimer

Stopping Windows notification services may disable notifications for some applications.

Use at your own discretion.
