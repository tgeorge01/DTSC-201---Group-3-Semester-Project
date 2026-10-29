import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="BudgetWiser", page_icon="💰", layout="centered"
)

st.title("💰 BudgetWiser Personal Budget Assistant")
st.write(
    "Organize your monthly cash flow and plan your long-term financial goals."
)

# --- INCOMES & ESSENTIALS ---
st.header("1. Income & Living Expenses")
income = st.number_input(
    "What is your net monthly income ($)?",
    min_value=0,
    value=5000,
    step=100,
    key="income_input",
)

st.subheader("Essential Living Expenses")
phone = st.number_input(
    "Phone bill", min_value=0, value=75, step=5, key="phone_input"
)
groceries = st.number_input(
    "Groceries", min_value=0, value=400, step=25, key="groceries_input"
)
gas = st.number_input(
    "Gasoline and vehicle maintenance",
    min_value=0,
    value=200,
    step=25,
    key="gas_input",
)
rent = st.number_input(
    "Rent or house payment", min_value=0, value=1500, step=50, key="rent_input"
)
insurance = st.number_input(
    "Insurance (health, home, car)",
    min_value=0,
    value=200,
    step=25,
    key="insurance_input",
)
debt_repayment = st.number_input(
    "Debt repayment (student loans, mortgage)",
    min_value=0,
    value=300,
    step=25,
    key="debt_input",
)
essential_other = st.number_input(
    "Other essentials",
    min_value=0,
    value=50,
    step=10,
    key="essential_other_input",
)

essentials = [
    phone,
    groceries,
    gas,
    rent,
    insurance,
    debt_repayment,
    essential_other,
]
total_essentials = sum(essentials)
percent_essential = (
    round((total_essentials / income) * 100) if income > 0 else 0
)
margin = income - total_essentials

st.info(
    f"Your living expenses total **${total_essentials:,}**, which is **{percent_essential}%** of your income. Remaining margin: **${margin:,}**"
)

# --- NON-ESSENTIALS ---
st.header("2. Non-Essentials / Fun Money")
nonessentials = st.number_input(
    "How much are you willing to spend on non-essentials (restaurants, leisure, etc.)?",
    min_value=0,
    max_value=max(0, margin),
    value=min(300, max(0, margin)),
    step=50,
    key="nonessentials_input",
)
margin -= nonessentials

st.info(f"Your updated margin after non-essentials is **${margin:,}**.")

# --- LONG-TERM GOALS ---
st.header("3. Long-Term Goals & Savings")
st.write(
    "Allocate your remaining margin toward your future security and investments."
)

emergency_fund = st.number_input(
    "Emergency fund (3-6 months living expenses)",
    min_value=0,
    max_value=max(0, margin),
    value=min(200, max(0, margin)),
    step=50,
    key="emergency_input",
)
extra_debt = st.number_input(
    "Extra debt repayment",
    min_value=0,
    max_value=max(0, margin - emergency_fund),
    value=0,
    step=50,
    key="extra_debt_input",
)
retirement = st.number_input(
    "Retirement savings",
    min_value=0,
    max_value=max(0, margin - emergency_fund - extra_debt),
    value=min(300, max(0, margin - emergency_fund - extra_debt)),
    step=50,
    key="retirement_input",
)
savings = st.number_input(
    "General savings (goals, vacations, car)",
    min_value=0,
    max_value=max(0, margin - emergency_fund - extra_debt - retirement),
    value=0,
    step=50,
    key="savings_input",
)
investments = st.number_input(
    "Investments (stocks, real estate)",
    min_value=0,
    max_value=max(
        0, margin - emergency_fund - extra_debt - retirement - savings
    ),
    value=0,
    step=50,
    key="investments_input",
)
charity = st.number_input(
    "Charity / Giving",
    min_value=0,
    max_value=max(
        0,
        margin
        - emergency_fund
        - extra_debt
        - retirement
        - savings
        - investments,
    ),
    value=0,
    step=50,
    key="charity_input",
)
long_term_other = st.number_input(
    "Other long-term allocation",
    min_value=0,
    max_value=max(
        0,
        margin
        - emergency_fund
        - extra_debt
        - retirement
        - savings
        - investments
        - charity,
    ),
    value=0,
    step=50,
    key="long_term_other_input",
)

long_term = [
    emergency_fund,
    extra_debt,
    retirement,
    savings,
    investments,
    charity,
    long_term_other,
]
total_long_term = sum(long_term)
ending_balance = margin - total_long_term

if ending_balance == 0:
    st.success("Congrats! Your full income has been budgeted.")
else:
    st.warning(
        f"You have **${ending_balance:,}** remaining unallocated margin. Consider putting it into your emergency fund!"
    )

# --- CASH FLOW BREAKDOWN & PIE CHART ---
st.header("4. Cash Flow Breakdown")

categories = []
amounts = []

if total_essentials > 0:
    categories.append("Living Essentials")
    amounts.append(total_essentials)

if nonessentials > 0:
    categories.append("Non-Essentials")
    amounts.append(nonessentials)

long_term_labels = [
    "Emergency Fund",
    "Extra Debt Repayment",
    "Retirement",
    "Savings",
    "Investments",
    "Charity",
    "Other Goals",
]
for label, amt in zip(long_term_labels, long_term):
    if amt > 0:
        categories.append(label)
        amounts.append(amt)

if ending_balance > 0:
    categories.append("Unallocated Margin")
    amounts.append(ending_balance)

if sum(amounts) > 0:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Paired.colors,
    )
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.write("Enter your budget details above to generate the breakdown chart.")
