#import lib
import sys
try:
    import tkinter
    from tkinter.font import Font
    from tkinter import Frame, Label, Button
    from tkinter import messagebox as msg
except ImportError:
    print("Failed to import class: Tkinter")
    sys.exit()
try:
    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    # Implement the default Matplotlib key bindings.
    from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
except ImportError:
    msg.showerror("Error", "Failed to import class: matplotlib")
    sys.exit()
try:
    import numpy as np
except ImportError:
    msg.showerror("Error", "Failed to import class: numpy")
    sys.exit()

#main class
class RootWindow():
    'This class draw the root window for data manipulate'
    root = tkinter.Tk()
    draw_frame = Frame(root)
    draw_frame.pack(side=tkinter.RIGHT)
    def __init__(self):
        self.plot_data([0],[0],[0],"title","fig1","fig2")
        self.main_ui()
        self.root.mainloop()

    def plot_data(self, x, y1, y2, title, legend_y1, legend_y2):
        for widget in self.draw_frame.winfo_children():
             widget.destroy()
        fig = Figure(figsize=(5, 3.8), dpi=100)
        fig.suptitle(title)
        fig.add_subplot(111).plot(x,y1)
        fig.legend(legend_y1)
        if len(y2) > 0:
            fig.add_subplot(111).plot(x,y2)
            fig.legend((legend_y1,legend_y2))

        canvas = FigureCanvasTkAgg(fig, master=self.draw_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()
        #toolbar = NavigationToolbar2Tk(canvas,self.root)
        #toolbar.update()
        #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def main_ui(self):
        #self.config_root_ui()
        self.config_buttons_frame_ui()


    def config_root_ui(self):
        #full screen
        width_value = self.root.winfo_screenwidth()
        height_value = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (width_value, height_value))
        
        #root title
        self.root.title("Data Figures")

    def config_buttons_frame_ui(self):
        #create frame instance
        button_frame = Frame(self.root, width=300, height=480)
        
        #create buttons
        btn_speed = Button(button_frame, text="Actual Speed", command="actual_speed")
        btn_rec_vs_act_speed = Button(button_frame, text="Menitor Speed", command="menitor_speed")
        btn_ranke = Button(button_frame, text="Drive rank", command="ranke")
        btn_fuel_km = Button(button_frame, text="Fuel/dist", command="remain_fuel")
        
        #configure buttons grid layout
        btn_back = Button(button_frame, bd=1, text="<<<", command="back")
        btn_back.grid(row=0, column=0, rowspan=4, padx=10)
        btn_speed.grid(row=0,column=1, padx=15, pady=10)
        btn_rec_vs_act_speed.grid(row=1,column=1, pady=10)
        btn_ranke.grid(row=2, column=1, pady=10)
        btn_fuel_km.grid(row=3, column=1, pady=10)
        button_frame.pack(side=tkinter.LEFT)

    def actual_speed():
        return 0
    def menitor_speed():
        return 0



