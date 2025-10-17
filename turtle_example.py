import tkinter as tk
import turtle

def draw_square(t):
    for _ in range(4):
        t.forward(100)
        t.right(90)

root = tk.Tk()
root.title("Turtle in Tkinter")

canvas = tk.Canvas(master=root, width=600, height=400)
canvas.pack()

screen = turtle.TurtleScreen(canvas)
screen.bgcolor("lightblue")

my_turtle = turtle.RawTurtle(screen, shape="turtle")
my_turtle.color("green")

draw_square(my_turtle) # Call a function to draw with the turtle

root.mainloop()