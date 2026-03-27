# NSU Audit Core - Mobile App

Mobile version of NSU Audit Core for Android - Student Graduation Eligibility Checker

## Features

- Login screen with NSU branding
- Dashboard with GRADUATED status, 130 credits, CGPA
- 51 courses displayed
- Download Certificate PDF
- Download Transcript PDF
- Grades breakdown with visual bars
- Login history tracking
- Logout functionality

## Files

```
NSU Audit Mobile/
├── main.py           # Main Kivy app
├── buildozer.spec    # Android build configuration
├── requirements.txt  # Python dependencies
├── spec.md          # App specification
└── README.md       # This file
```

## How to Build APK

### 1. Install Python Dependencies

```bash
pip install kivy>=2.3.0 reportlab Pillow buildozer
```

### 2. Test on PC (Optional)

```bash
python main.py
```

### 3. Build Android APK

```bash
buildozer android debug
```

The APK will be in: `bin/nsuauditcore-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`

### 4. Install on Phone

1. Transfer APK to phone (USB, email, etc.)
2. Enable "Install from unknown sources" in phone settings
3. Open the APK file
4. Tap Install

## App Screens

1. **Login Screen** - NSU branded login page
2. **Dashboard** - Status card with GRADUATED, credits, CGPA
3. **Courses Tab** - Scrollable list of all 51 courses
4. **Grades Tab** - Grade distribution with visual bars
5. **History Tab** - Login history with dates

## Technical Details

- **Framework**: Kivy 2.3.0+
- **PDF Generation**: ReportLab
- **Image Handling**: Pillow
- **Target**: Android (API 21+)

## Notes

- Login is simulated (no real Google OAuth in mobile version)
- PDFs save to Downloads folder on Android
- Student name/email shown as placeholder (update in main.py)
