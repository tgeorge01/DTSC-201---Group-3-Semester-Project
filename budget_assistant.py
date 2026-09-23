print()
print("Hello, I'm your budgeting assistant--here to help you organize your monthly cashflow.")

print()
print("For the following questions, please enter an integer which represents the dollar amount per month. (If the amount is $0 per month, enter 0.)")

print()
income = int(input("To get started, what is your net monthly income? "))

print()
essentials = []
print("Let's discuss living expenses--essential, here-and-now needs. What is the minimum you must spend monthly in the following categories?")

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
print("Now consider how much you currently spend monthly on non-essentials, like restaurants, merchandise, and leisure activties. These are discretionary expenses.")
print("(It's okay to have some "fun money." However, keep in mind that the more you spend on non-essentials, the less you will be able to invest in things you may need in the future.)")
int(input("Based on your available margin, how much are you willing to spend monthly on discretionary expenses going forward?" )

print()
long_term = []
print(f"Now let's plan how to use your remaining ${margin}.")

print()
print("For the following categories, enter the dollar amount you intend to allocate.")
print("(Note: You cannot exceed your total margin, but you should make a plan for every remaining dollar. Your ending balance should be $0.)")

print()
print("If you don't have an emergeny fund which can cover living expenses for 3-6 months, that's a good place to begin investing your margin.")
long_term.append(int(input("emergency fund: ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
print("If you have debt, you can put extra money toward your monthly repayment to make the debt disappear faster.")
long_term.append(int(input("extra debt repayment: ")))

print()
long_term.append(int(input("retirement: ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
long_term.append(int(input("savings (e.g., college, car, home, vacation): ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
long_term.append(int(input("investments (e.g., stocks, bonds, index funds, real estate): ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
long_term.append(int(input("charity: ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
long_term.append(int(input("other: ")))
print(f"You have ${margin - sum(long_term)} remaining.")

print()
ending_balance = margin - (sum(long_term))
if ending_balance == 0:
    print("Congrats! Your full income has been budgeted.")
else:
    print(f"Consider investing your remaining {ending_balance} in savings or your emergency fund.")


print("Here's a breakdown of your planned cashflow.")


## Create pandas dataframe and pie chart showing budget categories, amounts, and percentages
## Make it possible for user to return to previous questions
