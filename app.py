import json
import random
import string
import streamlit as st
from pathlib import Path

# ── Bank Core ────────────────────────────────────────────────────────────────

class Bank:
    DATABASE = "data.json"

    @classmethod
    def _load(cls):
        if Path(cls.DATABASE).exists():
            with open(cls.DATABASE) as f:
                return json.loads(f.read())
        return []

    @classmethod
    def _save(cls, data):
        with open(cls.DATABASE, "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def _generate_account():
        parts = random.choices(string.ascii_letters, k=3) + \
                random.choices(string.digits, k=3) + \
                random.choices("!@#$%^&*", k=1)
        random.shuffle(parts)
        return "".join(parts)

    @classmethod
    def _find_user(cls, acc, pin):
        data = cls._load()
        match = [u for u in data if u["account No."] == acc and u["pin"] == pin]
        return data, match

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18:
            return False, "Age must be 18 or above."
        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits."
        data = cls._load()
        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account No.": cls._generate_account(),
            "balance": 0,
        }
        data.append(account)
        cls._save(data)
        return True, account

    @classmethod
    def deposit(cls, acc, pin, amount):
        data, match = cls._find_user(acc, pin)
        if not match:
            return False, "Invalid account number or PIN."
        if amount <= 0 or amount > 10000:
            return False, "Deposit must be between ₹1 and ₹10,000."
        match[0]["balance"] += amount
        cls._save(data)
        return True, match[0]["balance"]

    @classmethod
    def withdraw(cls, acc, pin, amount):
        data, match = cls._find_user(acc, pin)
        if not match:
            return False, "Invalid account number or PIN."
        if amount <= 0:
            return False, "Amount must be positive."
        if amount > match[0]["balance"]:
            return False, "Insufficient balance."
        match[0]["balance"] -= amount
        cls._save(data)
        return True, match[0]["balance"]

    @classmethod
    def get_details(cls, acc, pin):
        _, match = cls._find_user(acc, pin)
        if not match:
            return False, "Invalid account number or PIN."
        return True, match[0]

    @classmethod
    def update_details(cls, acc, pin, name=None, email=None, new_pin=None):
        data, match = cls._find_user(acc, pin)
        if not match:
            return False, "Invalid account number or PIN."
        if name:
            match[0]["name"] = name
        if email:
            match[0]["email"] = email
        if new_pin:
            if len(str(new_pin)) != 4:
                return False, "New PIN must be exactly 4 digits."
            match[0]["pin"] = new_pin
        cls._save(data)
        return True, "Details updated successfully."

    @classmethod
    def delete_account(cls, acc, pin):
        data, match = cls._find_user(acc, pin)
        if not match:
            return False, "Invalid account number or PIN."
        data.remove(match[0])
        cls._save(data)
        return True, "Account deleted successfully."


# ── Streamlit UI ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="Anix_Bank", page_icon="🏦", layout="centered")

# Header / Logo
st.markdown(
    """
    <div style='text-align:center; padding: 10px 0 20px 0'>
        <span style='font-size:52px'>🏦</span>
        <h1 style='margin:0; color:#1a73e8; font-size:2.5rem; letter-spacing:2px'>AnixBank</h1>
        <p style='color:gray; margin:0'>Your Trusted Digital Bank</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

menu = st.sidebar.selectbox(
    "📋 Menu",
    ["🏠 Home", "➕ Create Account", "💰 Deposit", "💸 Withdraw", "📄 Account Details", "✏️ Update Details", "🗑️ Delete Account"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("<small style='color:gray'>AnixBank © 2026</small>", unsafe_allow_html=True)


def acc_pin_inputs():
    acc = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999, step=1, format="%d")
    return acc, int(pin)


# ── Pages ─────────────────────────────────────────────────────────────────────

if menu == "🏠 Home":
    st.subheader("Welcome to AnixBank 👋")
    st.info("Use the sidebar to navigate between features.")
    cols = st.columns(3)
    cols[0].metric("Feature", "Secure PIN")
    cols[1].metric("Feature", "Instant Transfer")
    cols[2].metric("Feature", "24/7 Access")

elif menu == "➕ Create Account":
    st.subheader("Create New Account")
    with st.form("create_form"):
        name  = st.text_input("Full Name")
        age   = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email")
        pin   = st.number_input("4-digit PIN", min_value=1000, max_value=9999, step=1, format="%d")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        ok, result = Bank.create_account(name, int(age), email, int(pin))
        if ok:
            st.success("✅ Account created successfully!")
            st.warning("📌 Save your Account Number — you'll need it to log in.")
            st.json({k: v for k, v in result.items() if k != "pin"})
        else:
            st.error(f"❌ {result}")

elif menu == "💰 Deposit":
    st.subheader("Deposit Money")
    with st.form("deposit_form"):
        acc, pin = acc_pin_inputs()
        amount = st.number_input("Amount (max ₹10,000)", min_value=1, max_value=10000, step=1)
        submitted = st.form_submit_button("Deposit")

    if submitted:
        ok, result = Bank.deposit(acc, pin, int(amount))
        if ok:
            st.success(f"✅ Deposited ₹{amount}. New balance: ₹{result}")
        else:
            st.error(f"❌ {result}")

elif menu == "💸 Withdraw":
    st.subheader("Withdraw Money")
    with st.form("withdraw_form"):
        acc, pin = acc_pin_inputs()
        amount = st.number_input("Amount", min_value=1, step=1)
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        ok, result = Bank.withdraw(acc, pin, int(amount))
        if ok:
            st.success(f"✅ Withdrawn ₹{amount}. Remaining balance: ₹{result}")
        else:
            st.error(f"❌ {result}")

elif menu == "📄 Account Details":
    st.subheader("Account Details")
    with st.form("details_form"):
        acc, pin = acc_pin_inputs()
        submitted = st.form_submit_button("View Details")

    if submitted:
        ok, result = Bank.get_details(acc, pin)
        if ok:
            st.success("✅ Account found!")
            safe = {k: v for k, v in result.items() if k != "pin"}
            for k, v in safe.items():
                st.write(f"**{k.title()}:** {v}")
        else:
            st.error(f"❌ {result}")

elif menu == "✏️ Update Details":
    st.subheader("Update Account Details")
    with st.form("update_form"):
        acc, pin = acc_pin_inputs()
        st.caption("Leave fields blank to keep existing values.")
        new_name  = st.text_input("New Name (optional)")
        new_email = st.text_input("New Email (optional)")
        new_pin   = st.text_input("New PIN (optional, 4 digits)")
        submitted = st.form_submit_button("Update")

    if submitted:
        np = int(new_pin) if new_pin.strip() else None
        ok, result = Bank.update_details(acc, pin, new_name or None, new_email or None, np)
        if ok:
            st.success(f"✅ {result}")
        else:
            st.error(f"❌ {result}")

elif menu == "🗑️ Delete Account":
    st.subheader("Delete Account")
    st.warning("⚠️ This action is permanent and cannot be undone.")
    with st.form("delete_form"):
        acc, pin = acc_pin_inputs()
        confirm = st.checkbox("I understand this will permanently delete my account.")
        submitted = st.form_submit_button("Delete Account")

    if submitted:
        if not confirm:
            st.error("Please confirm deletion by checking the box.")
        else:
            ok, result = Bank.delete_account(acc, pin)
            if ok:
                st.success(f"✅ {result}")
            else:
                st.error(f"❌ {result}")
