import tkinter as tk

root = tk.Tk()
root.geometry("300x200")  # ウィンドウサイズ

# 背景用の Frame を作る
frame = tk.Frame(root, bg="lightblue")
frame.grid(row=0, column=0, sticky="nsew")

# ちゃんと広がるように grid の weight を設定
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ボタンを配置
btn = tk.Button(frame, text="Click Me")
btn.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()
