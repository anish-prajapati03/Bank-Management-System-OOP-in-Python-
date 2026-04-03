# 🏦 AnixBank — Digital Bank Management System
🔗 Live Demo: https://anixbank.streamlit.app/

A simple yet fully functional bank management system built with **Python** and **Streamlit**, featuring a clean web-based UI.

---

## 📌 Features

| Feature | Description |
|---|---|
| ➕ Create Account | Register with name, age, email & 4-digit PIN |
| 💰 Deposit Money | Add funds (max ₹10,000 per transaction) |
| 💸 Withdraw Money | Withdraw with balance validation |
| 📄 Account Details | View your account info securely |
| ✏️ Update Details | Change name, email, or PIN |
| 🗑️ Delete Account | Permanently remove account with confirmation |

---

## 🗂️ Project Structure

```
Bank Management OOPs/
│
├── app.py          # Main Streamlit app (UI + Bank logic)
├── main.py         # Original CLI version
├── data.json       # Local database (auto-created)
└── README.md       # Project documentation
```

---

## ⚙️ Requirements

- Python 3.8+
- Streamlit

---

## 🚀 Getting Started

### 1. Clone or Download the project

```bash
cd "c:\PYTHON\Bank Management OOPs"
```

### 2. Install dependencies

```bash
pip install streamlit
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

To stop the app press `Ctrl + C` in the terminal.

---

## 🧠 How It Works

### Account Creation
- Must be **18 years or older**
- PIN must be exactly **4 digits**
- A unique **Account Number** is auto-generated (mix of letters, digits & special characters)
- All data is saved to `data.json`

### Authentication
- Every operation (deposit, withdraw, view, update, delete) requires your **Account Number + PIN**

### Data Storage
- All accounts are stored locally in `data.json`
- No external database required

---

## 🔐 Security Notes

- PIN is never displayed in the UI
- Account deletion requires an explicit confirmation checkbox
- Each operation re-validates credentials before making changes

---

## 🐛 Bugs Fixed (from original CLI version)

| Bug | Fix |
|---|---|
| `Delete` method was nested inside `updatedetails` | Moved to correct indentation level |
| `if userdata == False` doesn't work for lists | Fixed to `if not match` |
| `if check == "n" or "N"` always evaluated `True` | Replaced with Streamlit checkbox confirmation |
| Stale in-memory data across operations | Data is now loaded fresh on every operation |

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **UI Framework:** Streamlit
- **Storage:** JSON file (local)
- **Libraries:** `json`, `random`, `string`, `pathlib`

---

## 👨‍💻 Author

Built as an OOP learning project — improved with Streamlit for a better user experience.

⭐ Support

If you like this project, please ⭐ the repository!
