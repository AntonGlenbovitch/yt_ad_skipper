# 🎬 YouTube Ad Skipper (macOS M1/M2/M3)

Automatically skip YouTube ads using Python + Selenium.

## 🚀 How It Works
- Launches Chrome using your saved Chrome profile
- Loads the video
- Detects and skips ads automatically

## 🛠 Setup

I suggest using conda to set up runtime env.

💡 Notes
    You must download the ARM64 ChromeDriver
    Tested on macOS M3, Python 3.11, Chrome 114+

bash
pip install -r requirements.txt
export CHROMEDRIVER_PATH=/your/path/to/chromedriver
export CHROME_USER_DATA_DIR=/your/path/to/chrome-profile
python yt_skip.py

# yt_skip Minimal ChromeDriver Test

NOTE: this app will only monitor for one Crome browser instance. 
      You have to start this app via terminal, and kill using the same terminal with "Ctl + C" 

How It Works
   Kills any lingering chromedriver processes.
   Launches Google Chrome in controlled mode with your saved profile.
   Loads the specified YouTube video.
   Triggers playback and unmutes the video.
   Periodically scans for:
   kippable video ads and clicks the "Skip" button.
   Overlay ads and clicks the "Close" (X) button.
   Runs indefinitely until you press Ctrl + C or close the browser.

##  Setup Instructions (Apple Silicon)
macOS (M1/M2/M3) ARM64

- Python 3.9+ (Tested with 3.10) - don't use higher verision as app may not be stable.
- Google Chrome (latest version)
- ChromeDriver (Apple Silicon build)
- Chrome user data profile (optional)

1. Download matching ARM64 ChromeDriver for Chrome version 138.0.7204.93:
   https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/138.0.7204.93/mac-arm64/chromedriver-mac-arm64.zip

2. Unzip and move it to this folder:
   bash
   unzip chromedriver-mac-arm64.zip
   mv chromedriver-mac-arm64/chromedriver /Users/ag/projects/yt_skip/
   chmod +x chromedriver
   xattr -rd com.apple.quarantine chromedriver
   
3. Check chromedriver version (make sure it arm64) 
   bash
   - project_home=$(pwd)
   - $project_home/chromedriver --version
      ChromeDriver 138.0.7204.93 (6ba765882015a451663f48e7c0330d883250061c-refs/branch-heads/7204_50@{#9})

5. Make sure chromedriver is binary executable
   - chmod +x /Users/ag/projects/yt_skip/chromedriver

4. Install dependencies:
   bash:
   pip install -r requirements.txt
   

5. Run the test:
   bash:
   python yt_skip.py
   

10:30:03 [INFO] Killing any old ChromeDriver processes...
10:30:03 [INFO] Killed existing chromedriver processes.
10:30:03 [INFO] Launching Chrome browser...
10:30:12 [INFO] Video unmuted and playback started.
10:30:12 [INFO] Watching for ads... Press Ctrl+C or close browser to exit.
10:32:14 [INFO] Skipped video ad.

Expected: Chrome opens and loads https://example.com for 5 seconds.
