import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="BudgetWiser", page_icon="💰", layout="wide")

st.title("💰 BudgetWiser")
st.caption("Personal Budgeting Assistant")

page = st.sidebar.radio("Navigation", ["Dashboard", "Budget Planner", "About"])

if page == "Dashboard":
    st.header("Monthly Budget Dashboard")

    st.subheader("Income")
    income = st.number_input(
        "Monthly net income ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
    )

    st.subheader("Expenses")
    col1, col2 = st.columns(2)

    with col1:
        housing = st.number_input("Housing", min_value=0.0, value=0.0, step=10.0)
        transportation = st.number_input("Transportation", min_value=0.0, value=0.0, step=10.0)
        insurance = st.number_input("Insurance", min_value=0.0, value=0.0, step=10.0)

    with col2:
        utilities = st.number_input("Utilities and phone", min_value=0.0, value=0.0, step=10.0)
        groceries = st.number_input("Groceries", min_value=0.0, value=0.0, step=10.0)
        other = st.number_input("Other expenses", min_value=0.0, value=0.0, step=10.0)

    total_expenses = (housing + groceries + transportation + utilities + insurance + other)
    remaining = income - total_expenses

    st.divider()

    st.header("Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Income", f"${income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Margin", f"${remaining:,.2f}")

    if remaining < 0:
        st.error("You are spending more than your monthly income.")
    elif remaining == 0:
        st.warning("Your income is fully used by your expenses.")
    else:
        st.success(f"You have ${remaining:,.2f} remaining after expenses.")

    expense_data = pd.DataFrame({
        "Category": [
            "Housing",
            "Groceries",
            "Transportation",
            "Utilities and phone",
            "Insurance",
            "Other expenses",
        ],
        "Amount": [
            housing,
            groceries,
            transportation,
            utilities,
            insurance,
            other,
        ],
    })

    st.subheader("Expense Breakdown")
    fig = px.pie(
        expense_data,
        names="Category",
        values="Amount",
        title="Expense Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)

    summary_data = pd.DataFrame({
        "Category": [
            "Monthly Income",
            "Total Expenses",
            "Money Remaining",
        ],
        "Amount": [income, total_expenses, remaining],
    })

    st.subheader("Download Your Budget")
    st.download_button(
        label="Download Budget Summary as CSV",
        data=summary_data.to_csv(index=False),
        file_name="budgetwise_summary.csv",
        mime="text/csv",
    )

elif page == "Budget Planner":
    st.header("Budget Planner")
    st.write(
        "Use BudgetWise to organize your monthly income " "and expenses."
    )

    st.subheader("How to Use BudgetWise")
    st.write("1. Enter your monthly income.")
    st.write("2. Enter your monthly expenses.")
    st.write("3. Review your remaining money.")
    st.write("4. Use the chart to understand your spending.")
    st.write("5. Download your budget as a CSV file.")

elif page == "About":
    st.header("About BudgetWise")
    st.write(
        "BudgetWise is a personal budgeting assistant that helps "
        "users manage their monthly income and expenses."
    )

    st.subheader("Project Goals")
    st.write("- Create a simple monthly budget.")
    st.write("- Calculate expenses and remaining money.")
    st.write("- Visualize spending with a chart.")
    st.write("- Support future analysis of financial data.")

    st.caption("Developed as a DTSC 201 semester project.")
