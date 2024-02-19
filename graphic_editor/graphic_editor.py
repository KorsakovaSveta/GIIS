import tkinter as tk
import numpy as np
import math
class GraphicEditor:
    def __init__(self):
     
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.window.winfo_screenwidth(), height=self.window.winfo_screenheight())
        
        self.mainmenu = tk.Menu(self.window)
        self.window.config(menu=self.mainmenu)
        self.line_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.line_menu.add_command(label="ЦДА", command=self.activate_canvas_cda)
        self.line_menu.add_command(label="Брезенхем", command=self.activate_canvas_brezenhem)
        self.line_menu.add_command(label="Ву", command=self.activate_canvas_wu)
        self.mainmenu.add_cascade(label="Отрезки", menu=self.line_menu)

        #self.cda = tk.Button(self.window, text="Отрезки", command=self.activate_canvas)
        self.mainmenu.add_cascade(label="Отладка", command=self.debug_mode_toggle)
        self.mainmenu.add_cascade(label="Остановить отладку", command=self.delete_grid)
        #self.canvas.create_line(0, 2, self.window.winfo_screenwidth(), 2, fill="gray")
        #self.cda.pack()   
        #self.canvas.bind("<Button-1>", self.on_mouse_click)     
  
        
        self.canvas.pack()
       
        self.points = []
        self.debug_mode = False
        self.grid_size = 10


    def activate_canvas_cda(self):
        self.canvas.bind('<Button-1>', self.on_mouse_click_cda)

    def activate_canvas_brezenhem(self):
        self.canvas.bind('<Button-1>', self.on_mouse_click_brezenhem)
    
    def activate_canvas_wu(self):
        self.canvas.bind('<Button-1>', self.on_mouse_click_wu)

    def debug_mode_toggle(self):
        self.canvas.delete("all")
        self.debug_mode = not self.debug_mode
        self.draw_grid()
       
       

    def on_mouse_click_cda(self, event):
        self.points.append((event.x, event.y))
        if len(self.points) == 2:           
            self.draw_line_cda()           
            self.points = []
    
    def on_mouse_click_brezenhem(self, event):
        self.points.append((event.x, event.y))
        if len(self.points) == 2:           
            self.draw_line_brezenhem()           
            self.points = []
    
    def on_mouse_click_wu(self, event):
        self.points.append((event.x, event.y))
        if len(self.points) == 2:           
            self.draw_line_wu()           
            self.points = []
        
    def draw_line_cda(self):
        #self.canvas.create_line(0, 2, self.window.winfo_screenwidth(), 2, fill="gray")
        #self.canvas.bind("<Button-1>", self.on_mouse_click)
        
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]

        length = max(abs(x2-x1), abs(y2-y1))
        
        dx = (x2 - x1)/length if length!= 0 else 0
        dy = (y2 - y1)/length if length!= 0 else 0
        sign_dx = np.sign(dx)
        sign_dy = np.sign(dy)

        x=x1 + 0.5*sign_dx
        y=y1 +0.5*sign_dy
        prev_x_grid=prev_y_grid=0
        for i in range(int(length+1)):
            if self.debug_mode:
                
                 # Округляем значения x и y до ближайшего кратного grid_size
                x_grid = x // self.grid_size
                y_grid = y // self.grid_size
                
                # Отображаем текущие значения x и y на сетке
                if x_grid!= prev_x_grid or y_grid!= prev_y_grid:
                    self.canvas.create_rectangle(x_grid*self.grid_size, y_grid*self.grid_size, (x_grid+1)*self.grid_size, (y_grid+1)*self.grid_size, fill='lightgray')
                    self.window.update()
                prev_x_grid = x_grid
                prev_y_grid = y_grid
                self.canvas.create_line(x, y, x+1, y+1)
                self.window.update()
                #self.window.after(50)
            else:
                self.canvas.create_line(x, y, x+1, y+1)
            x += dx
            y += dy
    
    def draw_line_brezenhem(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        e = 2*dy - dx
        x=x1
        y=y1
        prev_x_grid=prev_y_grid=0
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        while x!= x2 or y!= y2:
            if self.debug_mode:
                
                 # Округляем значения x и y до ближайшего кратного grid_size
                x_grid = x // self.grid_size
                y_grid = y // self.grid_size
                
                # Отображаем текущие значения x и y на сетке
                if x_grid!= prev_x_grid or y_grid!= prev_y_grid:
                    self.canvas.create_rectangle(x_grid*self.grid_size, y_grid*self.grid_size, (x_grid+1)*self.grid_size, (y_grid+1)*self.grid_size, fill='lightgray')
                    self.window.update()
                prev_x_grid = x_grid
                prev_y_grid = y_grid
                self.canvas.create_line(x, y, x+1, y+1)
                self.window.update()
                #self.window.after(50)
            else:
                self.canvas.create_line(x, y, x+1, y+1)
            if e>=0:
                y+=sy
                e-=2*dx
            else:
                x+=sx
                e+=2*dy
            
                #self.canvas.create_rectangle(x, y, x, y)

   

    
    def draw_line_wu(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 or dy == 0:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            return

        gradient = 0
        if dx > dy:
            gradient = dy / dx
            intery = y1 + gradient
            self.canvas.create_rectangle(x1, y1, x1, y1, fill="black")
            for x in range(x1, x2):
                self.canvas.create_rectangle(x, int(intery), x, int(intery), fill=self._get_color(self.fractional_part(intery)))
                self.canvas.create_rectangle(x, int(intery) + 1, x, int(intery) + 1, fill=self._get_color(1 - self.fractional_part(intery)))
                intery += gradient
            self.canvas.create_rectangle(x2, y2, x2, y2, fill="black")
        else:
            gradient = dx / dy
            interx = x1 + gradient
            self.canvas.create_rectangle(x1, y1, x1, y1, fill="black")
            for y in range(y1, y2):
                self.canvas.create_rectangle(int(interx), y, int(interx), y, fill=self._get_color(self.fractional_part(interx)))
                self.canvas.create_rectangle(int(interx) + 1, y, int(interx) + 1, y, fill=self._get_color(1 - self.fractional_part(interx)))
                interx += gradient
            self.canvas.create_rectangle(x2, y2, x2, y2, fill="black")

    def _get_color(self, alpha):
        alpha = int(alpha * 255)
        return f'#{alpha:02x}{alpha:02x}{alpha:02x}'

    @staticmethod
    def fractional_part(x):
        return x - int(x)

   
    # def fractional_part(number):
    #     _, fractional = math.modf(number)
    #     return fractional
        # dx = x2 - x1
        # dy = y2 - y1

        # # Determine the slope of the line
        # if abs(dx) > abs(dy):
        #     m = dy / dx
        #     steep = False
        # else:
        #     m = dx / dy
        #     steep = True

        # # Swap the coordinates if the line is steep
        # if steep:
        #     x1, y1 = y1, x1
        #     x2, y2 = y2, x2

        # # Swap the coordinates if the line goes from right to left
        # if x1 > x2:
        #     x1, x2 = x2, x1
        #     y1, y2 = y2, y1

        # # Calculate the initial fractional part of the y-intercept
        # y = y1 + m * (x1 - int(x1))

        # # Draw the first endpoint
        # self.canvas.create_line(int(x1), int(y1), int(x1) + 1, int(y1) + 1, fill='black')

        # # Draw the main part of the line
        # for x in range(int(x1) + 1, int(x2)):
        #     if steep:
        #         self.canvas.create_line(int(y), x, int(y) + 1, x + 1, fill='black', width=1)
        #         self.canvas.create_line(int(y) + 1, x, int(y) + 2, x + 1, fill='white', width=1)
        #     else:
        #         self.canvas.create_line(x, int(y), x + 1, int(y) + 1, fill='black', width=1)
        #         self.canvas.create_line(x, int(y) + 1, x + 1, int(y) + 2, fill='white', width=1)
        #     y += m

        # # Draw the last endpoint
        # self.canvas.create_line(int(x2), int(y2), int(x2) + 1, int(y2) + 1, fill='black')
            
    def draw_grid(self):
        for x in range(0, self.window.winfo_screenwidth(), self.grid_size):
            self.canvas.create_line(x, 0, x, self.window.winfo_screenheight(), fill="gray")
            
        for y in range(0, self.window.winfo_screenheight(), self.grid_size):
            self.canvas.create_line(0, y, self.window.winfo_screenwidth(), y, fill="gray")
        
    def delete_grid(self):        
        self.debug_mode = False
        self.canvas.delete("all")
        self.canvas.create_line(0, 2, self.window.winfo_screenwidth(), 2, fill="gray")
        #self.cda = tk.Button(text="Отрезки" , state="disabled")
        #self.debug = tk.Button(text="Отладка", state="disabled")

    def run(self):
        self.window.mainloop()
        

editor = GraphicEditor()
editor.run()

