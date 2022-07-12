# Student Debt Repayment Calculator

This project was created to calculate how  best to repay student debt, and to calculate if the student debt will be payed off before it expires.

The input should be in the format of "object = Debt(debt ammount, annual interest (as a fraction), annual salary, plan = plan number, duration = duration)

Salary should either be inputted as an integer / float, or as a dictionary if the salary is expected to change over the duration of the repayments.

If the salary is expected to change, it should be inputted in the form of {year: salary, year: salary....}
where year is how many years away the salary change is. For the current salary, year should be 0. Year should be inputted as an integer.

An example input with a static salary is:
x = Debt(900000, 0.075, 25000, plan = 2, duration = 30)

An example input with a changing salary is:
x = Debt(900000, 0.075, {0:25000, 10:50000}, plan = 2, duration = 30)

The __str__ returns the inputted information. 
The default_payments method calculates the amount payed over the debt duration, and returns information on how much was payed and the year payments cease.
