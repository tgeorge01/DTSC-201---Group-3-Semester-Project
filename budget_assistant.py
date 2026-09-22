print()
print("Hello, I'm your budgeting assistant--here to help you organize your monthly cashflow. For the following questions, please enter an integer which represents the dollar amount per month. (If the amount is $0 per month, enter 0.)")

print()
income = int(input("To get started, what is your net monthly income? "))

print()
essentials = []
print("First, let's discuss living expenses. What is the minimum you must spend monthly in the following categories?")

print()
essentials.append(int(input("phone bill: ")))
essentials.append(int(input("groceries: ")))
essentials.append(int(input("gasoline and vehicle maintenance: ")))
essentials.append(int(input("rent or house payment: ")))
essentials.append(int(input("insurances (e.g., health, home, car): ")))
essentials.append(int(input("debt repayment (e.g., student loans, mortgage): ")))
essentials.append(int(input("other necessary expenses not listed: ")))

print()
percent_essential = round((sum(essentials) / income) * 100)
margin = income - (sum(essentials))
print(f"You're living from {percent_essential}% of your income. After all necessary monthly expenses are covered, you have a margin of ${margin}.")


print()
nonessentials = []
print(f"Now let's plan how to use your remaining ${margin}. For the following categories, enter the dollar amount you intend to allocate. (You cannot exceed your total margin, but you should make a plan for every remaining dollar. Your ending balance should be $0.)")

print()
nonessentials.append(int(input("Discretionary expenditures (e.g., restaurants, merchandise, leisure): ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Charity: ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Emergency fund: ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Future savings (e.g., college, car, home, vacation): ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Retirement: ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Investments (e.g., stocks, bonds, index funds, real estate): ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
nonessentials.append(int(input("Other: ")))
print(f"You have ${margin - sum(nonessentials)} remaining.")

print()
ending_balance = margin - (sum(nonessentials))
if ending_balance == 0:
    print("Congrats! Your full income has been budgeted.")
else:
    print(f"Consider investing your remaining {ending_balance} in savings or your emergency fund.")


print("Here's a breakdown of your planned cashflow.")


## Create pandas dataframe and pie chart showing budget categories, amounts, and percentages
## Make it possible for user to return to previous questions