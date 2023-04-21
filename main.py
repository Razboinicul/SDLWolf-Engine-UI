import tkinter as tk
map = []
file_entry = None
new_map = {}
def load():
    global path_entry, map
    filepath = path_entry.get()
    print(filepath)
    try:
        raw_map = open(filepath, "r")
        map = raw_map.readlines()
        raw_map.close()
        i=0
        for l in map:
            new_map[i] = l.split()
            i+=1
        print(new_map)
        return new_map
    except:
        print("error")

def set():
    global row, col, obj, new_map
    print("test")
    _row = int(row.get())-1
    _col = int(col.get())-1
    _obj = int(obj.get())
    print(_row, _col, _obj)
    new_map[_row][_col] = str(_obj)
    
def save():
    global path_entry
    path = path_entry.get()
    print(path)
    text = """"""
    for i in new_map:
        _text = " ".join(new_map[i])
        if i == 0: text = _text
        else: text = text+"\n"+_text
    raw_map = open(path, "w")
    print(text)
    raw_map.write(text)
    raw_map.close()
    
def back(root):
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Select")
    root.resizable(False, False)
    map_editor_button = tk.Button(root, text='Map Editor', width=30, command=lambda: map_editor(root)).grid(row=0, column=0)
    exit_button =tk.Button(root, text='Exit', width=30, command=lambda: root.destroy()).grid(row=1, column=0)
    root.mainloop()

def map_editor(_root):
    _root.destroy()
    root = tk.Tk()
    root.title("Map Editor")
    root.resizable(False, False)
    row = tk.Entry(root, width=20)
    row.grid(row=0, column=0)
    col = tk.Entry(root, width=20)
    col.grid(row=1, column=0)
    obj = tk.Entry(root, width=20)
    obj.grid(row=2, column=0)
    path_entry = tk.Entry(root, width=20)
    path_entry.grid(row=0, column=1)
    button = tk.Button(root, text="Set", width=15, command=set).grid(row=3, column=0)
    save_button = tk.Button(root, text="Save .map file", command=save).grid(row=2, column=1)
    open_button = tk.Button(root, text='Load .map file', command=load).grid(row=1, column=1)
    back_button = tk.Button(root, text='Back', command=lambda: back(root)).grid(row=3, column=1)
    root.mainloop()

if __name__ == "__main__":
    main()
