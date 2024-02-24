from tkinter import *

import constant


class ChinchorroCanvas:
    def __init__(self, canvas, thread_count, thread_length):
        self.canvas = canvas
        self.thread_count = thread_count
        self.thread_length = thread_length
        self.colors = ["blue", "orange"]
        self.output = []

    def print_output(self):
        print(self.output)

    def gradient_formula(self, x: int, p: int):
        return float(pow(x, p))

    def draw_chinchorro(self, gradient_range, gradient_pos, gradient_str, gradient_pow):
        padding = 2
        gradient_amt_percent = gradient_range / 100
        gradient_pos_percent = gradient_pos / 100

        gradient_thread_ct = (gradient_amt_percent * constant.GRADIENT_FULL_PERCENT) * self.thread_count
        color_inflection_thread = constant.THREAD_COUNT * gradient_pos_percent
        gradient_starting_thread = color_inflection_thread - (gradient_thread_ct / 2)
        gradient_ending_thread = gradient_starting_thread + gradient_thread_ct

        # how many strength ranges are in the "range"
        str_in_range = (gradient_ending_thread - gradient_starting_thread) / gradient_str
        threads_in_str_range = gradient_thread_ct / str_in_range
        # Add one to the strength range top to fade into the solid color.
        top_gradient_str_range_number: float = self.gradient_formula(str_in_range, gradient_pow)

        # Loops through the threads while in the gradient
        j = 0
        # Tracking which strength range we're in.
        str_num = 1
        # Track the thread in each str_num
        k = 0
        # track all output
        self.output.clear()
        output_counter = 0
        output_last_color = None
        for i in range(self.thread_count):
            # print(i)
            is_in_gradient = gradient_starting_thread <= i <= gradient_ending_thread
            if is_in_gradient:
                #
                # x^2, range 0 to gradient thread count, x is the str_num (str_in_range?)
                # = y, percentage of range will be next color.
                # use J. Pretend y is 20%
                # If gradient_str is 20, every 4th thread should turn color.
                #    j % (gradient_str * y) == 0

                t = self.gradient_formula(str_num, gradient_pow)
                y: float = t / top_gradient_str_range_number
                # This tells how many threads in the range should have the next color.
                threads_to_be_gradientized = round(gradient_str * y)
                thread_index = (gradient_str / (threads_to_be_gradientized + 1))

                # Increment or reset the in-gradient-thread-index
                if j >= thread_index:
                    line_color = self.colors[1]
                    j = 0
                else:
                    line_color = self.colors[0]
                    j += 1

                # Increment or reset the str_num
                if k <= threads_in_str_range:
                    k += 1
                else:
                    k = 0
                    str_num += 1

                print("j-%d gradient_str-%d top-%f t-%f y-%f threads_to_be_gradientized-%f thread_index-%d" % (
                    j, gradient_str, top_gradient_str_range_number, t, y, threads_to_be_gradientized, thread_index))
            else:
                line_color = self.colors[0] if i < color_inflection_thread else self.colors[1]

            # Uncomment to show the gradient range
            # line_color = "red" if is_in_gradient else line_color
            output_counter += 1
            if output_last_color != line_color:
                if output_last_color is not None:
                    self.output.append((output_last_color, output_counter))
                    output_last_color = line_color
                    output_counter = 0
                else:
                    output_last_color = line_color
            if i == self.thread_count - 1:
                self.output.append((output_last_color, output_counter))

            line_coords = []
            lc = padding
            h_gap = 2
            v_gap = 2
            while lc < constant.THREAD_LENGTH_CM:
                i_padding = padding + i
                line_coords.append((i_padding, lc))
                line_coords.append((i_padding + h_gap, lc + v_gap))
                line_coords.append((i_padding + h_gap, lc + (v_gap * 2)))
                line_coords.append((i_padding, lc + (v_gap * 3)))
                line_coords.append((i_padding, lc + (v_gap * 4)))
                lc += v_gap * 4
                self.canvas.create_line(line_coords, fill=line_color)

            # self.canvas.create_line(padding + i, 2, padding + i, constant.THREAD_LENGTH_CM, fill=line_color)


