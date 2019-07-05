# import lib
import sys
from threading import Thread
from statistics import mean
import time
try:
    import DataHandle
except Exception as e:
    print("Failed to import class: DataManipulate",e)
    sys.exit()
try:
    from tkinter import *
    import tkinter
    from tkinter import Frame, Label, Button, Tk, ttk
    from tkinter import messagebox as msg
except ImportError:
    print("Failed to import class: Tkinter")
    sys.exit()
try:
    # Implement the default Matplotlib key bindings.
    from matplotlib.figure import Figure
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation
    from matplotlib import style
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    msg.showerror("Error", "Failed to import class: matplotlib")
    sys.exit()
try:
    import numpy as np
except ImportError:
    msg.showerror("Error", "Failed to import class: numpy")
    sys.exit()
#****************************************************************************************************

# Main class

class MainWindow():
    iter = 0
    CURRENT_SPEED = 0
    MIN_SPEED = 1
    MAX_SPEED = 2
    AVG_SPEED = 3
    RANK = 4
    DISTANCE = 5
    ESTIMATED = 6
    SPENT_FUEL = 7

    TRIP_DISTANCE = 0
    TRIP_START_TIME = 0
    TRIP_FUEL_SPENT = 0
    'This class draw the root window for data manipulate'
    root = 0

    # Label to show data
    labels_frame = 0
    lbl_current_speed = 0
    lbl_min = 0
    lbl_max = 0
    lbl_avg = 0
    lbl_rank = 0
    lbl_estimated = 0
    lbl_distance = 0
    lbl_spent_fuel = 0

    lbl_current_speed_v = 0
    lbl_min_v = 0
    lbl_max_v = 0
    lbl_avg_v = 0
    lbl_rank_v = 0
    lbl_distance_v = 0
    lbl_estimated_v = 0
    lbl_spent_fuel_v = 0

    #ploting
    draw_frame = 0
    fig = 0
    plotcanvas = 0

    data = DataHandle.DataManipulate()
    class_dm_state = True
    ax1 = 0
    ax2 = 0
    ax3 = 0
    ax4 = 0
    ax5 = 0
    line1 = 0
    line2 = 0
    line3 = 0
    line4 = 0
    line5 = 0
    # figure variables
    FIGURE = 0
    FIGURE_AR_LIVE = 1
    FIGURE_A_LIVE = 2
    FIGURE_RANK_LIVE = 3
    FIGURE_HEALTH_LIVE = 4
    FIGURE_OSTACLES_LIVE = 5
    FIGURE_fUEL_SPEED = 6
    rank = [0]

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Data visual")
        self.root.overrideredirect(True)
        self.root.highlightthickness = 0
        self.root.attributes("-topmost", True)
        f = open('state.txt' , 'w')
        f.write('0')
        f.close()
        self.ui_def()
        self.main_ui()
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, blit=False)
        #self.plot_actual_speed_vs_recommend_speed_live_button()
        self.root.mainloop()
    def __del__(self):
        print("Class MainWindow destroyed")
