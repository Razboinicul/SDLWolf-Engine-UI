import tkinter as tk
from shutil import copytree
from os.path import exists, join, basename, relpath
from os import startfile, walk, rename
from pathlib import Path
import zipfile as zip
from uuid import uuid4
from subprocess import run
import DiscordRPC
import threading
map = []
file_entry = None
new_map = {}
path_entry = None
row = None
col = None
obj = None
project_n = None
path_entry = None
mode_choice = None
project_name = None
project_path = None
project_mode = None
project_file_path = None
load_text = None
text_edit = None
error_l = None
options = {}
rpc = DiscordRPC.RPC.Set_ID(app_id=1102676096568275057)
button = DiscordRPC.button(button_one_label="SDLWolf Engine", button_one_url="https://r9-games.itch.io/sdlwolf-engine", button_two_label="SDLWolf Engine Repository", button_two_url="https://github.com/Noahnoah55/sdlwolf")
rpc.set_activity(state="                    ", details="Developing a game", buttons=button, timestamp=rpc.timestamp())
mode_options = ["Singleplayer"]
#                "Multiplayer"]

def start():
    #startfile("D:/sdl_test")
    root = tk.Tk()
    root.title("Project")
    root.resizable(False, False)
    new_button = tk.Button(root, text="New Project", width=20, command=lambda: new_project_ui(root)).grid(row=0, column=0)
    load_button = tk.Button(root, text="Load Project", width=20, command=lambda: load_project_ui(root)).grid(row=1, column=0)
    root.mainloop()

def create_project(_root):
    global project_n, path_entry, mode_choice, project_name, project_path, project_mode
    project_name = project_n.get()
    project_path = path_entry.get()
    project_mode = mode_choice.get()
    _root.destroy()
    print(project_name, project_path, project_mode)
    project_path = project_path.replace('\\', '/')
    exe_path = Path(__file__).parent.resolve()
    if project_mode == "Singleplayer":
        if not exists(project_path):
            copytree(f"{exe_path}\\sp_example", project_path)
        else:
            print("path already exists")
    with open(f"{project_path}\\project.sdlwolf", "w") as f:
        write_text = f"""name {project_name} 
mode {project_mode}"""
        f.write(write_text)
        f.close()
    main()
    
def load_project(_root, path):
    global project_name, project_path, project_mode, options
    _root.destroy()
    project_path = path.replace("/", "\\")
    f = open(f"{project_path}\\project.sdlwolf", "r")
    lines = f.readlines()
    print(lines)
    f.close()
    i=0
    for l in lines:
        options[i] = l.split()
        i+=1
    project_name = options[0][1]
    project_mode = options[1][1]
    main()
    
def export_project():
    rootdir = basename(project_path)
    with zip.ZipFile("export.zip", mode="w") as archive:
        startfile(f"{project_path}")
        for dirpath, dirnames, filenames in walk(f"{project_path}"):
            for filename in filenames:
                filepath = join(dirpath, filename)
                parentpath = relpath(filepath, project_path)
                arcname = join(rootdir, parentpath)
                archive.write(filepath, arcname)
        archive.write(filepath, arcname)
    rename("export.zip", "export.wolfpkg")
    rename("export.wolfpkg", f"{project_path}\\export.wolfpkg")
    

    
def new_project_ui(_root):
    global mode_options, project_n, path_entry, mode_choice
    _root.destroy()
    root = tk.Tk()
    root.title("New Project")
    root.resizable(False, False)
    np_label = tk.Label(root, text="New Project").grid(row=0, column=0)
    name_label = tk.Label(root, text="Project Name: ").grid(row=1, column=0)
    project_n = tk.Entry(root,  width=20)
    project_n.grid(row=2, column=0)
    path_label = tk.Label(root, text="Path: ").grid(row=3, column=0)
    path_entry = tk.Entry(root,  width=20)
    path_entry.grid(row=4, column=0)
    gamemode_label = tk.Label(root, text="Gamemode: ").grid(row=5, column=0)
    mode_choice = tk.StringVar(root)
    mode_choice.set(mode_options[0]) # default value
    mode_choice_o = tk.OptionMenu(root, mode_choice, *mode_options)
    mode_choice_o.grid(row=6, column=0)
    create_button = tk.Button(root, text="Create Project", width=20, command=lambda: create_project(root)).grid(row=7, column=0)
    root.mainloop()

