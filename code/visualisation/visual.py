#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.21

import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# add the path
import sys
sys.path.append('..')

# import the solver
from task2_2 import GA
from task2_1 import PSO
from task2_3 import Hopfield
from task2_2 import dataset

class TSP:
    '''
    The class of defining the frame of the window
    '''
    def __init__(self):
        # create the window for the project
        self.window = tk.Tk()
        self.window.title('TSP solver')
        self.window.resizable(False,False)    # limit to change the size of the window
        self.window.geometry('1000x600')

        # Init the menu bar for the user
        # We can use the lambda to transfer the prama into the command function
        self.menubar = tk.Menu(self.window)
        self.algorithm_menu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = 'Algorithm', menu = self.algorithm_menu)
        self.algorithm_menu.add_command(label = 'GA', command = self.set_GA)
        self.algorithm_menu.add_command(label = 'PSO', command = self.set_PSO)
        self.algorithm_menu.add_command(label = 'Hopfield', command = self.set_Hopfield)
        self.algorithm_menu.add_separator()
        self.algorithm_menu.add_command(label = 'Exit', command = self.quit)
        self.window.config(menu = self.menubar)
        
        # add the notemessage for the reader on the menubar
        self.note_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label = 'Note', menu = self.note_menu)
        self.note_menu.add_command(label = 'README', command = self.README)

        # Init the canvas and right frame for the window
        # 196, 0  |  600, 800
        self.frm_r  = tk.Frame(self.window)
        self.frm_r.place(x = 196, y = 0)
        self.canvas = tk.Canvas(self.frm_r, bg = 'white', height = 600, width = 800)
        self.canvas.pack(side = 'left')

        # Init the left frame
        self.frm_l = tk.Frame(self.window)
        self.frm_l.place(x = 0, y = 0)

        # Init the tk Var
        self.current_algorithm_msg = tk.StringVar()    # current algorithm, default GA
        self.current_algorithm_msg.set('GA')
        self.iterations_msg        = tk.IntVar()
        self.iterations_msg.set(0)    # if the value is -1, refuse to run and give the warning messagebox
        self.best_result_tk = tk.StringVar()
        
        for i in range(9):
            if i == 0 :
                # init the label
                self.current_algorithm     = tk.Label(self.frm_l, textvariable = \
                self.current_algorithm_msg, bg = 'yellow', font = ('Arial', 12), \
                width = 24, height = 3)
                self.current_algorithm.grid(row = i, column = 0)
            elif i == 1:
                # init the button `init the map`
                self.init_map_button = tk.Button(self.frm_l, text = 'Init the map', \
                                     width = 24, height = 3, command = self.init_map)
                self.init_map_button.grid(row = i, column = 0)
            elif i == 2:
                # init the scale iterations setting widget
                # if the 
                self.iteration_scale = tk.Scale(self.frm_l, label = 'Set the iterations',\
                        from_ = 0, to = 3000, orient = tk.HORIZONTAL, length = 190,\
                        showvalue = 1, tickinterval = 1000, resolution = 1, \
                        command = self.set_iterations)
                self.iteration_scale.grid(row = i, column =0)
            elif i == 3:
                # init the button `run`
                self.run_button = tk.Button(self.frm_l, text = 'Search', \
                                     width = 24, height = 3, command = self.run)
                self.run_button.grid(row = i, column = 0)
            elif i == 4:
                # init the button `export result`
                self.export_button = tk.Button(self.frm_l, text = 'Export result', \
                                     width = 24, height = 3, command = self.export)
                self.export_button.grid(row = i, column = 0)  
            elif i == 5:
                # init the best result label
                self.search_label = tk.Label(self.frm_l, height = 1, width = 24, \
                        text = 'Best result', bg = 'yellow', font = ('Arial', 12))
                self.search_label.grid(row = i, column = 0)
            elif i == 6:
                # init the best result `text`
                self.best_text = tk.Text(self.frm_l, height = 1, width = 24)
                self.best_text.grid(row = i, column = 0)
            elif i == 7:
                # add the label for the search text
                self.search_label = tk.Label(self.frm_l, height = 1, width = 24, \
                        text = 'Seach result', bg = 'yellow', font = ('Arial', 12))
                self.search_label.grid(row = i, column = 0)
            elif i == 8:
                # init the text widget for result
                self.search_text = tk.Text(self.frm_l, height = 24, width = 24)
                self.search_text.grid(row = i, column = 0)

        # the default solver is the GA solver, load three solvers as function 
        # TSP.solver default
        self.solver = GA.main
        self.fpath  = None
        
        # Solver's param
        self.cities_map   = None
        self.dimension    = None
        self.cities       = None
        self.best_result  = np.inf
        self.path         = None
        self.current_time = None
        self.canvas_x     = []
        self.canvas_y     = []
        
        # the switch for the script
        self.havebeenrunned = True
        
    def quit(self):
        print("quit the window")
        self.window.destroy()
        
    def start(self):
        # start the main loop of the window
        self.window.mainloop()
        
    def README(self):
        # provide oen toplevel for the user to show how to create their own dataset 
        # for this python script
        self.tw = tk.Toplevel(self.window)
        self.tw.geometry('600x300')
        self.tw.title("README")
        
        self.tt = tk.Text(self.tw, height = 22, width = 300)
        self.tt.insert(1.0, '''Data file format (TSPLIB):\n
        1. NAME: china34\n
        2. TYPE: TSP\n
        3. COMMENT: 34\n
        4. locations in China\n
        5. DIMENSION: 34\n
        6. EDGE_WEIGHT_TYPE: EUC_2D\n
        7. NODE_COORD_SECTION\n
        8. ~ End \n
        is the data (label of the city(begin from 1), x, y)\n''')

        self.tt.place(x = 10, y = 0)
        self.tb = tk.Button(self.tw, text = 'Exit', width = 15, height = 2, command = self.tw.destroy)
        self.tb.place(x = 10, y = 250)
    
    def export(self):
        # export the result into the file
        # maybe use the filedialog
        best = self.best_result_tk
        search = self.search_text.get(0.0, 'end')
        with filedialog.asksaveasfile() as f:
            f.write("Best result : " + best + '\n')
            f.write("Search result : \n")
            f.write(search)
        return True
        
    def init_map(self):
        # Init the map for the solver (GA, PSO, Hopfield)
        # this function try to open the filedialog for user ti choose the tsplib file
        try:
            self.fpath = filedialog.askopenfilename()    # get the name of the tsplib
        except:
            print("Do not choose one file")
            return False
        # use the file to create the map
        try:
            self.cities_map, self.dimension, self.cities = dataset.create_map(self.fpath)
        except:
            messagebox.showerror(title = 'Fatal Error', message = 'The file is not in the right format !')
            return False
        # set unrunned 
        self.canvas_x     = []
        self.canvas_y     = []
        self.canvas.delete("all")
        # init the canvas, show the point
        self.draw_point()
        self.set_runned(False)
        
        # init the text
        self.search_text.delete(1.0,tk.END)
        self.best_text.delete(1.0,tk.END)
        
        return True
        
    def draw_point(self):
        # Init draw point on the canvas
        self.canvas.delete("all")
        # init the canvas cities x & y
        for i in range(self.dimension):
            self.canvas_x.append(self.cities[i][1])
            self.canvas_y.append(self.cities[i][2])
        max_x = max(self.canvas_x)
        max_y = max(self.canvas_y)
        
        if max_x > 800:
            self.canvas_x = list(map(lambda x : x * 790.0 / max_x, self.canvas_x))
        if max_y > 600:
            self.canvas_y = list(map(lambda x : x * 590.0 / max_y, self.canvas_y))
        if max_x < 400:
            self.canvas_x = list(map(lambda x : x * 790.0 / max_x, self.canvas_x))
        if max_y < 600:
            self.canvas_y = list(map(lambda x : x * 590.0 / max_y, self.canvas_y))
            
        for i in range(self.dimension):
            x = self.canvas_x[i]
            y = self.canvas_y[i]
            r = 2
            self.canvas.create_oval(x - r, y - r, x + r, y + r,\
                                    fill="#ff0000", outline = "#000000", tags = 'node')
        return True
    
    def draw_path(self):
        # Init draw path on the canvas
        if self.path is None : 
            return False
        else:
            for i in range(1, self.dimension):
                self.canvas.create_line(self.canvas_x[self.path[i] - 1], self.canvas_y[self.path[i] - 1],\
                                        self.canvas_x[self.path[i - 1] - 1], self.canvas_y[self.path[i - 1] - 1], tags = 'li')
            self.canvas.create_line(self.canvas_x[self.path[-1] - 1], self.canvas_y[self.path[-1] - 1],\
                                    self.canvas_x[self.path[0] - 1  ], self.canvas_y[self.path[0] - 1], tags = 'li')
            return True

    def check_iterations(self):
        # the check function for running function
        # OK - True
        # NO - False
        if self.iterations_msg.get() == 0 :
            messagebox.showerror(title = 'Fatal Error', message = 'Iterations is ' \
                    + str(0) + ', refuse to execute, please reset the iterations !')
            return False
        elif self.iterations_msg.get() < 100 :
            return messagebox.askyesno(title = 'Warning', message = 'Iterations is small, suggest to reset, do you really want to execute ?')
        else:
            return True

    def set_GA(self):
        # ---- Init ---- #
        # 1. change the self.current_algorithm_msg
        self.current_algorithm_msg.set('GA')
        # 2. change the solver
        self.solver = GA.main
        return True

    def set_PSO(self):
        # ---- Init ---- #
        # 1. change the self.current_algorithm_msg
        self.current_algorithm_msg.set('PSO')
        self.solver = PSO.run
        return True

    def set_Hopfield(self):
        # ---- Init ---- #
        # 1. change the self.current_algorithm_msg
        self.current_algorithm_msg.set('Hopfield')
        self.solver = Hopfield.TSPThread().run
        return True

    def set_iterations(self, value):
        # set iterations, just set
        self.iterations_msg.set(value)

    def insert_best_result(self):
        # insert the best result into the self.best_text
        # refresh
        try:
            # still do not solve the question about rewrite the data in the text
            self.best_text.insert(1.0, self.best_result_tk + '\n')
        except Exception as e:
            print(e)
        
    def insert_search_text(self):
        # insert the log into the self.search_text
        try:
            print('insert the search box')
            self.search_text.insert(1.0, 'Loop %d, %f\n' % \
                                    (self.current_time, self.best_result))
        except Exception as e:
            print(e)
            
    def help_run(self, generate):
        for i, j, k in generate:
            print('iterations %d' % i)
            self.current_time = i
            if j < self.best_result:
                self.best_result  = j
                self.path         = k
                # fix the function widget
                self.best_result_tk = str(self.best_result)
                self.insert_best_result()
                # refrsh the canvas
                # self.canvas.delete("all")
                self.canvas.delete('li')
                self.draw_path()
                self.insert_search_text()
            # refresh the window
            self.window.update()

    def run(self):
        # check the runned flag
        if self.havebeenrunned == True:
            messagebox.showerror(title = 'Fatal Error', message = 'Please init the \
map before you execute the progrom !')
            return False
        else:
            # execute the algorithm
            if self.check_iterations() == False:
                return False
            else:
                self.set_runned(True)
        # execute normally
        print(self.current_algorithm_msg.get())
        if self.current_algorithm_msg.get() == 'GA':
            print("execute GA")
            # create the genertor of the solver
            generate = self.solver(100, self.dimension, self.cities_map, \
                        self.iterations_msg.get(), 20, 100, 0.9, 1, 5, 10)
        elif self.current_algorithm_msg.get() == 'PSO':
            print('execute PSO')
            generate = self.solver(self.cities_map, self.dimension,\
                                   self.iterations_msg.get(), 200, 10, 0.42)
        elif self.current_algorithm_msg.get() == 'Hopfield':
            print('execute Hopfield')
            generate = self.solver(self.iterations_msg.get(), self.dimension, self.fpath)
        else:
            print("execute other algorithm")
            return False
        self.help_run(generate)
        return True
    
    def set_runned(self, flag):
        self.havebeenrunned = flag
        if flag : 
            print("set runned !")
        else:
            print("set unrunned !")

if __name__ == "__main__":
    app = TSP()
    app.start()
