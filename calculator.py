"""
模仿 Windows 计算器的 Python GUI 程序
特殊功能：点击 "=" 按钮时，打开 Chrome 浏览器搜索计算器中的表达式
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import urllib.parse
import os

BROWSER_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ---------- 颜色主题 (Windows 11 深色风格) ----------
COLOR_BG = "#202020"
COLOR_BTN_NUM = "#323232"
COLOR_BTN_NUM_HOVER = "#3d3d3d"
COLOR_BTN_FUNC = "#2b2b2b"
COLOR_BTN_FUNC_HOVER = "#363636"
COLOR_BTN_OP = "#323232"
COLOR_BTN_OP_HOVER = "#3d3d3d"
COLOR_BTN_EQ = "#4cc2ff"
COLOR_BTN_EQ_HOVER = "#62c9ff"
COLOR_FG = "#ffffff"
COLOR_FG_FUNC = "#c0c0c0"
COLOR_FG_OP = "#4cc2ff"
COLOR_FG_HISTORY = "#6a6a6a"


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.geometry("380x580")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.history_var = tk.StringVar(value="")

        self._build_ui()
        self._bind_keys()

    # ---------- UI 构建 ----------
    def _build_ui(self):
        # 顶部标题栏
        header = tk.Frame(self.root, bg=COLOR_BG)
        header.pack(fill="x", padx=18, pady=(16, 4))
        tk.Label(
            header, text="☰  标准",
            font=("Segoe UI", 13),
            fg="#e8e8e8", bg=COLOR_BG
        ).pack(side="left")

        # 显示区域
        display_frame = tk.Frame(self.root, bg=COLOR_BG, height=120)
        display_frame.pack(fill="x", padx=18, pady=(6, 10))
        display_frame.pack_propagate(False)

        tk.Label(
            display_frame, textvariable=self.history_var,
            font=("Segoe UI", 12), fg=COLOR_FG_HISTORY,
            bg=COLOR_BG, anchor="e"
        ).pack(side="top", fill="x", pady=(20, 0))

        tk.Label(
            display_frame, textvariable=self.display_var,
            font=("Segoe UI", 42, "bold"), fg=COLOR_FG,
            bg=COLOR_BG, anchor="e"
        ).pack(side="top", fill="x")

        # 按钮区域
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(fill="both", expand=True, padx=8, pady=(4, 14))

        for r in range(6):
            btn_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            btn_frame.grid_columnconfigure(c, weight=1, uniform="col")

        layout = [
            [("%", "func"), ("CE", "func"), ("C", "func"), ("⌫", "func")],
            [("1/x", "func"), ("x²", "func"), ("√x", "func"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("±", "num"), ("0", "num"), (".", "num"), ("=", "eq")],
        ]
        for r, row in enumerate(layout):
            for c, (text, style) in enumerate(row):
                self._make_button(btn_frame, text, r, c, style)

    def _make_button(self, parent, text, row, col, style):
        colors = {
            "eq":   (COLOR_BTN_EQ,    "#ffffff",      COLOR_BTN_EQ_HOVER),
            "op":   (COLOR_BTN_OP,    COLOR_FG_OP,    COLOR_BTN_OP_HOVER),
            "func": (COLOR_BTN_FUNC,  COLOR_FG_FUNC,  COLOR_BTN_FUNC_HOVER),
            "num":  (COLOR_BTN_NUM,   COLOR_FG,       COLOR_BTN_NUM_HOVER),
        }
        bg, fg, hover_bg = colors[style]
        font_weight = "bold" if style in ("op", "eq") else "normal"
        font_size = 18 if style != "func" else 15

        btn = tk.Label(
            parent, text=text,
            font=("Segoe UI", font_size, font_weight),
            fg=fg, bg=bg, cursor="hand2"
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        btn.bind("<Button-1>", lambda e: self.on_button_click(text))

    # ---------- 键盘支持 ----------
    def _bind_keys(self):
        for ch in "0123456789.()+":
            self.root.bind(ch, lambda e, c=ch: self.on_button_click(c))
        self.root.bind("-", lambda e: self.on_button_click("−"))
        self.root.bind("*", lambda e: self.on_button_click("×"))
        self.root.bind("/", lambda e: self.on_button_click("÷"))
        self.root.bind("<Return>", lambda e: self.on_button_click("="))
        self.root.bind("<Escape>", lambda e: self.on_button_click("C"))
        self.root.bind("<BackSpace>", lambda e: self.on_button_click("⌫"))

    # ---------- 按钮逻辑 ----------
    def on_button_click(self, text):
        if text == "=":
            self._search_in_browser()
        elif text == "C":
            self.expression = ""
            self.display_var.set("0")
            self.history_var.set("")
        elif text == "CE":
            self.expression = ""
            self.display_var.set("0")
        elif text == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif text == "±":
            if self.expression:
                if self.expression.startswith("−"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "−" + self.expression
                self.display_var.set(self.expression)
        elif text == "x²":
            self.expression += "²"
            self.display_var.set(self.expression)
        elif text == "√x":
            self.expression += "√"
            self.display_var.set(self.expression)
        elif text == "1/x":
            self.expression = f"1/({self.expression})" if self.expression else "1/"
            self.display_var.set(self.expression)
        elif text == "%":
            self.expression += "%"
            self.display_var.set(self.expression)
        else:
            self.expression += text
            self.display_var.set(self.expression)

    # ---------- 搜索 ----------
    def _search_in_browser(self):
        if not self.expression.strip():
            return
        query = self.expression
        self.history_var.set(query + " =")

        confirm = messagebox.askyesno(
            "提示",
            "此计算超出我的能力范围，是否需要帮你深度搜索"
        )
        if confirm:
            search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
            try:
                subprocess.Popen([BROWSER_PATH, search_url])
            except Exception:
                try:
                    os.startfile(search_url)
                except Exception:
                    pass
        else:
            messagebox.showwarning("提示", "计算失败，不在我的计算范围之内")

        self.expression = ""
        self.display_var.set("0")


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