# ************************ car_design Start ************************
    # main function call other
    def ui_def(self):
        self.root.resizable(0, 0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        # Label to show data
        self.labels_frame = Frame(self.root, width=550, height=130)
        self.labels_frame.grid(row=1, column=1, sticky=N+S)
        self.labels_frame.grid_columnconfigure(0, weight=1)
        self.lbl_current_speed=Label(self.labels_frame, text="Current Speed")
        self.lbl_min=Label(self.labels_frame, text="Min Speed")
        self.lbl_max=Label(self.labels_frame, text="Max Speed")
        self.lbl_avg=Label(self.labels_frame, text="Avg Speed")
        self.lbl_rank=Label(self.labels_frame, text="Speed Ranking")
        self.lbl_estimated=Label(self.labels_frame, text="Estimate Time")
        self.lbl_distance=Label(self.labels_frame, text="Trip Distace")
        self.lbl_spent_fuel=Label(self.labels_frame, text="Spent Fuel")
        self.lbl_current_speed_v=Label(self.labels_frame, text="")
        self.lbl_min_v=Label(self.labels_frame, text="")
        self.lbl_max_v=Label(self.labels_frame, text="")
        self.lbl_avg_v=Label(self.labels_frame, text="")
        self.lbl_rank_v=Label(self.labels_frame, text="")
        self.lbl_distance_v=Label(self.labels_frame, text="")
        self.lbl_estimated_v=Label(self.labels_frame, text="")
        self.lbl_spent_fuel_v=Label(self.labels_frame, text="")

        #ploting
        self.draw_frame = Frame(self.root, width=550, height=350)
        self.draw_frame.grid(row=0,column=1, sticky=N+S+E+W)
        self.draw_frame.grid_rowconfigure(0, weight=1)
        self.draw_frame.grid_columnconfigure(0, weight=1)
        style.use('bmh')
        self.fig = Figure(figsize=(5.5, 3.5), dpi=100, linewidth=.5)
        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.root)
        self.plotcanvas.get_tk_widget().place(x=250,y=0,width=550,height=350)

    def main_ui(self):
        self.config_root_ui()
        self.config_buttons_frame_ui()
        self.config_labels_frame()

    def config_root_ui(self):
        # full screen
        w = 800
        h = 480
        width_value = self.root.winfo_screenwidth()
        height_value = self.root.winfo_screenheight()
        x = (width_value/2) - (w/2)
        y = (height_value/2) - (h/2)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        # root title
        self.root.title("Data Figures")

    def config_buttons_frame_ui(self):
        # create frame instance
        button_frame = Frame(self.root, width=300, height=480)
        # create buttons
        btn_speed = Button(button_frame, text="Actual Speed", command=self.plot_actual_speed_live_button)
        btn_rec_vs_act_speed = Button(button_frame, text="Menitor Speed", command=self.plot_actual_speed_vs_recommend_speed_live_button)
        btn_ranke = Button(button_frame, text="Driver Rank", command=self.plot_rank_live_button)
        btn_health_reads = Button(button_frame, text="Health", command=self.plot_health_read_live_button)
        btn_obstacles = Button(button_frame, text="Obstacles", command=self.plot_obstacles_live_button)
        btn_trip_info = Button(button_frame, text="Trip Info", command=self.show_trip_info)
        btn_fuel_km = Button(button_frame, text="Fuel Econemy", command=self.plot_fuel_speed_live_button)


        #configure buttons grid layout
        btn_back = Button(button_frame, bd=1, text="<<<", command=self.terminate)
        btn_back.grid(row=0, column=0, rowspan=7, padx=10)
        btn_speed.grid(row=0,column=1, padx=15, pady=10)
        btn_rec_vs_act_speed.grid(row=1,column=1, pady=10)
        btn_ranke.grid(row=2, column=1, pady=10)
        btn_obstacles.grid(row=3, column=1, pady=10)
        btn_health_reads.grid(row=4, column=1, pady=10)
        btn_fuel_km.grid(row=5, column=1, pady=10)
        btn_trip_info.grid(row=6, column=1, pady=10)
        button_frame.grid(row=0, column=0, rowspan=2, sticky=W+E)# ,i sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

    def terminate(self):
        self.data.working = False
        self.root.destroy()

    def show_trip_info(self):
        #self.data.get_trip_weather()
        #self.data.get_trip_start_location()
        #TripInfo(self.data.all_readings, self.data.weather_data)
        Intution()

    def config_labels_frame(self):
        # grid table
        self.lbl_current_speed.grid(row=0, column=0, pady=5)
        self.lbl_min.grid(row=1, column=0, pady=5)
        self.lbl_max.grid(row=2, column=0, pady=5)
        self.lbl_avg.grid(row=3, column=0, pady=5)
        self.lbl_rank.grid(row=0, column=2, padx= 20)
        self.lbl_estimated.grid(row=1, column=2, padx= 20)
        self.lbl_distance.grid(row=2, column=2, padx= 20)
        self.lbl_spent_fuel.grid(row=3, column=2, padx = 20)

        self.lbl_current_speed_v.grid(row=0, column=1, padx=20)
        self.lbl_min_v.grid(row=1, column=1, padx=20)
        self.lbl_max_v.grid(row=2, column=1, padx=20)
        self.lbl_avg_v.grid(row=3, column=1, padx=20)
        self.lbl_rank_v.grid(row=0, column=3)
        self.lbl_distance_v.grid(row=2, column=3)
        self.lbl_estimated_v.grid(row=1, column=3)
        self.lbl_spent_fuel_v.grid(row=3, column=3)

