from tkinter import *

import constant


class ChinchorroCanvas:
    def __init__(self, canvas, thread_count, thread_length):
        self.canvas = canvas
        self.thread_count = thread_count
        self.thread_length = thread_length

    def draw_chinchorro(self, gradient_amt, gradient_pos, gradient_str):
        padding = 2
        gradient_amt_percent = gradient_amt / 100
        gradient_pos_percent = gradient_pos / 100

        gradient_thread_ct = (gradient_amt_percent * constant.GRADIENT_FULL_PERCENT) * self.thread_count
        color_inflection_thread = constant.THREAD_COUNT * gradient_pos_percent
        gradient_starting_thread = color_inflection_thread - (gradient_thread_ct / 2)
        gradient_ending_thread = gradient_starting_thread + gradient_thread_ct

        for i in range(self.thread_count):
            # print(i)
            # is_in_gradient = gradient_starting_thread <= i <= gradient_ending_thread
            # if is_in_gradient:

            # else:
            line_color = "blue" if i < color_inflection_thread else "orange"

            # Uncomment to show the gradient range
            # line_color = "red" if is_in_gradient else line_color
            self.canvas.create_line(padding + i, 2, padding + i, 200, fill=line_color)


window = Tk()
window.geometry("%dx%d" % (constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT))

print(constant.CANVAS_CONTROLS_WIDTH)
print(constant.CANVAS_CONTROLS_HEIGHT)
canvas_controls = Canvas(window, width=constant.CANVAS_CONTROLS_WIDTH,
                         height=constant.CANVAS_CONTROLS_HEIGHT)

scale_gradient_amt_val = IntVar()
scale_gradient_pos_val = IntVar()
scale_gradient_str_val = IntVar()


def chinchorro_callback(value=None):
    chinchorro.draw_chinchorro(scale_gradient_amt_val.get(),
                               scale_gradient_pos_val.get(),
                               scale_gradient_str_val.get())


lbl_gradient_amt = Label(canvas_controls, text="Gradient Amount")
scale_gradient_amt = Scale(canvas_controls, variable=scale_gradient_amt_val,
                           from_=0, to=100,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)
scale_gradient_amt.set(constant.GRADIENT_AMT)

lbl_gradient_pos = Label(canvas_controls, text="Gradient Position")
scale_gradient_pos = Scale(canvas_controls, variable=scale_gradient_pos_val,
                           from_=0, to=100,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)
scale_gradient_pos.set(constant.GRADIENT_POS)

lbl_gradient_str = Label(canvas_controls, text="Gradient Strength")
scale_gradient_str = Scale(canvas_controls, variable=scale_gradient_str_val,
                           from_=10, to=50,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)

b1 = Button(canvas_controls, text="Display Horizontal",
            command=chinchorro_callback,
            bg="yellow")

l1 = Label(canvas_controls)

canvas_controls.pack()
chinchorro_canvas = Canvas(window, width=constant.CANVAS_CHINCHORRO_WIDTH,
                           height=constant.CANVAS_CHINCHORRO_HEIGHT)
print(chinchorro_canvas)
chinchorro = ChinchorroCanvas(chinchorro_canvas, constant.THREAD_COUNT, constant.THREAD_LENGTH_CM)
chinchorro_callback()

lbl_gradient_amt.pack(anchor=CENTER)
scale_gradient_amt.pack(anchor=CENTER)
lbl_gradient_pos.pack(anchor=CENTER)
scale_gradient_pos.pack(anchor=CENTER)
lbl_gradient_str.pack(anchor=CENTER)
scale_gradient_str.pack(anchor=CENTER)
b1.pack(anchor=CENTER)
l1.pack()

chinchorro_canvas.pack(anchor=CENTER, fill=BOTH)

window.mainloop()
