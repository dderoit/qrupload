# QRUpload

## Instantly Share Files via QR Code — Right from Your Terminal

**QRUpload** is a simple Python utility that lets you instantly share any file by uploading it to [tmpfiles.org](https://tmpfiles.org) and generating a scannable QR code in your terminal.

Uploaded files expire after **1 hour**, making it perfect for quick, temporary sharing.

----------

## 🚀 Features

-   🖱️ Pick a file via CLI or use a GUI file picker
    
-   ☁️ Uploads securely to tmpfiles.org
    
-   📱 Instantly get a QR code you can scan or share
    
-   🕐 Auto-expiry in 1 hour for security and convenience
    

----------

## 📦 Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

----------

## 🛠️ Usage

```bash
qr [filepath]
```

-   If you provide a file path, it will be uploaded directly.
    
-   If you don’t, a file picker will appear to let you choose a file interactively.
    

----------

## 🧭 Tip: Add to PATH

To use `qr` from anywhere:

1.  Add the script’s directory to your `PATH`.
2.  Optionally, on Linux, create an alias for even quicker access. On Windows, there is no need; it is already provided.
----------

## 📝 Notes

-   Make sure you trust the content you’re uploading — files are public via link.
    
-   Perfect for quick sharing between devices without needing email, AirDrop, or USBs.