# ************************ car_design End ************************

# ****************** Set labels text start *******************
    def set_label_value(self, label, value):
        try:
            label['text'] = str(value)
        except ValueError:
            print("ValueError")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
#****************** Set labels text end *******************

#******************** Plot data Start *********************

    def animate(self, i):
        try:
            if self.class_dm_state:
                self.data.working = True
                self.data.test.start()
                self.class_dm_state = False
            if self.FIGURE == self.FIGURE_AR_LIVE:
                self.plot_actual_speed_vs_recommend_speed_live(i)
            elif self.FIGURE == self.FIGURE_A_LIVE:
                self.plot_actual_speed_live(i)
            elif self.FIGURE == self.FIGURE_RANK_LIVE:
                self.plot_rank_live(i)
            elif self.FIGURE == self.FIGURE_HEALTH_LIVE:
                self.plot_health_read_live(i)
            elif self.FIGURE == self.FIGURE_OSTACLES_LIVE:
                self.plot_obstacles_live(i)
            elif self.FIGURE == self.FIGURE_fUEL_SPEED:
                self.plot_fuel_speed_live(i)
        except ValueError:
            print("ValueError")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

# ************** actual speed vs recommand speed

    def plot_actual_speed_vs_recommend_speed_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r', marker='.')
        self.line2, = self.ax1.plot([], [], 'b', marker='*')
        self.line1.set_linewidth(1)
        self.line2.set_linewidth(1)
        self.FIGURE = self.FIGURE_AR_LIVE

    def plot_actual_speed_vs_recommend_speed_live(self, i):
        self.ax1.legend(["Actual", "Recommend"])
        self.fig.suptitle("Actual Speed VS Recommend Speed")
        y, y1 = self.data.get_car_speed_readings()
        y, y1 = np.asarray(y), np.asarray(y1)
        x = self.data.get_list_number(len(y)-1)
        self.line1.set_data(x, y)
        self.line2.set_data(x, y1)
        self.ax1.set_xlim(0, 30)
        self.ax1.set_xticklabels([])
        self.ax1.set_ylim(min(min(y), min(y1))-15, max(max(y), max(y1))+15)
        self.car_des(y, y1)

# ************** actual speed

    def plot_actual_speed_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r', marker='.')
        self.line1.set_linewidth(1)
        self.ax1.set_xlim(0, 30)
        self.ax1.set_xticklabels([])
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Speed")
        self.FIGURE = self.FIGURE_A_LIVE

    def plot_actual_speed_live(self, i):
        try:
            self.fig.suptitle("Runtime Car Speed")
            self.ax1.legend(["Actual Speed"])
            y, y1 = self.data.get_car_speed_readings()
            #if len(y) == 21:
            #    return
            x = self.data.get_list_number(len(y)-1)
            y = np.asarray(y)
            try:
                self.line1.set_data(x, y)
            except ValueError:
                print("ValueError")
            except:
                print("un Error")
            self.ax1.set_ylim(min(y)-15, max(y)+15)
            self.car_des(y, y1)
        except ValueError:
            print("Error")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

# ************** ranking speed

    def plot_rank_live(self, i):
        self.fig.suptitle("Runtime Ranking")
        self.ax1.legend(["Speed Ranking"])
        y, y1 = self.data.get_car_speed_readings()
        y, y1 = np.asarray(y), np.asarray(y1)
        self.rank.append(self.data.driver_rank(y1, y))
        x = self.data.get_list_number(len(self.rank)-1)
        self.line1.set_data(x, self.rank)
        self.ax1.set_xlim(0, 45)
        self.ax1.set_ylim(0, 11)
        self.car_des(y, y1)

    def plot_rank_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r')
        self.line1.set_linewidth(1)
        self.FIGURE = self.FIGURE_RANK_LIVE


