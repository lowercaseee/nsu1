# NSU Audit Mobile - App Specification

## Overview
Mobile version of NSU Audit Core for Android - Student Graduation Eligibility Checker

## Features

### 1. Login Screen
- NSU branded design (Blue/Gold colors)
- Logo display
- "Sign in with Google" button (simulated)
- Secure login message

### 2. Dashboard
- GRADUATED status banner
- Credits: 130 / 130
- CGPA display
- Course count
- Quick action buttons

### 3. Certificate PDF Download
- Full PDF certificate with NSU branding
- Student name, credits, CGPA, status
- Save to device downloads

### 4. Transcript PDF Download  
- Full transcript with all courses
- NSU header with logo
- Student info and course list
- Save to device downloads

### 5. Grades Breakdown Tab
- Grade distribution chart/text
- A, A-, B+, B, etc. counts
- Percentage breakdown

### 6. History Tab
- Login history display
- Date, credits, CGPA, status per entry
- Shows recent audit sessions

### 7. Logout
- Return to login screen
- Session end

## Technical Stack
- Kivy Framework
- ReportLab (PDF generation)
- Pillow (Image handling)

## Build
- Buildozer for Android APK
- Python 3.9+