def load_project_ui(_root):
    global mode_options, project_n, path_entry, mode_choice
    _root.destroy()
    root = tk.Tk()
    root.title("New Project")
    root.resizable(False, False)
    np_label = tk.Label(root, text="Load Project").grid(row=0, column=0)
    path_label = tk.Label(root, text="Path: ").grid(row=3, column=0)
    path_entry = tk.Entry(root,  width=20)
    path_entry.grid(row=4, column=0)
    create_button = tk.Button(root, text="Load Project", width=20, command=lambda: load_project(root, path_entry.get())).grid(row=7, column=0)
    root.mainloop()
    
def load(filepath):
    global map
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
    
def save(path):
    text = """"""
    for i in new_map:
        _text = " ".join(new_map[i])
        if i == 0: text = _text
        else: text = text+"\n"+_text
    raw_map = open(path, "w")
    print(text)
    raw_map.write(text)
    raw_map.close()
    
def load_file(filepath, text):
    f = open(filepath, "r")
    load_text = f.readlines()
    temp = """"""
    for l in load_text:
        temp = temp+l
    text.delete(0.3, "end")
    text.insert(0.3, temp)
    f.close()
    
def save_file(filepath, text):
    f = open(filepath, "w")
    f.writelines(text)
    f.close()
    
def back(root):
    root.destroy()
    main()

def main():
    root = tk.Tk()
    root.title("Select")
    root.resizable(False, False)
    map_editor_button = tk.Button(root, text='Map Editor', width=30, command=lambda: map_editor(root)).grid(row=0, column=0)
    text_editor_button = tk.Button(root, text='Text Editor', width=30, command=lambda: text_editor(root)).grid(row=1, column=0)
    assets_button = tk.Button(root, text='Open Assets Folder', width=30, command=lambda: startfile(f"{project_path}\\assets")).grid(row=2, column=0)
    export_button = tk.Button(root, text='Export Project', width=30, command=lambda: export_project()).grid(row=3, column=0)
    exit_button = tk.Button(root, text='Exit', width=30, command=lambda: root.destroy()).grid(row=4, column=0)
    root.mainloop()
    
def text_editor(_root):
    global error_l
    _root.destroy()
    root = tk.Tk()
    root.title("Text Editor")
    root.resizable(False, False)
    scrollbar =tk.Scrollbar(root, width=1)
    scrollbar.pack(side=tk.RIGHT)
    text_edit = tk.Text(root, width=70, height=30)
    text_edit.pack()
    scrollbar.config(command=text_edit.yview)
    error_l = tk.StringVar(root)
    error_l.set("-")
    error = tk.Label(root, textvariable=error_l).pack()
    analize_button = tk.Button(root, text='Analize Lua Code', width=50, command=lambda: analyze_code(f"{project_path}\\main.lua", text_edit.get(0.3, "end"), root)).pack()
    save_button = tk.Button(root, text='Save Lua File', width=50, command=lambda: save_file(f"{project_path}\\main.lua", text_edit.get(0.3, "end"))).pack()
    back_button = tk.Button(root, text='Back', width=50, command=lambda: back(root)).pack()
    load_file(f"{project_path}\\main.lua", text_edit)
    root.mainloop()
    
def analyze_code(filepath, text, root):
    save_file(filepath, text)
    process = run(["luau\\luau-analyze.exe", filepath], capture_output=True, text=True)
    err = process.stderr
    error_l.set(err)

def map_editor(_root):
    global col, row, obj, project_path
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
    button = tk.Button(root, text="Set", width=15, command=set).grid(row=3, column=0)
    col_save_button = tk.Button(root, text="Save .map collision file", command=lambda: save(f"{project_path}\\maps\\collision.map")).grid(row=0, column=2)
    col_open_button = tk.Button(root, text='Load .map collision file', command=lambda:load(f"{project_path}\\maps\\collision.map")).grid(row=0, column=1)
    light_save_button = tk.Button(root, text="Save .map light file", command=lambda: save(f"{project_path}\\maps\\light.map")).grid(row=1, column=2)
    light_open_button = tk.Button(root, text='Load .map light file', command=lambda:load(f"{project_path}\\maps\\light.map")).grid(row=1, column=1)
    back_button = tk.Button(root, text='Back', command=lambda: back(root)).grid(row=3, column=1)
    root.mainloop()
    
def rpc_func():
    rpc.run()

if __name__ == "__main__":
    rpc_thread = threading.Thread(target=rpc_func)
    rpc_thread.daemon = True
    rpc_thread.start()
    start()
