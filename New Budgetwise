import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date
import html
import math

st.set_page_config(
    page_title="BudgetWise",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    h1, h2, h3 {
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.18);
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stProgressBar"] {
        height: 14px;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# BLS annual spending data
bls_annual = {
    "Food": 10633,
    "Alcoholic Beverages": 630,
    "Housing": 27790,
    "Apparel and Services": 2010,
    "Transportation": 13492,
    "Healthcare": 6470,
    "Entertainment": 4084,
    "Personal Care": 986,
    "Reading": 114,
    "Education": 1583,
    "Tobacco Products": 365,
    "Miscellaneous": 1335,
    "Cash Contributions": 2237,
    "Personal Insurance and Pensions": 10175
}

bls_monthly = {
    category: amount / 12
    for category, amount in bls_annual.items()
}


# Expense categories
categories = list(bls_annual.keys())


# Three rotating example budgets
budget_profiles = [
    {
        "income": 2500,
        "expenses": {
            "Food": 350,
            "Alcoholic Beverages": 0,
            "Housing": 1000,
            "Apparel and Services": 50,
            "Transportation": 200,
            "Healthcare": 100,
            "Entertainment": 50,
            "Personal Care": 30,
            "Reading": 10,
            "Education": 50,
            "Tobacco Products": 0,
            "Miscellaneous": 40,
            "Cash Contributions": 20,
            "Personal Insurance and Pensions": 100
        }
    },
    {
        "income": 4200,
        "expenses": {
            "Food": 650,
            "Alcoholic Beverages": 35,
            "Housing": 1450,
            "Apparel and Services": 150,
            "Transportation": 400,
            "Healthcare": 250,
            "Entertainment": 180,
            "Personal Care": 65,
            "Reading": 20,
            "Education": 150,
            "Tobacco Products": 0,
            "Miscellaneous": 100,
            "Cash Contributions": 75,
            "Personal Insurance and Pensions": 300
        }
    },
    {
        "income": 3200,
        "expenses": {
            "Food": 300,
            "Alcoholic Beverages": 0,
            "Housing": 850,
            "Apparel and Services": 60,
            "Transportation": 175,
            "Healthcare": 90,
            "Entertainment": 75,
            "Personal Care": 35,
            "Reading": 10,
            "Education": 60,
            "Tobacco Products": 0,
            "Miscellaneous": 35,
            "Cash Contributions": 40,
            "Personal Insurance and Pensions": 150
        }
    }
]


# Load a different example budget for each new session
if "profile_loaded" not in st.session_state:
    profile_file = Path(__file__).with_name("profile_index.txt")

    try:
        profile_number = int(profile_file.read_text().strip())
    except (FileNotFoundError, ValueError, OSError):
        profile_number = 0

    profile_number = profile_number % len(budget_profiles)
    selected_profile = budget_profiles[profile_number]

    st.session_state.income = selected_profile["income"]

    for category in categories:
        key = "expense_" + category
        st.session_state[key] = selected_profile["expenses"][category]

    next_profile = (profile_number + 1) % len(budget_profiles)

    try:
        profile_file.write_text(str(next_profile))
    except OSError:
        pass

    st.session_state.profile_loaded = True


# Keep history during the current session
if "budget_history" not in st.session_state:
    st.session_state.budget_history = []


# Rule-based recommendations
def get_recommendations(income, expenses, total_expenses, remaining):

    recommendations = []

    if income <= 0:
        return ["Enter a monthly income greater than $0 to receive budget recommendations."]

    if total_expenses == 0:
        return ["Start entering your monthly expenses to receive recommendations."]

    if total_expenses > income:
        recommendations.append(
            "Your expenses are higher than your income. Review your spending and look for categories where you can reduce costs."
        )

        recommendations.append(
            "Separate essential expenses, such as housing and food, from optional expenses, such as entertainment and nonessential shopping."
        )

    savings_percentage = (remaining / income) * 100

    if remaining >= 0 and savings_percentage < 10:
        recommendations.append(
            "Your remaining balance is less than 10% of your income. Try setting a weekly spending limit and building a larger savings buffer."
        )

    elif remaining >= 0 and savings_percentage < 20:
        recommendations.append(
            "You have some money remaining. Consider gradually increasing the amount you put into savings each month."
        )

    elif remaining >= 0 and savings_percentage >= 20:
        recommendations.append(
            "You have a healthy amount remaining after expenses. Consider building an emergency fund or increasing your savings."
        )

        recommendations.append(
            "An automatic transfer to savings after payday can help you stay consistent."
        )

    housing = expenses.get("Housing", 0)

    if housing > income * 0.35:
        recommendations.append(
            "Housing takes up more than 35% of your income. Review rent, utilities, and other housing costs to see where you may be able to save."
        )

    elif housing > income * 0.25:
        recommendations.append(
            "Housing is taking up more than 25% of your income. Keep track of housing costs so they do not become difficult to manage."
        )

    food = expenses.get("Food", 0)

    if food > income * 0.20:
        recommendations.append(
            "Food spending is more than 20% of your income. Meal planning, grocery lists, and comparing prices may help lower costs."
        )

    transportation = expenses.get("Transportation", 0)

    if transportation > income * 0.15:
        recommendations.append(
            "Transportation is taking up more than 15% of your income. Review fuel, maintenance, insurance, and transportation costs."
        )

    entertainment = expenses.get("Entertainment", 0)

    if entertainment > 0 and total_expenses > 0:
        if entertainment / total_expenses > 0.15:
            recommendations.append(
                "Entertainment makes up more than 15% of your expenses. Review subscriptions and consider lower-cost activities."
            )

    if remaining >= 0 and remaining < 100:
        recommendations.append(
            "You have less than $100 remaining. Try keeping a small buffer for unexpected expenses."
        )

    if total_expenses > 0:
        largest_category = max(expenses, key=expenses.get)
        largest_amount = expenses[largest_category]

        if largest_amount / total_expenses >= 0.40:
            recommendations.append(
                largest_category + " makes up at least 40% of your total spending. Review this category to see whether any costs can be reduced."
            )

    # Compare spending with BLS averages
    for category in categories:
        amount = expenses.get(category, 0)
        average = bls_monthly[category]

        if amount > average * 1.20 and amount - average > 50:
            recommendations.append(
                category + " is noticeably higher than the national monthly average used by BudgetWise. Review this category for possible savings."
            )

    if not recommendations:
        recommendations.append(
            "Your spending does not currently trigger any of the BudgetWise spending guidelines. Keep monitoring your expenses."
        )

    return recommendations


# Spending alerts
def get_alerts(income, expenses, total_expenses, remaining):

    alerts = []

    if income <= 0:
        return alerts

    if total_expenses > income:
        alerts.append(
            ("error", "Your expenses exceed your monthly income.")
        )

    elif remaining >= 0 and remaining < income * 0.10:
        alerts.append(
            ("warning", "Less than 10% of your income remains after expenses.")
        )

    housing = expenses.get("Housing", 0)

    if housing > income * 0.35:
        alerts.append(
            ("warning", "Housing costs are above 35% of your income.")
        )

    food = expenses.get("Food", 0)

    if food > income * 0.20:
        alerts.append(
            ("warning", "Food spending is above 20% of your income.")
        )

    transportation = expenses.get("Transportation", 0)

    if transportation > income * 0.15:
        alerts.append(
            ("warning", "Transportation spending is above 15% of your income.")
        )

    if total_expenses > 0:
        largest_category = max(expenses, key=expenses.get)

        if expenses[largest_category] / total_expenses >= 0.40:
            alerts.append(
                ("info", largest_category + " accounts for at least 40% of your expenses.")
            )

    return alerts


# Comparison chart
def create_comparison_chart(expenses):

    comparison_data = pd.DataFrame({
        "Category": categories,
        "National Average": [
            bls_monthly[category] for category in categories
        ],
        "Your Expenses": [
            expenses[category] for category in categories
        ]
    })

    chart_data = comparison_data.melt(
        id_vars="Category",
        var_name="Spending Type",
        value_name="Amount"
    )

    fig = px.bar(
        chart_data,
        x="Category",
        y="Amount",
        color="Spending Type",
        barmode="group",
        color_discrete_map={
            "National Average": "#A0A0A0",
            "Your Expenses": "#1769AA"
        },
        title="Your Expenses Compared to National Averages"
    )

    fig.update_layout(
        xaxis_title="Expense Category",
        yaxis_title="Monthly Amount ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827", size=12),
        title_font=dict(color="#111827", size=19),
        legend_title_text="",
        xaxis=dict(
            tickangle=-35,
            tickfont=dict(color="#111827")
        ),
        yaxis=dict(
            tickfont=dict(color="#111827"),
            gridcolor="#E5E7EB"
        ),
        margin=dict(l=20, r=20, t=60, b=100)
    )

    return fig


