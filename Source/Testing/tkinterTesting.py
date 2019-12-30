from tkinter import *

def main():
    root = Tk()
    frame = Frame(root, width=250, height=200)
    frame.pack()

    urlLabel = Label(frame, text="YouTube URL")
    urlEntry = Entry(frame)

    urlLabel.grid(row=0,column=0)
    urlEntry.grid(row=0,column=1)

    root.mainloop()


if __name__ == "__main__" :
    main()