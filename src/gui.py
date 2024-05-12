import customtkinter as ctk
import pandas as pd
from tkinter import END
import tkinter as tk
from pandastable import Table


class DisplayTable(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text="DisplayTable")
        label.grid(row=0, column=1, padx=10, pady=10, columnspan=4)

        df = pd.read_csv("link_result.csv")

        self.table_FRAME = ctk.CTkFrame(self)
        self.table = Table(self.table_FRAME,
                           dataframe=df)
        self.table.grid(row=0, column=0, padx=10, pady=10, columnspan=4)
        self.table_FRAME.grid(row=1, column=1, padx=30, pady=10, columnspan=4,
                              rowspan=10)
        # self.table_FRAME.grid_propagate(False)
        # self.table_FRAME.configure(width=10, height=20)
        self.table.show()


if __name__ == '__main__':
    # Declare root window first to be able to get screen information
    root = tk.Tk()

    app = DisplayTable(parent=root)
    app.pack(fill="both", expand=True)

    root.mainloop()