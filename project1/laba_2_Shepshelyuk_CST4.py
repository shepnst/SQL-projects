import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

class EmployeeDatabase:
    def __init__(self, filename):  #function for initialization
        self.filename = filename
        if not os.path.exists(self.filename): # func from module os for checking whether the directory exists.
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'surname', 'name', 'position', 'salary'])  # names of columns

    def add_employee(self, id, surname, name, position, salary): #function for inserting new employee
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, surname, name, position, salary])

    def delete_employee(self, field, value):
        temp_file = 'temp.csv' #temporary data base
        with open(self.filename, 'r', newline='') as file, open(temp_file, 'w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            headers = next(reader)  # scanning headers
            writer.writerow(headers)  # write new headers to data base
            for row in reader:
                if str(row[0 if field == 'id' else 1]) != str(value):  # condition for deleting
                    writer.writerow(row)
        os.replace(temp_file, self.filename)  # old file is being replaced with temporary one

    def search_employee(self, field, value):
        with open(self.filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip headers
            for row in reader:
                if str(row[0 if field == 'id' else 1]) == str(value):  # condition for searching
                    return row
        return None  # if none is found

    def update_employee(self, id, surname, name, position, salary):
        temp_file = 'temp.csv' #temporary data base
        with open(self.filename, 'r', newline='') as file, open(temp_file, 'w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            headers = next(reader)
            writer.writerow(headers)  # write headers into new data base
            for row in reader:
                if row[0] == id:
                    writer.writerow([id, surname, name, position, salary])  # update 
                else:
                    writer.writerow(row)
        os.replace(temp_file, self.filename)  #old file is being replaced with temporary one

    
    def backup(self): #backup copy
        with open(self.filename, 'rb') as file:
            with open(self.filename + '.bak', 'wb') as backup_file:
                backup_file.write(file.read())  # copying 

    def restore(self, backup_filename): #restoring data from a backup
        os.replace(backup_filename, self.filename)  #restoring the file

    def clear_employee_table(self):  #for deleting data from table
        with open(self.filename, 'w') as f:
            f.write('')

    def export_to_csv(self, export_filename):
        with open(self.filename, 'rb') as orig_file:
            with open(export_filename, 'wb') as export_file:
                export_file.write(orig_file.read())  # copying the file to new file .csv


class Staff_GUI:  #class for creating graphics users interface
    def __init__(self, master):
        self.master = master
        self.db = EmployeeDatabase('employees.csv')
        
        #declaration of variables and their types
        self.id = tk.StringVar()
        self.surname = tk.StringVar()
        self.name = tk.StringVar()
        self.position = tk.StringVar()
        self.salary = tk.StringVar()

        #completing GUI with Tkinter(labels and entries for inserting the data)
        tk.Label(self.master, text="ID").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.id, width=30).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Surname").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.surname, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.master, text="Name").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.name, width=30).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Position").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.position, width=30).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Salary").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.salary, width=30).grid(row=4, column=1, padx=10, pady=5)

        #buttons for realization of some functions
        tk.Button(self.master, text="Add employee", command=self.add_employee, width=20).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Delete employee by ID", command=self.delete_employee, width=20).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Search employee", command=self.search_employee, width=20).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Update employee", command=self.update_employee, width=20).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Backup", command=self.backup, width=20).grid(row=9, column=0, pady=10)
        tk.Button(self.master, text="Restore", command=self.restore, width=20).grid(row=9, column=1, pady=10)
        tk.Button(self.master, text="Export to CSV", command=self.export, width=20).grid(row=10, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Clear Employee Table", command=self.clear_table, width=20).grid(row=11, column=0, columnspan=2, pady=10)
    #try except block
    def add_employee(self):
        try:
            existing_employee = self.db.search_employee('id',self.id.get())  # searching in ID field
            if existing_employee: #case when employee with this id is already exists
                messagebox.showerror("Error", "Employee with this ID already exists!")
                return

            self.db.add_employee(self.id.get(), self.surname.get(), self.name.get(), self.position.get(), self.salary.get())
            messagebox.showinfo("Success", "Employee added!") 
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_employee(self):
        emp_id = self.id.get()
        self.db.delete_employee('id', emp_id)
        messagebox.showinfo("Success", "Employee deleted!")

    def search_employee(self):
        field = 'id'  
        emp_id = self.id.get()
        result = self.db.search_employee(field, emp_id)
        if result:
            messagebox.showinfo("Search Result", f"Found: {result}")
        else:
            messagebox.showinfo("Search", "No employees found.")

    def update_employee(self):
        self.db.update_employee(self.id.get(), self.surname.get(), self.name.get(), self.position.get(), self.salary.get())
        messagebox.showinfo("Success", "Employee updated!")

    def clear_table(self):
        try:
            confirmation = messagebox.askyesno("Confirm", "Are you sure you want to clear the employee table?") # to ensure it is a right action
            if confirmation:
                self.db.clear_employee_table() 
                messagebox.showinfo("Success", "Employee table cleared!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def backup(self):
        self.db.backup()
        messagebox.showinfo("Backup", "Backup created!")

    def restore(self):
        backup_file = filedialog.askopenfilename(filetypes=[("Backup files", "*.bak")])
        if backup_file:
            self.db.restore(backup_file)
            messagebox.showinfo("Restore", "Database restored!")

    def export(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_name:
            self.db.export_to_csv(file_name)
            messagebox.showinfo("Export", "Database exported to CSV! Please find it and check!")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500") #size of window
    root.config(bg="lightblue") #colour
    app = Staff_GUI(root)
    root.title("Staff Database")
    root.mainloop()
