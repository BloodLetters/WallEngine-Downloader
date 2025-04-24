# WallEngine-Downloader

WallEngine-Downloader is a simple GUI-based application for downloading wallpapers from the Wallpaper Engine Workshop page on Steam **without requiring an owned Steam account or the Wallpaper Engine app itself**.

## Features

- **Download Workshop Wallpapers**: Enter the Workshop URL, choose your download location, and grab wallpapers without Steam ownership restrictions.
- **User-Friendly GUI**: No need to deal with command line tools—just point, click, and download.
- **Automatic Extraction**: Downloaded wallpapers are extracted and ready to use right away in wallpaper engine program.

## How It Works

This project uses [DepotDownloaderMod](https://github.com/SteamAutoCracks/DepotDownloaderMod/) under the hood, which allows downloading Steam Workshop content even if you don't own the actual game or application.

## Installation & Usage

WallEngine-Downloader can be used in **two ways**:

### 1. Using the Compiled Release (Recommended)

For the easiest experience, use the pre-built executable from the [Releases tab](https://github.com/BloodLetters/WallEngine-Downloader/releases).  
**DepotDownloaderMod is already included**—no need for manual setup.

**Steps:**
1. Download the latest release for your OS from the [Releases page](https://github.com/BloodLetters/WallEngine-Downloader/releases).
2. Extract the files.
3. Run the `WallEngine-Downloader.exe`.
4. Use the GUI to download wallpapers directly.

### 2. Running Manually (Manual Mode)

If you prefer or need to run the Python source code directly, you **must download DepotDownloaderMod separately**.

**Steps:**
1. Clone this repository:
    ```bash
    git clone https://github.com/BloodLetters/WallEngine-Downloader.git
    cd WallEngine-Downloader
    ```
2. Set up dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Download [DepotDownloaderMod](https://github.com/SteamAutoCracks/DepotDownloaderMod/releases) and extract it to a folder.
4. Make sure all file in the `DepotDownloaderMod` in folder.  copy it into the WallEngine-Downloader directory.
5. Run the application:
    ```bash
    python main.py
    ```

## Usage

1. Launch the app (either the compiled .exe or with `python app.py`).
2. Enter the Workshop wallpaper URL or ID you want to download.
3. Choose where to save the downloaded wallpaper.
4. Click the "Download" button.
5. The wallpaper will be downloaded and extracted automatically.

## Hard Dependency

- [DepotDownloaderMod](https://github.com/SteamAutoCracks/DepotDownloaderMod/)
    - **Included in the compiled release.**
    - **Required separately for manual mode.**

## Screenshot

![image](https://github.com/user-attachments/assets/ebc3505d-f370-441f-aae7-7418c7e8a3ab)
![image](https://github.com/user-attachments/assets/8aa16af8-c16d-4189-99a8-7429df13ea51)


## Notes

- No Steam login is required.
- For personal and educational use only.
- Please comply with Steam and Wallpaper Engine's Terms of Service.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Contributions and feedback are welcome!**
