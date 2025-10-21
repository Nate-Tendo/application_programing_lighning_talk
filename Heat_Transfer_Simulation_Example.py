import tkinter as tk
from tkinter import ttk

# ================================================================
# WINDOW AND FRAME SETUP
# ================================================================
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600

root = tk.Tk()
root.title("S.S. 1D Heat Transfer Simulation")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

main_window = ttk.Frame(master=root, borderwidth=5, relief='ridge', width=0.9*WINDOW_WIDTH, height=WINDOW_HEIGHT)
bottom_frame = ttk.Frame(master=main_window, borderwidth=5, relief='ridge', width=0.9*WINDOW_WIDTH, height=1/4*WINDOW_HEIGHT)
inputs_frame = ttk.Frame(master=bottom_frame)
materials_frame = ttk.Frame(master=bottom_frame)
outputs_frame = ttk.Frame(master=bottom_frame)

# ================================================================
# CANVAS DRAWING
# ================================================================
LEFT_GAP, RIGHT_GAP = 0.05, 0.20
canvas_width = 0.9 * WINDOW_WIDTH
canvas_height = 2/3 * WINDOW_HEIGHT

canvas = tk.Canvas(master=main_window, width=canvas_width, height=canvas_height, bg='white')
canvas.grid(row=0, column=0)

N_WALLS = 2
left_margin = LEFT_GAP * canvas_width
right_margin = RIGHT_GAP * canvas_width
wall_width = (canvas_width - left_margin - right_margin) / N_WALLS
top, bottom = 0.1 * canvas_height, 0.9 * canvas_height

# ================================================================
# TEMPERATURE VARIABLES AND CALCS
# ================================================================
T_min, T_max = 0, 1000
T_values = [0, 0, 0]  # initial T1, T2, T3

T1_var = tk.IntVar(value=1000)
T2_var = tk.DoubleVar(value=0)
T3_var = tk.DoubleVar(value=0)
T_inf_var = tk.DoubleVar(value=300.0)
h_var = tk.DoubleVar(value = 25.0)

k_constants = {'Wood':0.16, 'Brick':0.72, 'Steel':60.5}
MATERIAL_OPTIONS = ['Wood', 'Brick', 'Steel']
wall_vars = [tk.StringVar(value='Wood') for _ in range(N_WALLS)]
A = 2.0
L = 1.5

def temperature_calcs():
    T1 = float(T1_var.get())
    T_inf = float(T_inf_var.get())
    h = float(h_var.get())
    k1 = k_constants[wall_vars[0].get()]
    k2 = k_constants[wall_vars[1].get()]
    
    R1 = L / (k1*A)
    R2 = L / (k2*A)
    R_conv = 1/(h*A)
    R_tot = R1+R2+R_conv
    q = (T1 - T_inf)/R_tot
    T2 = T1 - q*R1
    T3 = T1 - q*(R1+R2)
    T_values[0] = T1
    T_values[1] = T2
    T_values[2] = T3
    T2_var.set(T2)
    T3_var.set(T3)
    return q, R1, R2, R_conv

# ================================================================
# COLOR AND GRADIENT FUNCTIONS
# ================================================================
def temp_to_color(T):
    """Map temperature to RGB color (blue=cold, red=hot)."""
    ratio = (T - T_min) / (T_max - T_min)
    ratio = max(0.0, min(1.0, ratio))  # clamp to [0,1]

    r = int(255 * ratio)
    g = 0
    b = int(255 * (1 - ratio))
    
    r = max(0, min(255, r))
    b = max(0, min(255, b))

    return f"#{r:02x}{g:02x}{b:02x}"

def draw_horizontal_gradient_rect(x1, y1, x2, y2, T_start, T_end, steps=50):
    """
    Draw a rectangle with a horizontal gradient from T_start (left) to T_end (right)
    """
    width = x2 - x1
    step_width = width / steps
    for i in range(steps):
        x_left = x1 + i * step_width
        x_right = x1 + (i + 1) * step_width
        # interpolate temperature
        T = T_start + (T_end - T_start) * (i / steps)
        color = temp_to_color(T)
        canvas.create_rectangle(x_left, y1, x_right, y2, outline="", fill=color)

   