# ************** health sensors

    def plot_health_read_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(3, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r')
        self.line1.set_linewidth(1)
        self.ax2 = self.fig.add_subplot(3, 1, 2)
        self.line2, = self.ax2.plot([], [], 'b')
        self.line2.set_linewidth(1)
        self.ax3 = self.fig.add_subplot(3, 1, 3)
        self.line3, = self.ax3.plot([], [], 'g')
        self.line3.set_linewidth(1)
        self.line4, = self.ax3.plot([], [], 'y')
        self.line4.set_linewidth(1)
        self.FIGURE = self.FIGURE_HEALTH_LIVE
        self.health_default()


    def plot_health_read_live(self, i):
        self.fig.suptitle("Health Sensors Reading")
        self.ax1.legend(["Temperture"])
        self.ax2.legend(["Heart Beat"])
        self.ax3.legend(["Blood Pressure L", "Blood Pressure H"])
        try:
            temp, heart_bet, blood_pressure, blood_pressure_high = self.data.get_health_sensors_readings()
        except Exception as e:
            print("Error happed in get_health_sensors_readings while get sensors readings", e)
        try:
            x = self.data.get_list_number(len(temp)-1)
            temp, heart_bet, blood_pressure, blood_pressure_high = np.asarray(temp), np.asarray(heart_bet), np.asarray(blood_pressure), np.asarray(blood_pressure_high)

            self.line1.set_data(x, temp)
            self.line2.set_data(x, heart_bet)
            self.line3.set_data(x, blood_pressure)
            self.line4.set_data(x, blood_pressure_high)

            self.ax1.set_xlim(0, 50)
            self.ax2.set_xlim(0, 50)
            self.ax3.set_xlim(0, 50)

            self.ax1.set_xticklabels([])
            self.ax2.set_xticklabels([])
            self.ax3.set_xticklabels([])

            self.ax1.set_ylim(min(temp)-5, max(temp)+5)
            self.ax2.set_ylim(min(heart_bet)-5, max(heart_bet)+5)
            self.ax3.set_ylim(min(blood_pressure_high)-5, max(blood_pressure_high)+5)
        except Exception as e:
            print(e)
        self.set_health_reading_to_labels()

    def set_health_reading_to_labels(self):
        self.set_label_value(self.lbl_current_speed_v, self.data.get_car_speed())
        self.set_label_value(self.lbl_min_v, self.data.get_body_temp())
        self.set_label_value(self.lbl_max_v, self.data.get_body_heart_bet())
        self.set_label_value(self.lbl_avg_v, self.data.get_body_blood_pressure())
        self.set_label_value(self.lbl_rank_v, self.data.all_readings['car_parameters']['max_speed'])
        self.set_label_value(self.lbl_distance_v, "{} / {}".format(self.data.get_health_min_temp(), self.data.get_health_max_temp()))
        self.set_label_value(self.lbl_estimated_v, "{} / {}".format(self.data.get_health_min_heart_bet(), self.data.get_health_max_heart_bet()))
        self.set_label_value(self.lbl_spent_fuel_v, "{} / {}".format(self.data.get_health_min_blood_pressure(), self.data.get_health_max_blood_pressure()))

    def health_default(self):
        self.set_label_value(self.lbl_current_speed, "Current Speed")
        self.set_label_value(self.lbl_min, "Temperture")
        self.set_label_value(self.lbl_max, "Heart Bet")
        self.set_label_value(self.lbl_avg, "Blood Pressure")
        self.set_label_value(self.lbl_rank, "Max Speed")
        self.set_label_value(self.lbl_distance, "Min / Max")
        self.set_label_value(self.lbl_estimated, "Min / Max ")
        self.set_label_value(self.lbl_spent_fuel, "Min / Max")


# ************** health sensors


# ************** ultrasonic

    def plot_obstacles_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(3, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r', marker='o')
        self.line1.set_linewidth(1)
        self.ax2 = self.fig.add_subplot(3, 2, 3)
        self.line2, = self.ax2.plot([], [], 'b')  # , marker='o')
        self.line2.set_linewidth(1)
        self.ax3 = self.fig.add_subplot(3, 2, 4)
        self.line3, = self.ax3.plot([], [], 'g')  # , marker='o')
        self.line3.set_linewidth(1)
        self.ax4 = self.fig.add_subplot(3, 2, 5)
        self.line4, = self.ax4.plot([], [], 'y')  # , marker='o')
        self.line4.set_linewidth(1)
        self.ax5 = self.fig.add_subplot(3, 2, 6)
        self.line5, = self.ax5.plot([], [], 'b')  # , marker='o')
        self.line5.set_linewidth(1)
        self.FIGURE = self.FIGURE_OSTACLES_LIVE

    def plot_obstacles_live(self, i):
        # setting axes titles and legend
        self.fig.suptitle("NearBy Car & Obstacles")
        self.ax1.legend(["Obst."])
        self.ax2.legend(["L_Car"])
        self.ax3.legend(["R_Car"])
        self.ax4.legend(["F_Car"])
        self.ax5.legend(["B_Car"])

        u_right, u_left, u_front, u_back, u_bump = self.data.get_ultrasonic_readings()
        u_right, u_left, u_front, u_back, u_bump = np.asarray(u_right), np.asarray(u_left), np.asarray(u_front), np.asarray(u_back), np.asarray(u_bump)
        x = self.data.get_list_number(len(u_left) - 1)
        self.line1.set_data(x, u_bump)
        self.line2.set_data(x, u_left)
        self.line3.set_data(x, u_right)
        self.line4.set_data(x, u_front)
        self.line5.set_data(x, u_back)

        self.ax1.set_xlim(0, 50)
        self.ax2.set_xlim(0, 50)
        self.ax3.set_xlim(0, 50)
        self.ax4.set_xlim(0, 50)
        self.ax5.set_xlim(0, 50)

        self.ax1.set_xticklabels([])
        self.ax2.set_xticklabels([])
        self.ax3.set_xticklabels([])
        self.ax4.set_xticklabels([])
        self.ax5.set_xticklabels([])

        self.ax1.set_ylim(0, 6)
        self.ax2.set_ylim(0, 6)
        self.ax3.set_ylim(0, 6)
        self.ax4.set_ylim(0, 6)
        self.ax5.set_ylim(0, 6)
        self.set_obstecals_reading_to_labels()

    def set_obstecals_reading_to_labels(self):
        try:
            self.set_label_value(self.lbl_current_speed, "Current Speed")
            self.set_label_value(self.lbl_current_speed_v, self.data.get_car_speed())
            self.set_label_value(self.lbl_min, "Max Speed")
            self.set_label_value(self.lbl_min_v, self.data.all_readings['car_parameters']['max_speed'])
            self.set_label_value(self.lbl_max, "Bumb Height")
            self.set_label_value(self.lbl_max_v, self.data.get_ultrasonic_bump_read())
            self.set_label_value(self.lbl_avg, "Max Bump")
            self.set_label_value(self.lbl_avg_v, self.data.get_ultrasonic_bump_max_height())
            self.set_label_value(self.lbl_rank, "Left Car")
            self.set_label_value(self.lbl_rank_v, self.data.get_ultrasonic_left_read())
            self.set_label_value(self.lbl_distance, "Right Car")
            self.set_label_value(self.lbl_distance_v, self.data.get_ultrasonic_right_read())
            self.set_label_value(self.lbl_estimated, "Front Car")
            self.set_label_value(self.lbl_estimated_v, self.data.get_ultrasonic_front_read())
            self.set_label_value(self.lbl_spent_fuel, "Back Car")
            self.set_label_value(self.lbl_spent_fuel_v, self.data.get_ultrasonic_back_read())
        except ValueError:
            print('ValueError')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

# ************** ultrasonic

    def car_des(self, y, y1):
        try:
            r = self.data.driver_rank(y ,y1)
            print(r)
            self.set_label_value(self.lbl_current_speed, "Current Speed")
            self.set_label_value(self.lbl_current_speed_v, self.data.get_car_speed())
            self.set_label_value(self.lbl_min, "Fuel Econemy")
            self.set_label_value(self.lbl_min_v, self.data.get_car_fuel_eco())
            self.set_label_value(self.lbl_max, "Speed Ranking")
            self.set_label_value(self.lbl_max_v, self.data.driver_rank(y, y1))
            self.set_label_value(self.lbl_avg, "Location")
            if self.iter == 10:
                self.set_label_value(self.lbl_avg_v, self.data.get_loc_data())
                self.iter = 0
            self.set_label_value(self.lbl_rank, "Max / Avg")
            self.set_label_value(self.lbl_rank_v, "{} / {}".format(self.data.all_readings['car_parameters']['max_speed'], int(mean(y))))
            self.set_label_value(self.lbl_distance, "Trip Distance")
            self.set_label_value(self.lbl_distance_v, self.data.get_car_distance())
            self.set_label_value(self.lbl_estimated, "ESTIMATED")
            self.set_label_value(self.lbl_estimated_v, self.data.get_car_estimated_time())
            self.set_label_value(self.lbl_spent_fuel, "Spent Fuel")
            self.set_label_value(self.lbl_spent_fuel_v, self.data.get_car_spent_fuel())
            #self.set_label_value(self.lbl_spent_fuel_v, self.data.poly_regression_train('speed_fuel_dataset.csv', 1, [1, 80]))

            self.iter = self.iter + 1
        except ValueError:
            print("ValueError")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
# ********************* Fuel Speed
    def plot_fuel_speed_live_button(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot([], [], 'r', marker='o')
        self.line1.set_linewidth(1)
        self.ax1.set_xlim(0, 250)
        self.ax1.set_ylim(0, 30)
        self.FIGURE = self.FIGURE_fUEL_SPEED

    def plot_fuel_speed_live(self, i):
        try:
            self.fig.suptitle("speed - fuel")
            self.ax1.legend(["KM/Litter"])
            self.ax1.set_ylabel("KM")
            speed, fuel_eco = self.data.get_fuel_speed_readings()
            self.ax1.set_xlabel("Current Speed {}".format(speed[-1]))
            self.ax1.set_xlim(0,30)#min(speed)-5, max(speed)+5)
            self.ax1.set_ylim(0,20)#min(fuel_eco)+2, max(fuel_eco)+2)
            self.ax1.set_xticklabels([])

            x = self.data.get_list_number(len(speed)-1)
            speed, fuel_eco = np.asarray(speed), np.asarray(fuel_eco)
            try:
                self.line1.set_data(x, fuel_eco)
            except ValueError:
                print("ValueError")
            except:
                print("Unknown Error")
            # self.car_des(y, y1)
        except ValueError:
            print("Error")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise



# ******************** Plot data End *********************


class TripInfo():
    root = 0
    win = 0
    l11, l12, l13, l14, l15, l16, l17 = 0, 0, 0, 0, 0, 0, 0
    l21, l22, l23, l24, l25, l26, l27 = 0, 0, 0, 0, 0, 0, 0
    l31, l32, l33, l34, l35, l36, l37 = 0, 0, 0, 0, 0, 0, 0
    l41, l42, l43, l44, l45, l46, l47 = 0, 0, 0, 0, 0, 0, 0
    data = 0
    weather = 0
    def __init__(self, data, weather):
        self.data = data
        self.weather = weather
        self.root = tkinter.Tk()
        self.root.overrideredirect(True)
        self.root.highlightthickness = 2
        self.root.attributes("-topmost", True)
        self.main_ui()
        self.config_root_ui()
        self.config_labels()
        self.root.mainloop()
    def main_ui(self):
        #root.resizable(0, 0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)

    def config_root_ui(self):
        # full screen
        w = 500
        h = 300
        width_value = self.root.winfo_screenwidth()
        height_value = self.root.winfo_screenheight()
        x = (width_value/2) - (w/2)
        y = (height_value/2) - (h/2)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        # root title
        self.root.title("Trip Info")
    def config_labels(self):
        self.l11 = Label(self.root, text="Driver").grid(row=0, column=0, padx=20)
        self.l12 = Label(self.root, text='Start Time').grid(row=1, column=0, padx=20)
        self.l13 = Label(self.root, text='Start Date').grid(row=2, column=0, padx=20)
        self.l14 = Label(self.root, text='Start Location').grid(row=3, column=0, padx=20)
        self.l15 = Label(self.root, text='Day Temperture').grid(row=4, column=0, padx=20)
        self.l16 = Label(self.root, text='Day Min Temp').grid(row=5, column=0, padx=20)
        self.l17 = Label(self.root, text='Visibility').grid(row=6, column=0, padx=20)

        self.l21 = Label(self.root, text=self.data['trip_info']['driver_name']).grid(row=0, column=1)
        self.l22 = Label(self.root, text=self.data['trip_info']['start_time']).grid(row=1, column=1)
        self.l23 = Label(self.root, text=self.data['trip_info']['start_date']).grid(row=2, column=1)
        self.l24 = Label(self.root, text=self.data['trip_info']['start_loc_name']).grid(row=3, column=1)
        self.l25 = Label(self.root, text=self.weather['temp']).grid(row=4, column=1, padx=20)
        self.l26 = Label(self.root, text=self.weather['min_temp']).grid(row=5, column=1, padx=20)
        self.l27 = Label(self.root, text=self.weather['visibility']).grid(row=6, column=1, padx=20)

        self.l31 = Label(self.root, text='Litters / Distance').grid(row=0, column=2)
        self.l32 = Label(self.root, text='Max / Avg').grid(row=1, column=2)
        self.l33 = Label(self.root, text='Trip Rank').grid(row=2, column=2)
        self.l34 = Label(self.root, text='Current Location').grid(row=3, column=2)
        self.l35 = Label(self.root, text='Weather Descreption').grid(row=4, column=2)
        self.l36 = Label(self.root, text='Day Max Temp').grid(row=5, column=2)
        self.l37 = Label(self.root, text='Humidity').grid(row=6, column=2)

        self.l41 = Label(self.root, text="{} / {}".format(self.data['car_parameters']['spent_fuel'], self.data['car_parameters']['distance'])).grid(row=0, column=3, padx=20)
        self.l42 = Label(self.root, text="{} / {}".format(self.data['car_parameters']['max_speed'], self.data['car_parameters']['distance'])).grid(row=1, column=3, padx=20)
        self.l43 = Label(self.root).grid(row=2, column=3, padx=20)
        self.l44 = Label(self.root).grid(row=3, column=3, padx=20)
        self.l45 = Label(self.root, text=self.weather['descreption']).grid(row=4, column=3, padx=20)
        self.l46 = Label(self.root, text=self.weather['max_temp']).grid(row=5, column=3, padx=20)
        self.l47 = Label(self.root, text=self.weather['humidity']).grid(row=6, column=3, padx=20)
        self.button = Button(self.root, text='Exit', command=self.root.destroy).grid(row=7, column=0, columnspan=4)

class Intution:
    db = MySQLdb.connect(host="localhost", user="safaandsound", passwd="12345", db="SafeAndSound") # local
    root = 0
    win = 0
    btn_submit = 0
    btn_exit = 0
    l00, l01, l02, l03, l04, l05, l06, l07 = 0, 0, 0, 0, 0, 0, 0, 0
    l20, l21, l22, l23, l24, l25, l26 = 0, 0, 0, 0, 0, 0, 0
    c10, c11, c12, c13, c14, c15, c16, c17 = 0, 0, 0, 0, 0, 0, 0, 0
    c30, c31, c32, c33, c34, c35, c36 = 0, 0, 0, 0, 0, 0, 0
    multi_vechiles = ['single vechile', 'multi vechiles', 'vechiles(s)+pedestrian(s)', 'vechile(s)+cyclist(s) only', 'cyclists only', 'vechile(s)+mutiple other types', 'cyclist(s)+pedestrain(s) only', 'other without non-parked veh', 'other']
    intersection = ['unknown', 'intersection', 'at landmark']
    crash_state_highway = ['yes', 'no']
    flat_hill = ['flat', 'hill']
    road_chatacter = ['unknown', 'bridge', 'motorway ramp', 'railway crossing']
    road_curvature = ['straight', 'easy', 'modereate', 'severe']
    road_wet = ['unknown', 'wet', 'dry', 'ice/snow']
    number_of_lanes = [1, 2, 3, 4, 5, 6, 7, 8]
    traffic_control = ['nil', 'traffic signal', 'stop sign', 'give way sign', 'points man', 'school patrol', 'n/a']
    speed_limit = [40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    urban = ['urban', 'open road']
    light = ['unknown', 'bright sun', 'over cast', 'twilight', 'dark']
    street_light = ['unknown', 'on', 'off', 'none']
    weather = ['unknown', 'fine', 'mist', 'light rain', 'heavy rain', 'snow']
    crash_severity = ['non-fetal', 'medium', 'super', 'fatal']
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.overrideredirect(True)
        self.root.highlightthickness = 2
        self.root.attributes("-topmost", True)
        self.main_ui()
        self.config_root_ui()
        self.config_label_combo()
        self.root.mainloop()

    def main_ui(self):
        #root.resizable(0, 0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)

    def config_root_ui(self):
        # full screen
        w = 800
        h = 480
        width_value = self.root.winfo_screenwidth()
        height_value = self.root.winfo_screenheight()
        x = (width_value/2) - (w/2)
        y = (height_value/2) - (h/2)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        # root title
        self.root.title("Trip")

    def config_label_combo(self):
        self.l00 = Label(self.root, text="Multi Vechiles").grid(row=0, column=0)
        self.l01 = Label(self.root, text='Intersection').grid(row=1, column=0)
        self.l02 = Label(self.root, text='Crash State Highway').grid(row=2, column=0)
        self.l03 = Label(self.root, text='Flat Hill').grid(row=3, column=0)
        self.l04 = Label(self.root, text='Road Characte').grid(row=4, column=0)
        self.l05 = Label(self.root, text='Road Curvature').grid(row=5, column=0)
        self.l06 = Label(self.root, text='Road Wet').grid(row=6, column=0)
        self.l07 = Label(self.root, text='Number of Lanes').grid(row=7, column=0)

        self.c10 = ttk.Combobox(self.root, values=self.multi_vechiles, width=30)
        self.c10.grid(row=0, column=1)
        self.c11 = ttk.Combobox(self.root, values=self.intersection)
        self.c11.grid(row=1, column=1)
        self.c12 = ttk.Combobox(self.root, values=self.crash_state_highway)
        self.c12.grid(row=2, column=1)
        self.c13 = ttk.Combobox(self.root, values=self.flat_hill)
        self.c13.grid(row=3, column=1)
        self.c14 = ttk.Combobox(self.root, values=self.road_chatacter)
        self.c14.grid(row=4, column=1)
        self.c15 = ttk.Combobox(self.root, values=self.road_curvature)
        self.c15.grid(row=5, column=1)
        self.c16 = ttk.Combobox(self.root, values=self.road_wet)
        self.c16.grid(row=6, column=1)
        self.c17 = ttk.Combobox(self.root, values=self.number_of_lanes)
        self.c17.grid(row=7, column=1)

        self.l20 = Label(self.root, text='Traffic Control').grid(row=0, column=2)
        self.l21 = Label(self.root, text='Speed Limit').grid(row=1, column=2)
        self.l22 = Label(self.root, text='Urban').grid(row=2, column=2)
        self.l23 = Label(self.root, text='Light').grid(row=3, column=2)
        self.l24 = Label(self.root, text='Street Light').grid(row=4, column=2)
        self.l25 = Label(self.root, text='Weather').grid(row=5, column=2)
        self.l26 = Label(self.root, text='Crash Severity').grid(row=6, column=2)

        self.c30 = ttk.Combobox(self.root, values=self.traffic_control)
        self.c30.grid(row=0, column=3)
        self.c31 = ttk.Combobox(self.root, values=self.speed_limit)
        self.c31.grid(row=1, column=3)
        self.c32 = ttk.Combobox(self.root, values=self.urban)
        self.c32.grid(row=2, column=3)
        self.c33 = ttk.Combobox(self.root, values=self.light)
        self.c33.grid(row=3, column=3)
        self.c34 = ttk.Combobox(self.root, values=self.street_light)
        self.c34.grid(row=4, column=3)
        self.c35 = ttk.Combobox(self.root, values=self.weather)
        self.c35.grid(row=5, column=3)
        self.c36 = ttk.Combobox(self.root, values=self.crash_severity)
        self.c36.grid(row=6, column=3)

        self.btn_exit = Button(self.root, text='Exit', command=self.root.destroy).grid(row=7, column=3)
        self.btn_submit = Button(self.root, text='Submit', command="self.submit_button").grid(row=7, column=2)

    # this fuction will run when submit button click
    # wrie you code you want inside in
    def submit_button(self):
        print('x')
        """
        cur = self.db.cursor()
        sql = "INSERT INTO "
        try:
                print "Writing to the database..."
                cur.execute(*sql)
                db.commit()
                print "Write complete"

        except Exception as e:
                db.rollback()
                print ("We have a problem",e)

        cur.close()
        db.close()"""

#if DataHandle.DataManipulate.all_readings['state']=='1':
MainWindow()
