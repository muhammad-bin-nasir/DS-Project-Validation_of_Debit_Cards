import tkinter as tk
from tkinter import messagebox
from tkinter import font

def card_authentication(card_num):
    total = 0
    card_num = [int(x) for x in str(card_num)]
    for i in range(len(card_num) - 2, -1, -2):
        card_num[i] = card_num[i] * 2
        if card_num[i] > 9:
            card_num[i] -= 9
    total = sum(card_num)
    return total % 10 == 0

def isbn_authentication(isbn):
    isbn = isbn.replace("-", "").replace(" ", "") 
    if len(isbn) == 10:
        return validate_isbn10(isbn)
    elif len(isbn) == 13:
        return validate_isbn13(isbn)
    else:
        return False

def validate_isbn10(isbn):
    total = 0
    for i in range(10):
        total += int(isbn[i]) * (10 - i)
    return total % 11 == 0

def validate_isbn13(isbn):
    total = 0
    for i in range(12):
        factor = 1 if i % 2 == 0 else 3
        total += int(isbn[i]) * factor   
    checksum = int(isbn[-1])
    return 10 - (total % 10) == checksum or (total % 10 == checksum and checksum == 0)

def UPC_Number(upc):
    if len(upc) == 12:
        total_1 = 0
        total_2 = 0
        for i in range(11):
            if i % 2 == 0:
                total_1 += int(upc[i])
            else:
                total_2 += int(upc[i])
        total_1 = 3 * total_1
        total = total_1 + total_2   
        if total % 10 == 0:
            return int(upc[11]) == 0
        else:
            return 10 - (total % 10) == int(upc[11])

def validate_ean13(ean):
    ean = ean.replace("-", "").replace(" ", "") 
    if len(ean) == 13:
        ean12 = ean[:-1]
        provided_check_digit = int(ean[-1])
        calculated_check_digit = int(calculate_ean13_check_digit(ean12))
        return provided_check_digit == calculated_check_digit
    else:
        return False

def calculate_ean13_check_digit(ean12):
    if len(ean12) != 12 or not ean12.isdigit():
        raise ValueError("Invalid input for EAN-13 check digit calculation.")
    sum_odd = sum(int(ean12[i]) for i in range(0, 12, 2))
    sum_even = sum(int(ean12[i]) for i in range(1, 12, 2))
    total = sum_odd + sum_even * 3
    remainder = total % 10
    if remainder == 0:
        check_digit = 0
    else:
        check_digit = 10 - remainder
    return str(check_digit)

def validate_card(card_type):
    card_number = entry.get()
    card_number = card_number.replace(" ", "")
    
    if card_type in ["Visa", "Mastercard"] and len(card_number) != 16:
        messagebox.showerror("Validation Result", f"Invalid {card_type} number. It should be 16 digits long.")
        return
    elif card_type == "ISBN" and (len(card_number) != 10 and len(card_number) != 13):
        messagebox.showerror("Validation Result", "Invalid ISBN number. It should be either 10 or 13 digits long.")
        return
    elif card_type == "UPC" and len(card_number) != 12:
        messagebox.showerror("Validation Result", "Invalid UPC code. It should be 12 digits long.")
        return
    elif card_type == "EAN-13" and not validate_ean13(card_number):
        messagebox.showerror("Validation Result", "Invalid EAN-13 number.")
        return

    if card_type == "Visa" and card_authentication(card_number):
        messagebox.showinfo("Validation Result", "Valid Visa card number.")
    elif card_type == "Mastercard" and card_authentication(card_number):
        messagebox.showinfo("Validation Result", "Valid Mastercard number.")
    elif card_type == "ISBN" and isbn_authentication(card_number):
        messagebox.showinfo("Validation Result", "Valid ISBN number.")
    elif card_type == "UPC" and UPC_Number(card_number):
        messagebox.showinfo("Validation Result", "Valid UPC code.")
    elif card_type == "EAN-13" and validate_ean13(card_number):
        messagebox.showinfo("Validation Result", "Valid EAN-13 number.")
    else:
        messagebox.showerror("Validation Result", f"Invalid {card_type} number.")

def validate_input():
    user_input = check.get()
    if user_input == "1":
        switch_to_card_validator_frame("Visa")
    elif user_input == "2":
        switch_to_card_validator_frame("Mastercard")
    elif user_input == "3":
        switch_to_card_validator_frame("ISBN")
    elif user_input == "4":
        switch_to_card_validator_frame("UPC")
    elif user_input == "5":
        switch_to_card_validator_frame("EAN-13")
    else:
        messagebox.showerror("Invalid Option", "Please select a valid option (1, 2, 3, 4, or 5).")

def switch_to_card_validator_frame(card_type):
    frame_options.pack_forget()
    frame_card_validator.pack()
    label_card_validator.config(text=f"Enter {card_type} Number:", pady=10, padx=100)

    entry.delete(0, tk.END)
    entry.insert(0, card_number_entry.get())
    entry.bind("<Return>", lambda event: validate_card(card_type))

def back_to_options_frame():
    frame_card_validator.pack_forget()
    frame_options.pack()

window = tk.Tk()
window.title("Options")

frame_options = tk.Frame(window)
frame_card_validator = tk.Frame(window)

label_options = ["1. Authenticate VISA card",
                "2. Authenticate Mastercard",
                "3. Authenticate ISBN",
                "4. Authenticate UPC"]

label = tk.Label(frame_options, text="What do you want to do?", font=("Arial", 14))
label.pack(pady=10, padx=100)

for option in label_options:
    label_option = tk.Label(frame_options, text=option, font=("Arial", 14))  
    label_option.pack(pady=0)

check = tk.Entry(frame_options, font=("Arial", 14))  
check.pack(pady=0)
check.bind("<Return>", lambda event: validate_input())

validate_button1 = tk.Button(frame_options, text="Validate", command=validate_input, font=("Arial", 14))  
validate_button1.pack(pady=10)

label_card_validator = tk.Label(frame_card_validator, text="Enter Number:", font=("Arial", 14))  
label_card_validator.pack(pady=0)

entry = tk.Entry(frame_card_validator, font=("Arial", 14))  
entry.pack(pady=0)

card_number_entry = tk.Entry(frame_card_validator, font=("Arial", 14))  
card_number_entry.pack_forget()

validate_button_card_validator = tk.Button(frame_card_validator, text="Validate", command=lambda: validate_card("Visa" if check.get() == "1" else "Mastercard" if check.get() == "2" else "ISBN" if check.get() == "3" else "UPC" if check.get() == "4" else "EAN-13" if check.get() == "5" else "Unknown"), font=("Arial", 14))  # Set the font size to 14
validate_button_card_validator.pack(pady=10)
entry.bind("<Return>", lambda event: validate_card("Visa" if check.get() == "1" else "Mastercard" if check.get() == "2" else "ISBN" if check.get() == "3" else "UPC" if check.get() == "4" else "EAN-13" if check.get() == "5" else "Unknown"))

back_button = tk.Button(frame_card_validator, text="Back", command=back_to_options_frame, font=("Arial", 14)) 
back_button.pack(pady=10)

frame_options.pack()

window.mainloop()
