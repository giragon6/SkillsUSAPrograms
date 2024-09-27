import tkinter as tk 
from tkinter import ttk

def main():
    window = tk.Tk()

    window_width = 600
    window_height = 400

    # Gets coordinates to center window on screen
    screen_center_x = int((window.winfo_screenwidth()/2)-(window_width/2))
    screen_center_y = int((window.winfo_screenheight()/2)-(window_height/2))

    window.geometry(f'{window_width}x{window_height}+{screen_center_x}+{screen_center_y}')
    window.columnconfigure(0, weight=3)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)

    window.title('102 - Food Truck')

    class Item():
        '''Items for sale in the food truck, storing name and price'''
        def __init__(self, name:str, price:float):
            self.name = name
            self.price = price
            self.qty = 0
            self.qty_label = ttk.Label(window, text=self.qty)
            self.increase_qty_btn = ttk.Button(window, text='+', command=self.handle_inc_button)
            self.decrease_qty_btn = ttk.Button(window, text='-', command=self.handle_dec_button)
            self.label = ttk.Label(window, text=f'{self.name} (${self.price:.2f})')
        def handle_inc_button(self):
            self.qty +=1
            self.qty_label.config(text=self.qty)
        def handle_dec_button(self):
            if self.qty != 0:
                self.qty -= 1
            self.qty_label.config(text=self.qty)
    
    items = [
        Item('Hot Dog', 2.50),
        Item('Pizza Slice', 3.50),
        Item('Hamburger', 5.00),
        Item('Fries', 2.00),
        Item('Soda', 2.00),
        Item('Water', 1.00),
        Item('Potato Chips', 3.75)
    ]

    total_label = ttk.Label(window, text='')

    def handle_order():
        total_price = 0
        for item in items:
            total_price += (item.price*item.qty)
        total_label.config(text=f'Total: ${total_price:.2f}')
        total_label.grid(column=0)

    def handle_clear():
        for item in items:
            item.qty=0
            item.qty_label.config(text=item.qty)
            total_label.grid_forget()

    order_button = ttk.Button(text='Order', command=handle_order)
    order_button.grid(column=0, row=10)

    clear_button = ttk.Button(text='Clear', command=handle_clear)
    clear_button.grid(column=1, row=10)

    exit_button = ttk.Button(text='Exit', command=window.quit)
    exit_button.grid(column=2, row=10)

    for i, item in enumerate(items):
        item.label.grid(column=0, row=i)
        item.decrease_qty_btn.grid(column=1, row=i)
        item.qty_label.grid(column=2, row=i)
        item.increase_qty_btn.grid(column=3, row=i)

    window.mainloop()

if __name__ == "__main__":
    main()