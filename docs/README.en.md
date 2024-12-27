# Sclat

Python-based YouTube video player with ASCII art functionality.

<p align="center">
    <img src="../asset/sclatLogo.png" width="248" alt="Sclat Logo">
</p>

## 🌐 언어 | Language

[한국어](README.md) | [English](../docs/README.en.md)

## ⚙️ Requirements

> **Important**: pytubefix must be version 7.1rc2 for streaming video compatibility

-   Python 3.8+
-   pygame
-   OpenCV (cv2)
-   numpy
-   moviepy == 1.0.3
-   chardet == 5.2.0
-   pytubefix == 7.1rc2
-   pyvidplayer2 == 0.9.24
-   yt_dlp == 2024.8.6

See requirements.txt for more information.

## 🌟 Key Features

-   YouTube video playback and download functionality
-   Real-time ASCII art conversion mode
-   Intuitive keyboard controls
-   YouTube subtitle loading functionality
-   Video search functionality
-   Volume and playback control
-   GUI and CLI interfaces
-   Discord RPC functionality
-   with watch video functionality

## 🚀 How to Run

### Installation

**Windows**

```batch
install.bat
```

**Terminal**

```bash
install.sh
```

### Usage

**Windows**

```batch
# GUI mode
start.bat
```

**Terminal**

```bash
# GUI mode
start.sh

# CLI mode
start.sh --nogui

# Single playback
start.sh --once

# Playlist mode
start.sh --nogui --play [URL1] [URL2]...


# client mode (beta)
start.sh --with-play-client

# server mode (beta)
start.sh --with-play-server
```

## 🎮 Video Controls

### Playback Control

| Key | Function          |
| --- | ----------------- |
| `S` | Seek video        |
| `R` | Restart video     |
| `P` | Play/Pause        |
| `M` | Mute/Unmute       |
| `L` | Toggle loop       |
| `A` | Toggle ASCII mode |

### Navigation

| Key | Function        |
| --- | --------------- |
| `↑` | Increase volume |
| `↓` | Decrease volume |
| `←` | Rewind 15s      |
| `→` | Forward 15s     |

### Function

| Key   | Function                |
| ----- | ----------------------- |
| `esc` | Return to search screen |
| `f11` | Fullscreen              |

## 🔍 Search Interface

-   Enter video URL or search term
-   Paste URL with `Ctrl+V`
-   Navigate results with arrow keys
-   Select and play with Enter

## 💬 Subtitle

**Steps to configure:**

1. Open the `setting/setting.json` file in the Sclat installation folder.
2. Change `"Subtitle-Lang": "~"` value to your desired language:

-   At this time, if you enter `none`, the subtitle function will be turned off.

    ```json
    {
        "Subtitle-Lang": "ko"
        // other settings...
    }
    ```

## ✨ Discord RPC

Sclat supports the Discord Rich Presence feature, which automatically displays the currently playing video information in your Discord status.

<p align="center">
    <img src="../asset/discordRPC.png" width="300" alt="Discord RPC image">
</p>

### How to enable Discord RPC

To use the Discord RPC feature, simply run the Discord program on your computer. If Discord is running, Sclat will automatically display the currently playing video information in the Discord status.

### How to Disable Discord RPC

To disable the Discord RPC feature, change the `discord_RPC` value to `false` in the `setting/setting.json` file. The default value is `true`.

**Steps to configure:**

1. Open the `setting/setting.json` file in the Sclat installation folder.
2. Change `"discord_RPC": true` to `"discord_RPC": false`:

    ```json
    {
        "discord_RPC": false
        // other settings...
    }
    ```

3. Save the file and restart the program.