window = Tk()
window.geometry("%dx%d" % (constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT))

print(constant.CANVAS_CONTROLS_WIDTH)
print(constant.CANVAS_CONTROLS_HEIGHT)
canvas_controls = Canvas(window, width=constant.CANVAS_CONTROLS_WIDTH,
                         height=constant.CANVAS_CONTROLS_HEIGHT)

scale_gradient_range_val = IntVar()
scale_gradient_pos_val = IntVar()
scale_gradient_str_val = IntVar()
scale_gradient_pow_val = IntVar()


def scale_set(range_val, pos_val, str_val, pow_val):
    scale_gradient_range.set(range_val)
    scale_gradient_pos_val.set(pos_val)
    scale_gradient_str_val.set(str_val)
    scale_gradient_pow_val.set(pow_val)


def button_callback_default():
    scale_set(constant.GRADIENT_AMT, constant.GRADIENT_POS, 10, 2)


def button_callback_1():
    scale_set(23, 50, 21, 1)


def chinchorro_callback(value=None):
    chinchorro.draw_chinchorro(scale_gradient_range_val.get(),
                               scale_gradient_pos_val.get(),
                               scale_gradient_str_val.get(),
                               scale_gradient_pow_val.get())
    chinchorro.print_output()


# 27 / 50 / 11/ 1
# 23 / 50 / 21 / 1
lbl_gradient_range = Label(canvas_controls, text="Gradient Range")
scale_gradient_range = Scale(canvas_controls, variable=scale_gradient_range_val,
                             from_=1, to=100,
                             command=chinchorro_callback,
                             orient=HORIZONTAL)
scale_gradient_range.set(constant.GRADIENT_AMT)

lbl_gradient_pos = Label(canvas_controls, text="Gradient Position")
scale_gradient_pos = Scale(canvas_controls, variable=scale_gradient_pos_val,
                           from_=0, to=100,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)
scale_gradient_pos.set(constant.GRADIENT_POS)

lbl_gradient_str = Label(canvas_controls, text="Gradient Strength")
scale_gradient_str = Scale(canvas_controls, variable=scale_gradient_str_val,
                           from_=2, to=100,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)
scale_gradient_str.set(10)

lbl_gradient_pow = Label(canvas_controls, text="Gradient Power")
scale_gradient_pow = Scale(canvas_controls, variable=scale_gradient_pow_val,
                           from_=1, to=20,
                           command=chinchorro_callback,
                           orient=HORIZONTAL)
scale_gradient_pow.set(2)

canvas_buttons = Canvas(canvas_controls, width=constant.CANVAS_CONTROLS_WIDTH*2)
btn_default = Button(canvas_buttons, text="Default", command=button_callback_default)
btn_one = Button(canvas_buttons, text="One", command=button_callback_1)

btn_default.pack()
btn_one.pack()
canvas_buttons.pack()

canvas_controls.pack()
chinchorro_canvas = Canvas(window, width=constant.CANVAS_CHINCHORRO_WIDTH,
                           height=constant.CANVAS_CHINCHORRO_HEIGHT)
print(chinchorro_canvas)
chinchorro = ChinchorroCanvas(chinchorro_canvas, constant.THREAD_COUNT, constant.THREAD_LENGTH_CM)
chinchorro_callback()

lbl_gradient_range.pack(anchor=CENTER)
scale_gradient_range.pack(anchor=CENTER)
lbl_gradient_pos.pack(anchor=CENTER)
scale_gradient_pos.pack(anchor=CENTER)
lbl_gradient_str.pack(anchor=CENTER)
scale_gradient_str.pack(anchor=CENTER)
lbl_gradient_pow.pack(anchor=CENTER)
scale_gradient_pow.pack(anchor=CENTER)

chinchorro_canvas.pack(anchor=CENTER, fill=BOTH)

window.mainloop()