# Personal spending chart
def create_personal_chart(expenses):

    chart_data = pd.DataFrame({
        "Category": categories,
        "Amount": [expenses[category] for category in categories]
    })

    chart_data = chart_data[chart_data["Amount"] > 0]

    if chart_data.empty:
        return None

    dark_theme = st.get_option("theme.base") == "dark"

    text_color = "#FFFFFF" if dark_theme else "#111827"

    fig = px.pie(
        chart_data,
        names="Category",
        values="Amount",
        hole=0.58,
        title="Your Monthly Spending",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(size=13, color=text_color),
        hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.2f}<extra></extra>"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color, size=13),
        title_font=dict(color=text_color, size=19),
        legend=dict(
            font=dict(color=text_color, size=11)
        ),
        margin=dict(l=10, r=10, t=55, b=10),
        annotations=[
            dict(
                text="Total",
                x=0.5,
                y=0.54,
                font=dict(size=15, color=text_color),
                showarrow=False
            )
        ]
    )

    return fig


# Create a downloadable HTML budget report
def create_budget_report(
    income,
    expenses,
    total_expenses,
    remaining,
    savings_goal,
    current_savings,
    recommendations,
    alerts
):

    rows = ""

    for category in categories:
        amount = expenses[category]
        average = bls_monthly[category]

        rows += f"""
        <tr>
            <td>{html.escape(category)}</td>
            <td>${amount:,.2f}</td>
            <td>${average:,.2f}</td>
        </tr>
        """

    recommendation_html = "".join(
        "<li>" + html.escape(item) + "</li>"
        for item in recommendations
    )

    alert_html = "".join(
        "<li>" + html.escape(item[1]) + "</li>"
        for item in alerts
    )

    savings_progress = 0

    if savings_goal > 0:
        savings_progress = min(
            current_savings / savings_goal * 100,
            100
        )

    report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>BudgetWise Monthly Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 35px;
                color: #1f2937;
            }}
            h1, h2 {{
                color: #1769AA;
            }}
            .summary {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin: 20px 0;
            }}
            .box {{
                background: #f3f4f6;
                padding: 15px;
                border-radius: 8px;
                min-width: 150px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 15px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background: #1769AA;
                color: white;
            }}
            li {{
                margin-bottom: 8px;
            }}
            @media print {{
                body {{ margin: 15px; }}
            }}
        </style>
    </head>
    <body>
        <h1>BudgetWise Monthly Budget Report</h1>
        <p>Generated on {date.today().strftime("%B %d, %Y")}</p>

        <div class="summary">
            <div class="box">
                <b>Monthly Income</b>
                <h2>${income:,.2f}</h2>
            </div>
            <div class="box">
                <b>Total Expenses</b>
                <h2>${total_expenses:,.2f}</h2>
            </div>
            <div class="box">
                <b>Remaining Balance</b>
                <h2>${remaining:,.2f}</h2>
            </div>
        </div>

        <h2>Savings Goal</h2>
        <p>Current savings: ${current_savings:,.2f}</p>
        <p>Savings goal: ${savings_goal:,.2f}</p>
        <p>Goal progress: {savings_progress:.1f}%</p>

        <h2>Expense Breakdown</h2>
        <table>
            <tr>
                <th>Category</th>
                <th>Your Spending</th>
                <th>National Monthly Average</th>
            </tr>
            {rows}
        </table>

        <h2>Spending Alerts</h2>
        <ul>
            {alert_html if alert_html else "<li>No spending alerts were triggered.</li>"}
        </ul>

        <h2>BudgetWise Recommendations</h2>
        <ul>
            {recommendation_html}
        </ul>

        <p>
            National averages are based on Bureau of Labor Statistics
            Consumer Expenditure data. They are comparison figures,
            not required spending targets.
        </p>
    </body>
    </html>
    """

    return report


# Sidebar navigation
st.sidebar.title("💰 BudgetWise")
st.sidebar.caption("Your personal budgeting tool")

page = st.sidebar.radio(
    "Navigation",
    ["Budget Planner", "About BudgetWise"]
)

st.sidebar.divider()
st.sidebar.caption("Manage your money. Understand your spending.")


# About page
if page == "About BudgetWise":

    st.title("About BudgetWise")

    st.write(
        "BudgetWise is a budgeting application designed to help "
        "people understand their monthly income and expenses."
    )

    st.subheader("What BudgetWise Offers")

    st.markdown("""
    - **Budget planning:** Enter your monthly income and expenses.
    - **Spending analysis:** See where your money is going.
    - **National comparisons:** Compare your spending with national averages.
    - **Savings goals:** Track progress toward a personal savings goal.
    - **Spending alerts:** Identify areas that may need attention.
    - **Recommendations:** Receive suggestions based on your spending.
    - **Budget history:** Save and compare monthly budgets.
    - **Downloadable reports:** Keep a copy of your budget information.
    """)

    st.subheader("Where the Data Comes From")

    st.write(
        "BudgetWise uses spending information from the Bureau of "
        "Labor Statistics Consumer Expenditure data to calculate "
        "national monthly comparison averages."
    )

    st.markdown(
        "[View the Bureau of Labor Statistics data](https://www.bls.gov/news.release/cesan.nr0.htm)"
    )

    st.info(
        "National averages are general comparison figures. Actual "
        "spending can vary based on location, household size, income, "
        "and personal circumstances. BudgetWise recommendations are "
        "general budgeting guidelines, not financial advice."
    )


# Main Budget Planner
else:

    st.title("💰 BudgetWise")
    st.write(
        "Plan your monthly budget, understand your expenses, "
        "and work toward your savings goals."
    )

    st.divider()

    # Income input
    st.subheader("1. Monthly Income")

    income = st.number_input(
        "Enter your monthly income ($)",
        min_value=0.0,
        max_value=1000000.0,
        step=100.0,
        key="income"
    )

    # Expense inputs
    st.subheader("2. Monthly Expenses")

    st.write("Enter how much you spend in each category.")

    expense_columns = st.columns(2)

    expenses = {}

    for index, category in enumerate(categories):

        with expense_columns[index % 2]:

            expenses[category] = st.number_input(
                category + " ($)",
                min_value=0.0,
                max_value=1000000.0,
                step=10.0,
                key="expense_" + category
            )

    total_expenses = sum(expenses.values())
    remaining = income - total_expenses

    st.divider()

    # Budget summary
    st.subheader("3. Your Budget Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Monthly Income",
        f"${income:,.2f}"
    )

    col2.metric(
        "Total Expenses",
        f"${total_expenses:,.2f}"
    )

    col3.metric(
        "Remaining Balance",
        f"${remaining:,.2f}",
        delta=f"${remaining:,.2f}"
    )

    if income > 0:

        spending_percentage = total_expenses / income
        progress_value = min(spending_percentage, 1.0)

        st.write("**Monthly Income Used**")

        st.progress(progress_value)

        st.caption(
            f"You have used {spending_percentage * 100:.1f}% "
            "of your monthly income."
        )

        if total_expenses > income:
            st.error(
                f"You are over budget by ${total_expenses - income:,.2f}."
            )

        else:
            st.success(
                f"You have ${remaining:,.2f} remaining this month."
            )

    else:
        st.info("Enter your income to see your budget progress.")

    st.divider()

    # Savings goal
    st.subheader("4. Savings Goal")

    st.write(
        "Set a savings goal and track how close you are to reaching it."
    )

    savings_col1, savings_col2 = st.columns(2)

    with savings_col1:

        savings_goal = st.number_input(
            "Your savings goal ($)",
            min_value=0.0,
            max_value=1000000.0,
            value=1000.0,
            step=100.0,
            key="savings_goal"
        )

    with savings_col2:

        current_savings = st.number_input(
            "How much have you saved so far? ($)",
            min_value=0.0,
            max_value=1000000.0,
            value=0.0,
            step=50.0,
            key="current_savings"
        )

    if savings_goal > 0:

        savings_progress = min(
            current_savings / savings_goal,
            1.0
        )

        st.write("**Savings Goal Progress**")

        st.progress(savings_progress)

        st.write(
            f"${current_savings:,.2f} saved out of "
            f"${savings_goal:,.2f}"
        )

        if current_savings >= savings_goal:
            st.success("Congratulations! You reached your savings goal.")

        else:
            amount_needed = savings_goal - current_savings

            st.info(
                f"You need another ${amount_needed:,.2f} to reach your goal."
            )

            monthly_contribution = st.number_input(
                "How much can you save each month? ($)",
                min_value=0.0,
                max_value=1000000.0,
                value=100.0,
                step=25.0,
                key="monthly_contribution"
            )

            if monthly_contribution > 0:

                months_needed = math.ceil(
                    amount_needed / monthly_contribution
                )

                st.write(
                    f"At that rate, you could reach your goal in "
                    f"approximately {months_needed} month(s)."
                )

            else:
                st.caption(
                    "Enter a monthly savings amount to estimate "
                    "how long your goal may take."
                )

    else:
        st.info("Enter a savings goal greater than $0 to track progress.")

    st.divider()

    # Spending alerts
    st.subheader("5. Spending Alerts")

    alerts = get_alerts(
        income,
        expenses,
        total_expenses,
        remaining
    )

    if alerts:

        for alert_type, message in alerts:

            if alert_type == "error":
                st.error(message)

            elif alert_type == "warning":
                st.warning(message)

            else:
                st.info(message)

    else:
        st.success(
            "No spending alerts right now. Keep monitoring your budget."
        )

    st.divider()

    # Charts
    st.subheader("6. Spending Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        personal_chart = create_personal_chart(expenses)

        if personal_chart is not None:
            st.plotly_chart(
                personal_chart,
                use_container_width=True
            )
        else:
            st.info("Enter expenses to see your spending chart.")

    with chart_col2:

        st.markdown("**Budget Breakdown**")

        breakdown_data = pd.DataFrame({
            "Type": ["Expenses", "Remaining"],
            "Amount": [
                total_expenses,
                max(remaining, 0)
            ]
        })

        if income > 0:

            breakdown_chart = px.pie(
                breakdown_data,
                names="Type",
                values="Amount",
                hole=0.58,
                color="Type",
                color_discrete_map={
                    "Expenses": "#1769AA",
                    "Remaining": "#55A878"
                }
            )

            breakdown_chart.update_traces(
                textposition="inside",
                textinfo="label+percent"
            )

            dark_theme = st.get_option("theme.base") == "dark"
            text_color = "#FFFFFF" if dark_theme else "#111827"

            breakdown_chart.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_color),
                legend=dict(font=dict(color=text_color)),
                margin=dict(l=10, r=10, t=20, b=10)
            )

            st.plotly_chart(
                breakdown_chart,
                use_container_width=True
            )

        else:
            st.info("Enter your income to see your budget breakdown.")

    st.divider()

    # National comparison
    st.subheader("7. Compare Your Expenses to National Averages")

    st.write(
        "Compare your monthly spending with average monthly spending "
        "figures from the Bureau of Labor Statistics."
    )

    comparison_chart = create_comparison_chart(expenses)

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )

    comparison_table = pd.DataFrame({
        "Category": categories,
        "Your Expenses": [
            expenses[category] for category in categories
        ],
        "National Monthly Average": [
            bls_monthly[category] for category in categories
        ]
    })

    comparison_table["Difference"] = (
        comparison_table["Your Expenses"]
        - comparison_table["National Monthly Average"]
    )

    st.dataframe(
        comparison_table.style.format({
            "Your Expenses": "${:,.2f}",
            "National Monthly Average": "${:,.2f}",
            "Difference": "${:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "National averages are for comparison only. They are not "
        "recommended spending limits or personal budget targets."
    )

    st.divider()

    # Recommendations
    st.subheader("8. BudgetWise Recommendations")

    recommendations = get_recommendations(
        income,
        expenses,
        total_expenses,
        remaining
    )

    st.write(
        "These suggestions are generated from your income and "
        "the expenses you entered."
    )

    for number, recommendation in enumerate(recommendations, start=1):

        st.markdown(
            f"**{number}.** {recommendation}"
        )

    st.divider()

    # Monthly history
    st.subheader("9. Monthly Spending History")

    st.write(
        "Save your current budget to compare it with other months."
    )

    selected_month = st.date_input(
        "Select the month for this budget",
        value=date.today().replace(day=1),
        key="history_month"
    )

    month_label = selected_month.strftime("%B %Y")

    if st.button("Save This Month's Budget", type="primary"):

        snapshot = {
            "Month": month_label,
            "Income": income,
            "Expenses": total_expenses,
            "Remaining": remaining
        }

        existing_month = None

        for index, item in enumerate(st.session_state.budget_history):

            if item["Month"] == month_label:
                existing_month = index
                break

        if existing_month is not None:

            st.session_state.budget_history[existing_month] = snapshot

            st.success(
                "Your saved budget for " + month_label + " was updated."
            )

        else:

            st.session_state.budget_history.append(snapshot)

            st.success(
                "Your budget for " + month_label + " was saved."
            )

    if st.session_state.budget_history:

        history_df = pd.DataFrame(
            st.session_state.budget_history
        )

        st.dataframe(
            history_df.style.format({
                "Income": "${:,.2f}",
                "Expenses": "${:,.2f}",
                "Remaining": "${:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        history_chart_data = history_df.melt(
            id_vars="Month",
            value_vars=["Income", "Expenses", "Remaining"],
            var_name="Budget Type",
            value_name="Amount"
        )

        history_chart = px.bar(
            history_chart_data,
            x="Month",
            y="Amount",
            color="Budget Type",
            barmode="group",
            title="Monthly Budget Comparison",
            color_discrete_map={
                "Income": "#55A878",
                "Expenses": "#1769AA",
                "Remaining": "#E6A23C"
            }
        )

        history_chart.update_layout(
            yaxis_title="Amount ($)",
            xaxis_title="Month",
            legend_title_text="",
            margin=dict(l=15, r=15, t=60, b=30)
        )

        st.plotly_chart(
            history_chart,
            use_container_width=True
        )

        history_csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Monthly History (CSV)",
            data=history_csv,
            file_name="budgetwise_monthly_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "Your monthly history will appear here after you save your first budget."
        )

    st.caption(
        "Monthly history is kept during your current session. "
        "Download the history CSV if you want to keep a copy."
    )

    st.divider()

    # Downloads
    st.subheader("10. Download Your Budget")

    st.write(
        "Download your current budget information to keep a personal copy."
    )

    budget_data = pd.DataFrame({
        "Category": categories,
        "Amount": [
            expenses[category] for category in categories
        ]
    })

    budget_data.loc[len(budget_data)] = [
        "Total Expenses",
        total_expenses
    ]

    budget_data.loc[len(budget_data)] = [
        "Monthly Income",
        income
    ]

    budget_data.loc[len(budget_data)] = [
        "Remaining Balance",
        remaining
    ]

    download_col1, download_col2 = st.columns(2)

    with download_col1:

        csv_data = budget_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Budget (CSV)",
            data=csv_data,
            file_name="budgetwise_budget.csv",
            mime="text/csv",
            use_container_width=True
        )

    with download_col2:

        report_html = create_budget_report(
            income,
            expenses,
            total_expenses,
            remaining,
            savings_goal,
            current_savings,
            recommendations,
            alerts
        )

        st.download_button(
            "Download Budget Report (HTML)",
            data=report_html,
            file_name="budgetwise_report.html",
            mime="text/html",
            use_container_width=True
        )

    st.caption(
        "The HTML report can be opened in a web browser and printed "
        "or saved as a PDF."
    )

    st.divider()

    st.caption(
        "BudgetWise | Budget planning and spending analysis"
    )
