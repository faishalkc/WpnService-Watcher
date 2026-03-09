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

## Build

Requires Python and PyInstaller.

```
pip install pywin32 pyinstaller
```

Build executable:

```
pyinstaller --clean --onefile --noconsole --uac-admin --icon=icon.ico main.py
```

## Disclaimer

Stopping Windows notification services may disable notifications for some applications.

Use at your own discretion.
