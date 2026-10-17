import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime
import os

FILE= "expense.csv"

class smart_expense_tracker:
    def __init__(self):
        if os.path exist(FILE):
            self.df = pd.read_csv(FILE)
        else:
            self.df=pd.DataFrame(columns=["Date", "Amount","Category","Description"])
        self.clean_data()
        
    def clean_data(self):
        if not self.df.empty:
            self.df["Date"]=pd.to_datetime(self.df["Date"],errors="coerce")
            self.df.dropna(subset=["Date","Amount","Category"],inplace=True)
            self.df=self.df[self.df["Amount"]>0]
            self.df["Category"]=self.df["Category"].astype(str)
    
    def save_data(self):
        self.df.to_csv(FILE , index=False , date_format=%Y-%m-%d)
            
    def add_expense(self , date , amount , category , description ):
        try:
            date=pd.to_datetime(date,errors="raise")
            amount=float(amount)
            
            if amount <=0:
                print("Amount must be greater than zero.")
                return
            
            new_expense = pd.DataFrame([{
                "Date" : date,
                "Amount" : amount ,
                "Category" : category,
                "Description" : description 
            }])
                
            self.df = pd.concat([self.df,new_expense],ignore_index=True )
            self.save_data()
            print("Expense added successfully!")
            
        except(ValueError,TypeError):
            print("Enter a valid date and amount")
            
    def get_summury(self):
        if self.df.empty:
            print("No expense data available.")
            return
        amount=self.df["Amount"].to_numpy()
        print("\n--- Expense Summury ---")
        print("Total Expense:",round(np.sum(amount),2))
        print("Average Expense:",round(np.mean(amount),2))
        print("Maximun Expense:",round(np.max(amount),2))
        print("Minimum Expense:",round(np.min(amount),2))
        print("Numbers of Transection:",len(amount))
        
    def filter_expense(self , condition=True ):
        if self.df.empty:
            print("No Filter expense found.")
            return
        
        filtered = self.df.copy()
        print("\nFilrter by category")
        print("1. Filter by category")
        print("2. Filter by date range")
        print("3 Filter by amount")
        
        choice=int(input("Enter your choice: "))
        
        try:
            if choice == 1:
                category=input("Enter Caterory:")
                filtered = filtered[filtered["Category"].str.lower() == category.lower()]
                
            elif choice == 2:
                start=d.to_datetime(input("Start date (YYYY-MM-DD):"))
                end=d.to_datetime(input("End date (YYYY-MM-DD):"))
                filtered=filtered[
                   (filtered["Date"]>=start) &
                   (filtered["Date"]<=end)
                
            elif choice == 3:
                minimum=float(input("Enter minimum amount:"))
                filtered=filtered[filtered["amount"] >= minimum]
                
            else:
                print("Invalid Filter choice:")
                return
        except(ValueError,TypeError):
            print("Enter a valid category")
            
            
    def generate_report(self):
        if self.df.empty:
            print("No data available for expance")
            return
        report=self.df.groupby("Category").agg(
            Total_Expense=("Amount","sum"),
            Average_Expense=("Amount","mean"),
            Transactions=("Amount","count")
        ).sot_values("Total_Expenses",ascending=False)
        print("\n--- expense Report ---")
        print(report.round(2))
        
        top_category=report["Total_Expense"].idxmax()
        print("\nTop spending category:",top_category)
        
        monthly=self.df.groupby(self.df["Date"].dt.to_period("M"))["Amount"].sum()
        
        print("\nMonthly Spending")
        print(monthly)
        
        report.to_csv("expense_report.csv")
        print("\nReport saved before generating charts")
        return
    
    def show_charts(self):
        if self.df.empty:
            print("Add expenses before generating charts")
            return
        data=self.df.copy()
        data["Month"]=data["Data"].dt.to_period("M").astype(str)
        category_totals=data.groupby("category")["Amount"].sum()
        monthly_totals=data.groupby("Month")["Amount"].sum()
        
        sns.set_theme(style="whitegrid")
        
        #bar
        plt.figure(figsize=(8,5))
        sns.barplot(
            x=category_totals.index,
            y=category_totals.values
        )
        plt.title("Total expense by category")
        plt.xlabel=("Category")
        plt.ylabel=("Expense")
        plt.show()
        
        # 2. Line Graph
        plt.figure(figsize=(8, 5))
        plt.plot(
            monthly_totals.index,
            monthly_totals.values,
            marker="o"
        )
        plt.title("Monthly Spending Trends")
        plt.xlabel("Month")
        plt.ylabel("Total Expenses")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

        # 3. Pie Chart
        plt.figure(figsize=(7, 7))
        plt.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Expense Distribution by Category")
        plt.tight_layout()
        plt.show()

        # 4. Histogram
        plt.figure(figsize=(8, 5))
        sns.histplot(data["Amount"], bins=10, kde=True)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Expense Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n===== SMART EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Filter Expenses")
        print("4. Generate Report")
        print("5. Show Charts")
        print("6. View All Expenses")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            expense_date = input("Date (YYYY-MM-DD): ")
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Enter a valid amount.")
                continue

            category = input("Category: ").strip()
            description = input("Description: ").strip()

            if not category:
                print("Category cannot be empty.")
                continue

            tracker.add_expense(
                expense_date, amount, category, description
            )

        elif choice == "2":
            tracker.get_summary()

        elif choice == "3":
            tracker.filter_expense()

        elif choice == "4":
            tracker.generate_report()

        elif choice == "5":
            tracker.show_charts()

        elif choice == "6":
            if tracker.df.empty:
                print("No expenses available.")
            else:
                print(tracker.df.to_string(index=False))

        elif choice == "7":
            print("Thank you for using Smart Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
        
        
        
    
        
            
            