def redraw_walls(*args):
    """Clear canvas and redraw walls with updated temperatures."""
    canvas.delete("all")  # remove old drawings

    # Compute updated temps from slider
    temperature_calcs()

    # Draw walls
    for i in range(N_WALLS):
        x1 = left_margin + i * wall_width
        x2 = x1 + wall_width
        draw_horizontal_gradient_rect(x1, top, x2, bottom, T_values[i], T_values[i+1])
        canvas.create_text(x1 + 8, (top + bottom)/2, text=f"T{i+1}", fill="black", anchor="w")
        canvas.create_text((x1 + x2)/2, bottom + 15, text=f"L = 1.5 m", fill="black")
        
        # Draw the wall edge
        canvas.create_rectangle(x1, top, x2, bottom, outline="black", width=2, fill="")

    # Labels
    canvas.create_text(left_margin + N_WALLS * wall_width + 8, (top + bottom)/2,
                       text=f"T{N_WALLS+1}", fill="black", anchor="w")
    canvas.create_text(left_margin - 10, (top + bottom)/2, text=f"A = 2.0 m²", fill="black", angle=90)

    # Convection arrows
    arrow_x = left_margin + N_WALLS * wall_width + right_margin / 2
    n_arrows = 4
    arrow_spacing = (bottom - top) / (n_arrows + 1)
    arrow_length = 25
    for i in range(n_arrows):
        y = bottom - (i + 1) * arrow_spacing
        canvas.create_line(arrow_x, y + arrow_length/2, arrow_x, y - arrow_length/2,
                           arrow=tk.LAST, width=2, fill="royalblue")
    canvas.create_text(arrow_x + 15, (top + bottom)/2, text="Convection (T∞), h = 25 W⋅m⁻²K⁻¹",
                       angle=90, fill="royalblue")
    
    T2_label.config(text=f"T2: {T2_var.get():.2f} K")
    T3_label.config(text=f"T3: {T3_var.get():.2f} K")

# ================================================================
# WIDGETS
# ================================================================
t1_label = tk.Label(master=inputs_frame, text="T1 (K):")
t1_scale = tk.Scale(master=inputs_frame, from_=1000, to=0, orient=tk.VERTICAL, variable=T1_var)
tinf_label = tk.Label(master=inputs_frame, text='T∞:')
tinf_entry = tk.Entry(master=inputs_frame, textvariable=T_inf_var, width=10)
tinf_units = tk.Label(master=inputs_frame, text='K')
T2_label = tk.Label(master=outputs_frame, text=f"T2: {T2_var.get()} K")
T3_label = tk.Label(master=outputs_frame, text=f"T3: {T3_var.get()} K")

material_labels = [tk.Label(master=materials_frame, text=f"Wall {i+1} Material:") for i in range(N_WALLS)]
material_menus = [ttk.Combobox(master=materials_frame, values=MATERIAL_OPTIONS,
                               textvariable=wall_vars[i], state='readonly', width=8) for i in range(N_WALLS)]

# ================================================================
# WIDGET PLACEMENT
# ================================================================
main_window.grid(row=0, column=0, padx=15, pady=5)
bottom_frame.grid(row=1, column=0)
inputs_frame.grid(row=0, column=0, padx=10)
materials_frame.grid(row=0, column=1, padx=20)
outputs_frame.grid(row=0, column=2, padx=20)

t1_label.grid(row=0, column=0)
t1_scale.grid(row=1, column=0, padx=(0,20))
tinf_label.grid(row=0, column=1, padx=(15,5))
tinf_entry.grid(row=0, column=2)
tinf_units.grid(row=0, column=3)

for i in range(N_WALLS):
    material_labels[i].grid(row=i, column=0, sticky='e')
    material_menus[i].grid(row=i, column=1, padx=5)

T2_label.grid(row=0, column=0, padx=10)
T3_label.grid(row=1, column=0, padx=10)

# ================================================================
# REDRAW WHENEVER VARIABLE CHANGES
# ================================================================
T1_var.trace_add("write", redraw_walls)
T_inf_var.trace_add("write", redraw_walls)
for menu in material_menus:
    menu.bind("<<ComboboxSelected>>", redraw_walls)

# Initial draw
redraw_walls()

# ================================================================
# START GUI
# ================================================================
root.mainloop()
