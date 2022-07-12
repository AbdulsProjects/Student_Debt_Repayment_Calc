#Variable storing the annual inflation rate
annual_inflation_fraction = 0.055
#Interest rates for plan 2 may vary based on income
monthly_inflation_fraction = annual_inflation_fraction / 12

class Debt:
    
    def __init__(self, amount, annual_interest_fraction, annual_salary_pre_tax, plan = 1, duration  = 30):
        self.amount = amount
        self.annual_interest_fraction = annual_interest_fraction
        self.monthly_interest_fraction = annual_interest_fraction / 12
        self.duration = duration
        self.plan = plan
        self.annual_salary_pre_tax = annual_salary_pre_tax
        
        
        #Assigns the payment threshhold based on plan
        if plan == 1:
            threshold = 1682

        elif plan == 2:
            threshold = 2274

        elif plan == 4:
            threshold = 2114

        else:
            raise ValueError("Invalid plan option inputted.")
            

        #Creates a dictionary containing all the monthly payment categories if a dictionary was used for salary
        if isinstance(annual_salary_pre_tax, dict):
            #Converting annual salary into monthly
            monthly_salary_pre_tax = annual_salary_pre_tax.copy()
            for key in monthly_salary_pre_tax:
                monthly_salary_pre_tax[key] = round((monthly_salary_pre_tax[key]/12), 2)
            self.monthly_repayments = monthly_salary_pre_tax.copy()
            
            #Iterates through the income dictionary inputted
            for key in self.monthly_repayments:
                #Calculates and stores the monthly payments that will be made based on income
                self.monthly_repayments[key] = (self.monthly_repayments[key] - threshold) * 0.09
                
                #Ensures monthly repayments are never negative
                if self.monthly_repayments[key] < 0:
                    self.monthly_repayments[key] = 0


        #Calculates monthly repayments based on plan and salary, used for a static salary
        else:   
            #Converting annual salary into monthly
            monthly_salary_pre_tax = annual_salary_pre_tax / 12
            self.monthly_repayments = (monthly_salary_pre_tax - threshold) * 0.09
                
    #Calculates the overall cost of the debt if using standard payments (maybe add option to change payments?)
    def default_payments(self):
        #Setting up variables
        amount_copy = self.amount
        pound_value = 1
        raw_payed = 0.0
        inflation_payed = 0.0
        current_repayment = self.monthly_repayments
        
        #Creates a monthly loop of payments and interest
        for i in range(self.duration * 12):
            
            #Checks if the current year has a salary change, and assigns the salary change if it does.
            if isinstance(self.monthly_repayments, dict):
                if (i/12) in self.monthly_repayments:
                    current_repayment = self.monthly_repayments[(i/12)]
                
            
            
            #Calculates the value of £1 with inflation
            pound_value = pound_value * (1 - monthly_inflation_fraction)
            
            #Applies interest
            amount_copy = amount_copy * (1 + self.monthly_interest_fraction)
            #Calculates payment
            #Debt isn't payed off this month
            if current_repayment <= amount_copy:
                payment = current_repayment
            #Debt is payed off this month
            else:
                payment = amount_copy
            
            #Deducts payment
            amount_copy = amount_copy - payment
            #Adds amount payed to tally
            raw_payed += payment
            inflation_payed += payment * pound_value
            
            #Debt is fully paid. Formatting and returning desired information
            if amount_copy == 0:
                years_to_pay = int(i/12)
                months_to_pay = i % 12
                raw_payed_output = "{:.2f}".format(raw_payed)
                inflation_payed_output = "{:.2f}".format(inflation_payed)
                
                return (f"The student debt of £{self.amount} is payed off after {years_to_pay} years and {months_to_pay} months.\
                \nThe total amount payed is £{raw_payed_output}, which is equivilent to £{inflation_payed_output} when applying an annual inflation rate of {annual_inflation_fraction*100}%.")

            
            
            #Checking for errors
            if amount_copy < 0:
                return "Error: 01"
        
        #Debt is wiped after the designated duration. Formatting and returning desired information
        raw_payed_output = "{:.2f}".format(raw_payed)
        inflation_payed_output = "{:.2f}".format(inflation_payed)
        outstanding_amount = "{:.2f}".format(amount_copy)
        return (f"The student debt of £{self.amount} is wiped after {self.duration} years, with an outstanding amount of £{outstanding_amount}.\
                \nThe total amount payed is £{raw_payed_output}, which is equivilent to £{inflation_payed_output} when applying an annual inflation rate of {annual_inflation_fraction*100}%.")


    #Making an informative __str__ for the object
    def __str__(self):

        output = f"\nDebt amount: {self.amount}\nAnnual interest: {self.annual_interest_fraction*100}%\
            \nPlan: {self.plan}\nDuration: {self.duration} years"
        
        if isinstance(self.annual_salary_pre_tax, dict):
            output += "\n\nAnnual salaries:\n"
        
            for key in self.annual_salary_pre_tax:
                output += f"Year: {key}".ljust(11)
                output += f"Salary: {self.annual_salary_pre_tax[key]}\n"
        else:
            output += f"\nAnnual salary: £{self.annual_salary_pre_tax}"
        return(output)
        
