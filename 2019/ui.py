# !/usr/bin/python3
# coding=utf8
import tkinter as tk

root = tk.Tk()

# constant
hashtb_cap = 8
canvas_width = 800
canvas_height = 800
rect_width = 80
rects_col1 = 150
rects_col2 = 550
# frame
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
# component
key_label = tk.Label(frame1, text="键")
key_input = tk.Entry(frame1)
value_label = tk.Label(frame1, text="值")
value_input = tk.Entry(frame1)

def insert():
    print("insert")


def delete():
    print("delete")

insert_button = tk.Button(frame1, text="插入", command=insert)  # command=xxx
delete_button = tk.Button(frame1, text="删除", command=delete)


canvas = tk.Canvas(frame2, width=canvas_width, height=canvas_height, bg='white')
canvas.create_text(200, 20, text="H1(x) = x mod "+str(hashtb_cap))
canvas.create_text(600, 20, text="H2(x) = (x div "+str(hashtb_cap)+") mod " + str(hashtb_cap))
for i in range(hashtb_cap):
    print(i)
    canvas.create_rectangle(rects_col1, 40+i*rect_width, rects_col1+rect_width, 40+(i+1)*rect_width, outline='blue')
    canvas.create_text(rects_col1-20, 40+20+i*rect_width, text=i)
    canvas.create_rectangle(rects_col2, 40+i*rect_width, rects_col2+rect_width, 40+(i+1)*rect_width, outline='blue')
    canvas.create_text(rects_col2-20, 40+20+i*rect_width, text=i)

# grid

key_label.grid(row=0, column=0, sticky='E')
key_input.grid(row=0, column=1)
value_label.grid(row=0, column=2, sticky='E')
value_input.grid(row=0, column=3)
insert_button.grid(row=0, column=4)
delete_button.grid(row=0, column=5)
frame1.grid(padx=20, pady=20)
canvas.grid()
frame2.grid(padx=10, pady=10)


# mainloop
root.mainloop()