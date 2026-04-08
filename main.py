import tkinter as tk
from tkinter import ttk, messagebox
import math

# ══════════════════════════════════════════════════════════════
#  CONVERTER DATA
# ══════════════════════════════════════════════════════════════
CONVERTERS = {
    "Currency": {
        "units": ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)",
                  "JPY (¥)", "CAD ($)", "AUD ($)", "CNY (¥)",
                  "AED (د.إ)", "SGD ($)"],
        "rates": {
            "USD ($)": 1.0, "INR (₹)": 83.5, "EUR (€)": 0.92,
            "GBP (£)": 0.79, "JPY (¥)": 149.5, "CAD ($)": 1.36,
            "AUD ($)": 1.53, "CNY (¥)": 7.24,
            "AED (د.إ)": 3.67, "SGD ($)": 1.34,
        }, "icon": "💱"
    },
    "Length": {
        "units": ["Meter","Kilometer","Mile","Foot",
                  "Inch","Centimeter","Millimeter","Yard"],
        "rates": {
            "Meter":1.0,"Kilometer":0.001,"Mile":0.000621371,
            "Foot":3.28084,"Inch":39.3701,"Centimeter":100.0,
            "Millimeter":1000.0,"Yard":1.09361,
        }, "icon": "📏"
    },
    "Weight & mass": {
        "units": ["Kilogram","Gram","Pound","Ounce",
                  "Ton","Milligram","Stone"],
        "rates": {
            "Kilogram":1.0,"Gram":1000.0,"Pound":2.20462,
            "Ounce":35.274,"Ton":0.001,
            "Milligram":1_000_000.0,"Stone":0.157473,
        }, "icon": "⚖"
    },
    "Temperature": {
        "units": ["Celsius","Fahrenheit","Kelvin"],
        "rates": {}, "icon": "🌡"
    },
    "Volume": {
        "units": ["Liter","Milliliter","Gallon (US)",
                  "Pint","Cup","Fluid Ounce","Cubic Meter"],
        "rates": {
            "Liter":1.0,"Milliliter":1000.0,
            "Gallon (US)":0.264172,"Pint":2.11338,
            "Cup":4.22675,"Fluid Ounce":33.814,
            "Cubic Meter":0.001,
        }, "icon": "⬤"
    },
    "Area": {
        "units": ["Square Meter","Square Kilometer",
                  "Square Mile","Square Foot","Acre","Hectare"],
        "rates": {
            "Square Meter":1.0,"Square Kilometer":1e-6,
            "Square Mile":3.861e-7,"Square Foot":10.7639,
            "Acre":0.000247105,"Hectare":0.0001,
        }, "icon": "▦"
    },
    "Speed": {
        "units": ["m/s","km/h","mph","knot","ft/s"],
        "rates": {
            "m/s":1.0,"km/h":3.6,"mph":2.23694,
            "knot":1.94384,"ft/s":3.28084,
        }, "icon": "🚀"
    },
    "Time": {
        "units": ["Second","Minute","Hour",
                  "Day","Week","Month","Year"],
        "rates": {
            "Second":1.0,"Minute":1/60,"Hour":1/3600,
            "Day":1/86400,"Week":1/604800,
            "Month":1/2_629_800,"Year":1/31_557_600,
        }, "icon": "🕐"
    },
    "Power": {
        "units": ["Watt","Kilowatt","Megawatt",
                  "Horsepower","BTU/hr"],
        "rates": {
            "Watt":1.0,"Kilowatt":0.001,"Megawatt":1e-6,
            "Horsepower":0.00134102,"BTU/hr":3.41214,
        }, "icon": "🔋"
    },
    "Energy": {
        "units": ["Joule","Kilojoule","Calorie",
                  "Kilocalorie","kWh","BTU"],
        "rates": {
            "Joule":1.0,"Kilojoule":0.001,
            "Calorie":0.239006,"Kilocalorie":0.000239006,
            "kWh":2.778e-7,"BTU":0.000947817,
        }, "icon": "⚡"
    },
    "Pressure": {
        "units": ["Pascal","Bar","PSI","Atmosphere","Torr"],
        "rates": {
            "Pascal":1.0,"Bar":1e-5,"PSI":0.000145038,
            "Atmosphere":9.8692e-6,"Torr":0.00750062,
        }, "icon": "🔩"
    },
    "Angle": {
        "units": ["Degree","Radian","Gradian"],
        "rates": {
            "Degree":1.0,"Radian":math.pi/180,"Gradian":10/9,
        }, "icon": "∠"
    },
    "Data": {
        "units": ["Byte","Kilobyte","Megabyte",
                  "Gigabyte","Terabyte","Bit"],
        "rates": {
            "Byte":1.0,"Kilobyte":1/1024,
            "Megabyte":1/1024**2,"Gigabyte":1/1024**3,
            "Terabyte":1/1024**4,"Bit":8.0,
        }, "icon": "💾"
    },
}


# ══════════════════════════════════════════════════════════════
#  STANDARD CALCULATOR PANEL
# ══════════════════════════════════════════════════════════════
class StandardPanel(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors     = colors
        self.expression = ""
        self.disp_var   = tk.StringVar(value="0")
        self.form_var   = tk.StringVar(value="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build()

    def _build(self):
        C = self.colors

        # Display
        disp = tk.Frame(self, bg=C["bg"])
        disp.grid(row=0, column=0, sticky="ew",
                  padx=20, pady=(10, 0))
        disp.grid_columnconfigure(0, weight=1)

        tk.Label(disp, textvariable=self.form_var,
                 font=("Segoe UI", 11), bg=C["bg"],
                 fg=C["txt_gray"], anchor="e").grid(
                     row=0, column=0, sticky="e")

        self.res_lbl = tk.Label(
            disp, textvariable=self.disp_var,
            font=("Segoe UI", 52, "bold"),
            bg=C["bg"], fg=C["txt_white"], anchor="e")
        self.res_lbl.grid(row=1, column=0, sticky="e")

        # Buttons
        body = tk.Frame(self, bg=C["bg"])
        body.grid(row=1, column=0, sticky="nsew",
                  padx=6, pady=6)
        body.grid_columnconfigure(tuple(range(4)), weight=1)

        # Memory row
        mem_row = tk.Frame(body, bg=C["bg"])
        mem_row.grid(row=0, column=0, columnspan=4,
                     sticky="ew", pady=(0, 4))
        for t, cb in [("%",  self._percent),
                      ("CE", self._ce),
                      ("C",  self._clear),
                      ("⌫",  self._back)]:
            tk.Button(mem_row, text=t,
                      font=("Segoe UI", 10),
                      bg=C["bg"], fg=C["txt_gray"],
                      bd=0, padx=12, pady=3,
                      cursor="hand2",
                      activebackground=C["btn_sci"],
                      relief="flat",
                      command=cb).pack(
                          side="left", padx=6)

        N, O, E = "N", "O", "E"
        grid = [
            [("MC","N"),("MR","N"),("M+","N"),
             ("M−","N"),("MS","N")],
            [("¹/x","O"),("|x|","O"),("x²","O"),
             ("√x","O"),("÷","O")],
            [("7","N"),("8","N"),("9","N"),("×","O")],
            [("4","N"),("5","N"),("6","N"),("−","O")],
            [("1","N"),("2","N"),("3","N"),("+","O")],
            [("+/−","N"),("0","N"),(".","N"),("=","E")],
        ]

        sm = {
            "N":(C["btn_num"],C["hover_num"],C["txt_white"]),
            "O":(C["btn_op"], C["hover_op"], C["txt_white"]),
            "E":(C["btn_eq"], C["btn_eq_h"], C["txt_white"]),
        }

        mem_labels = {"MC","MR","M+","M−","MS"}

        for r, row in enumerate(grid):
            body.grid_rowconfigure(r+1, weight=1)
            cols = 4 if r > 0 else 5
            skip = 0

            for c, (lbl, sty) in enumerate(row):
                bg, hbg, fg = sm[sty]
                if lbl in mem_labels:
                    fg = C["txt_gray"]

                cmd = self._make_cmd(lbl)
                span = 1
                actual_c = c

                btn = tk.Button(body, text=lbl,
                                font=("Segoe UI", 14),
                                bg=bg, fg=fg,
                                activebackground=hbg,
                                activeforeground=fg,
                                bd=0, relief="flat",
                                cursor="hand2",
                                command=cmd)
                btn.grid(row=r+1, column=actual_c,
                         sticky="nsew",
                         padx=2, pady=2)

    def _make_cmd(self, lbl):
        ops = {"÷":"/","×":"*","−":"-","+":"+"}
        if lbl in "0123456789":
            return lambda l=lbl: self._digit(l)
        elif lbl == ".":
            return self._dot
        elif lbl in ops:
            return lambda o=ops[lbl]: self._op(o)
        elif lbl == "=":  return self._equals
        elif lbl == "C":  return self._clear
        elif lbl == "CE": return self._ce
        elif lbl == "⌫":  return self._back
        elif lbl == "%":  return self._percent
        elif lbl == "x²": return self._square
        elif lbl == "√x": return self._sqrt
        elif lbl == "¹/x":return self._recip
        elif lbl == "|x|":return self._abs
        elif lbl == "+/−":return self._negate
        elif lbl == "MC": return self._mc
        elif lbl == "MR": return self._mr
        elif lbl == "M+": return self._mplus
        elif lbl == "M−": return self._mminus
        elif lbl == "MS": return self._ms
        return lambda: None

    # ── Memory ────────────────────────────────────────────────
    mem = 0.0
    def _mc(self):    StandardPanel.mem = 0.0
    def _mr(self):
        self.expression = str(StandardPanel.mem)
        self._refresh(self.expression)
    def _ms(self):
        try: StandardPanel.mem = float(self.disp_var.get())
        except: pass
    def _mplus(self):
        try: StandardPanel.mem += float(self.disp_var.get())
        except: pass
    def _mminus(self):
        try: StandardPanel.mem -= float(self.disp_var.get())
        except: pass

    # ── Input ─────────────────────────────────────────────────
    def _digit(self, d):
        if self.disp_var.get() in ("Error","0"):
            self.expression = d
        else:
            self.expression += d
        self._refresh(self.expression)

    def _dot(self):
        if "." not in self.expression:
            self.expression += "."
            self._refresh(self.expression)

    def _op(self, op):
        self.expression += op
        self._refresh(self.expression)

    def _equals(self):
        try:
            formula = self.expression
            self.form_var.set(formula + " =")
            r = eval(formula, {"__builtins__":{}}, {})
            res = (str(int(r)) if isinstance(r, float)
                   and r.is_integer() else f"{r:.10g}")
            self.expression = res
            self._refresh(res)
        except ZeroDivisionError:
            self._refresh("Cannot ÷ 0")
            self.expression = ""
        except:
            self._refresh("Error")
            self.expression = ""

    def _clear(self):
        self.expression = ""
        self.form_var.set("")
        self._refresh()

    def _ce(self):
        self.expression = ""
        self._refresh()

    def _back(self):
        self.expression = self.expression[:-1]
        self._refresh(self.expression)

    def _percent(self):
        try:
            v = float(self.expression) / 100
            self.expression = str(v)
            self._refresh(self.expression)
        except: pass

    def _square(self):
        try:
            v = float(self.expression) ** 2
            self.expression = str(v)
            self._refresh(self.expression)
        except: pass

    def _sqrt(self):
        try:
            v = math.sqrt(float(self.expression))
            self.expression = str(v)
            self._refresh(self.expression)
        except: pass

    def _recip(self):
        try:
            v = 1 / float(self.expression)
            self.expression = str(v)
            self._refresh(self.expression)
        except: pass

    def _abs(self):
        try:
            v = abs(float(self.expression))
            self.expression = str(v)
            self._refresh(self.expression)
        except: pass

    def _negate(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression
        self._refresh(self.expression)

    def _refresh(self, val=""):
        if not val:
            self.disp_var.set("0")
            return
        disp = val if len(val) <= 18 else val[-18:] + "…"
        self.disp_var.set(disp)


# ══════════════════════════════════════════════════════════════
#  GRAPHING CALCULATOR PANEL
# ══════════════════════════════════════════════════════════════
class GraphingPanel(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._functions = []
        self._colors_list = [
            "#e8896a","#4fc3f7","#81c784",
            "#ff8a65","#ba68c8","#4db6ac"
        ]
        self._build()

    def _build(self):
        C = self.colors

        # ── Top controls ──────────────────────────────────────
        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew",
                 padx=14, pady=8)
        top.grid_columnconfigure(1, weight=1)

        tk.Label(top, text="f(x) =",
                 font=("Segoe UI", 13, "bold"),
                 bg=C["bg"],
                 fg=C["txt_orange"]).grid(
                     row=0, column=0, padx=(0, 8))

        self.expr_var = tk.StringVar(value="sin(x)")
        entry = tk.Entry(top, textvariable=self.expr_var,
                         font=("Segoe UI", 13),
                         bg=C["btn_sci"],
                         fg=C["txt_white"],
                         insertbackground=C["txt_white"],
                         relief="flat", bd=8)
        entry.grid(row=0, column=1, sticky="ew")
        entry.bind("<Return>", lambda e: self._plot())

        tk.Button(top, text="Plot",
                  font=("Segoe UI", 11, "bold"),
                  bg=C["btn_eq"], fg=C["txt_white"],
                  bd=0, padx=14, pady=6,
                  cursor="hand2",
                  activebackground=C["btn_eq_h"],
                  relief="flat",
                  command=self._plot).grid(
                      row=0, column=2, padx=(8, 0))

        tk.Button(top, text="Clear All",
                  font=("Segoe UI", 10),
                  bg=C["btn_sci"],
                  fg=C["txt_gray"],
                  bd=0, padx=10, pady=6,
                  cursor="hand2",
                  activebackground=C["hover_sci"],
                  relief="flat",
                  command=self._clear_all).grid(
                      row=0, column=3, padx=(6, 0))

        # X range
        range_frame = tk.Frame(self, bg=C["bg"])
        range_frame.grid(row=1, column=0, sticky="ew",
                         padx=14, pady=(0, 6))

        for i, (lbl, var, val) in enumerate([
            ("X min:", "xmin_var", "-10"),
            ("X max:", "xmax_var", "10"),
            ("Y min:", "ymin_var", "-10"),
            ("Y max:", "ymax_var", "10"),
        ]):
            tk.Label(range_frame, text=lbl,
                     font=("Segoe UI", 9),
                     bg=C["bg"],
                     fg=C["txt_gray"]).grid(
                         row=0, column=i*2,
                         padx=(8, 2))
            sv = tk.StringVar(value=val)
            setattr(self, var, sv)
            tk.Entry(range_frame, textvariable=sv,
                     font=("Segoe UI", 10),
                     bg=C["btn_sci"],
                     fg=C["txt_white"],
                     insertbackground=C["txt_white"],
                     width=5, relief="flat", bd=4,
                     justify="center").grid(
                         row=0, column=i*2+1,
                         padx=(0, 4))

        # ── Main area: canvas + legend ─────────────────────────
        mid = tk.Frame(self, bg=C["bg"])
        mid.grid(row=2, column=0, sticky="nsew",
                 padx=14, pady=(0, 8))
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Canvas
        self.canvas = tk.Canvas(
            mid, bg="#0d1117",
            highlightthickness=1,
            highlightbackground=C["sep"])
        self.canvas.grid(row=0, column=0,
                         sticky="nsew")
        self.canvas.bind("<Configure>",
                         lambda e: self._redraw())

        # Legend panel
        self.legend = tk.Frame(mid, bg=C["btn_sci"],
                               width=160)
        self.legend.grid(row=0, column=1,
                         sticky="nsew", padx=(6, 0))
        self.legend.grid_propagate(False)

        tk.Label(self.legend, text="Functions",
                 font=("Segoe UI", 10, "bold"),
                 bg=C["btn_sci"],
                 fg=C["txt_white"]).pack(
                     pady=(10, 4))

        self.legend_inner = tk.Frame(
            self.legend, bg=C["btn_sci"])
        self.legend_inner.pack(fill="both",
                               expand=True, padx=6)

        # ── Quick presets ─────────────────────────────────────
        presets = tk.Frame(self, bg=C["bg"])
        presets.grid(row=3, column=0, sticky="ew",
                     padx=14, pady=(0, 8))

        tk.Label(presets, text="Quick:",
                 font=("Segoe UI", 9),
                 bg=C["bg"],
                 fg=C["txt_gray"]).pack(side="left",
                                        padx=(0, 6))

        for expr in ["sin(x)","cos(x)","tan(x)",
                     "x**2","x**3","1/x",
                     "sqrt(abs(x))","exp(x/5)"]:
            tk.Button(presets, text=expr,
                      font=("Segoe UI", 9),
                      bg=C["btn_sci"],
                      fg=C["txt_orange"],
                      bd=0, padx=8, pady=3,
                      cursor="hand2",
                      activebackground=C["hover_sci"],
                      relief="flat",
                      command=lambda e=expr: self._quick(e)
                      ).pack(side="left", padx=2)

    def _quick(self, expr):
        self.expr_var.set(expr)
        self._plot()

    def _plot(self):
        expr = self.expr_var.get().strip()
        if not expr:
            return
        color = self._colors_list[
            len(self._functions) % len(self._colors_list)]
        self._functions.append((expr, color))
        self._update_legend()
        self._redraw()

    def _clear_all(self):
        self._functions.clear()
        self._update_legend()
        self.canvas.delete("all")
        self._draw_axes()

    def _update_legend(self):
        for w in self.legend_inner.winfo_children():
            w.destroy()
        C = self.colors
        for i, (expr, col) in enumerate(self._functions):
            row = tk.Frame(self.legend_inner,
                           bg=C["btn_sci"])
            row.pack(fill="x", pady=2)

            tk.Frame(row, bg=col, width=12,
                     height=12).pack(side="left",
                                     padx=(0, 4))
            tk.Label(row, text=expr[:18],
                     font=("Segoe UI", 8),
                     bg=C["btn_sci"],
                     fg=C["txt_white"],
                     anchor="w").pack(side="left",
                                      fill="x",
                                      expand=True)

            idx = i
            tk.Button(row, text="✕",
                      font=("Segoe UI", 8),
                      bg=C["btn_sci"],
                      fg=C["txt_gray"],
                      bd=0, cursor="hand2",
                      activebackground=C["hover_sci"],
                      command=lambda i=idx:
                          self._remove(i)).pack(
                              side="right")

    def _remove(self, idx):
        if 0 <= idx < len(self._functions):
            self._functions.pop(idx)
            self._update_legend()
            self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        self._draw_axes()
        for expr, color in self._functions:
            self._draw_function(expr, color)

    def _draw_axes(self):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 2 or H < 2:
            return

        try:
            xmin = float(self.xmin_var.get())
            xmax = float(self.xmax_var.get())
            ymin = float(self.ymin_var.get())
            ymax = float(self.ymax_var.get())
        except:
            return

        # Grid lines
        for i in range(int(xmin)-1, int(xmax)+2):
            sx = self._sx(i, xmin, xmax, W)
            self.canvas.create_line(
                sx, 0, sx, H,
                fill="#1e2a3a", width=1)
        for i in range(int(ymin)-1, int(ymax)+2):
            sy = self._sy(i, ymin, ymax, H)
            self.canvas.create_line(
                0, sy, W, sy,
                fill="#1e2a3a", width=1)

        # Axes
        ox = self._sx(0, xmin, xmax, W)
        oy = self._sy(0, ymin, ymax, H)
        self.canvas.create_line(
            ox, 0, ox, H, fill="#444", width=2)
        self.canvas.create_line(
            0, oy, W, oy, fill="#444", width=2)

        # Labels
        for i in range(int(xmin), int(xmax)+1, 2):
            if i == 0:
                continue
            sx = self._sx(i, xmin, xmax, W)
            self.canvas.create_text(
                sx, oy+12, text=str(i),
                fill="#555", font=("Segoe UI", 7))

        for i in range(int(ymin), int(ymax)+1, 2):
            if i == 0:
                continue
            sy = self._sy(i, ymin, ymax, H)
            self.canvas.create_text(
                ox+14, sy, text=str(i),
                fill="#555", font=("Segoe UI", 7))

    def _draw_function(self, expr, color):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 2 or H < 2:
            return

        try:
            xmin = float(self.xmin_var.get())
            xmax = float(self.xmax_var.get())
            ymin = float(self.ymin_var.get())
            ymax = float(self.ymax_var.get())
        except:
            return

        safe = {
            "__builtins__": {},
            "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "sqrt": math.sqrt,
            "abs": abs, "log": math.log,
            "log10": math.log10, "log2": math.log2,
            "exp": math.exp, "pi": math.pi,
            "e": math.e, "asin": math.asin,
            "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh,
            "tanh": math.tanh, "ceil": math.ceil,
            "floor": math.floor,
        }

        points = []
        steps  = W * 2

        for i in range(steps + 1):
            x = xmin + (xmax - xmin) * i / steps
            try:
                safe["x"] = x
                y = eval(expr, safe)
                if (not math.isfinite(y) or
                        y < ymin - 1 or y > ymax + 1):
                    if points:
                        if len(points) >= 4:
                            self.canvas.create_line(
                                points, fill=color,
                                width=2, smooth=True)
                        points = []
                    continue
                sx = self._sx(x, xmin, xmax, W)
                sy = self._sy(y, ymin, ymax, H)
                points.append(sx)
                points.append(sy)
            except:
                if points and len(points) >= 4:
                    self.canvas.create_line(
                        points, fill=color,
                        width=2, smooth=True)
                points = []

        if points and len(points) >= 4:
            self.canvas.create_line(
                points, fill=color,
                width=2, smooth=True)

    def _sx(self, x, xmin, xmax, W):
        return (x - xmin) / (xmax - xmin) * W

    def _sy(self, y, ymin, ymax, H):
        return H - (y - ymin) / (ymax - ymin) * H


# ══════════════════════════════════════════════════════════════
#  CONVERTER PANEL
# ══════════════════════════════════════════════════════════════
class ConverterPanel(tk.Frame):
    def __init__(self, parent, name, data, colors, back_cb):
        super().__init__(parent, bg=colors["bg"])
        self.name    = name
        self.data    = data
        self.colors  = colors
        self.back_cb = back_cb
        C = colors
        self.grid_columnconfigure(0, weight=1)

        # Top bar
        top = tk.Frame(self, bg=C["bg"])
        top.grid(row=0, column=0, sticky="ew",
                 padx=16, pady=(14, 4))
        top.grid_columnconfigure(1, weight=1)

        tk.Button(top, text="← Back",
                  font=("Segoe UI", 11),
                  bg=C["bg"], fg=C["txt_orange"],
                  bd=0, cursor="hand2",
                  activebackground=C["btn_sci"],
                  command=back_cb).grid(
                      row=0, column=0, sticky="w")

        tk.Label(top,
                 text=f"{data['icon']}  {name}",
                 font=("Segoe UI", 18, "bold"),
                 bg=C["bg"],
                 fg=C["txt_white"],
                 anchor="w").grid(
                     row=0, column=1,
                     sticky="w", padx=12)

        # Card
        card = tk.Frame(self, bg=C["btn_num"],
                        relief="flat")
        card.grid(row=1, column=0, sticky="ew",
                  padx=20, pady=10)
        card.grid_columnconfigure((0, 1), weight=1)

        units = data["units"]

        # FROM
        tk.Label(card, text="From",
                 font=("Segoe UI", 10),
                 bg=C["btn_num"],
                 fg=C["txt_gray"]).grid(
                     row=0, column=0, sticky="w",
                     padx=16, pady=(14, 2))

        self.from_var = tk.StringVar(value=units[0])
        from_dd = ttk.Combobox(
            card, textvariable=self.from_var,
            values=units, state="readonly",
            font=("Segoe UI", 12))
        from_dd.grid(row=1, column=0, sticky="ew",
                     padx=16, pady=(0, 8))

        self.from_entry = tk.Entry(
            card, font=("Segoe UI", 22, "bold"),
            bg=C["btn_sci"], fg=C["txt_white"],
            insertbackground=C["txt_white"],
            relief="flat", bd=8, justify="right")
        self.from_entry.grid(row=2, column=0,
                             sticky="ew",
                             padx=16, pady=(0, 16))
        self.from_entry.insert(0, "1")

        # Swap
        tk.Button(card, text="⇄",
                  font=("Segoe UI", 18),
                  bg=C["btn_num"],
                  fg=C["txt_orange"],
                  bd=0, cursor="hand2",
                  activebackground=C["btn_sci"],
                  command=self._swap).grid(
                      row=1, column=0,
                      columnspan=2, pady=4)

        # TO
        tk.Label(card, text="To",
                 font=("Segoe UI", 10),
                 bg=C["btn_num"],
                 fg=C["txt_gray"]).grid(
                     row=0, column=1, sticky="w",
                     padx=16, pady=(14, 2))

        self.to_var = tk.StringVar(
            value=units[1] if len(units) > 1
            else units[0])
        to_dd = ttk.Combobox(
            card, textvariable=self.to_var,
            values=units, state="readonly",
            font=("Segoe UI", 12))
        to_dd.grid(row=1, column=1, sticky="ew",
                   padx=16, pady=(0, 8))

        self.to_entry = tk.Entry(
            card, font=("Segoe UI", 22, "bold"),
            bg=C["btn_sci"], fg=C["txt_orange"],
            insertbackground=C["txt_white"],
            relief="flat", bd=8, justify="right",
            state="readonly")
        self.to_entry.grid(row=2, column=1,
                           sticky="ew",
                           padx=16, pady=(0, 16))

        # Convert button
        tk.Button(self, text="Convert",
                  font=("Segoe UI", 13, "bold"),
                  bg=C["btn_eq"], fg=C["txt_white"],
                  bd=0, pady=12, cursor="hand2",
                  activebackground=C["btn_eq_h"],
                  relief="flat",
                  command=self._convert).grid(
                      row=2, column=0, sticky="ew",
                      padx=20, pady=(0, 8))

        self.result_lbl = tk.Label(
            self, text="",
            font=("Segoe UI", 13),
            bg=C["bg"], fg=C["txt_orange"],
            wraplength=500, justify="center")
        self.result_lbl.grid(row=3, column=0,
                             sticky="ew", padx=20)

        self._build_ref_table()

        self.from_var.trace_add(
            "write", lambda *a: self._convert())
        self.to_var.trace_add(
            "write", lambda *a: self._convert())
        self.from_entry.bind(
            "<KeyRelease>", lambda e: self._convert())
        self._convert()

    def _convert(self):
        try:
            val = float(self.from_entry.get())
        except ValueError:
            self.result_lbl.configure(
                text="⚠ Enter a valid number")
            return
        frm = self.from_var.get()
        to  = self.to_var.get()

        if self.name == "Temperature":
            result = self._temp(val, frm, to)
        else:
            rates  = self.data["rates"]
            base   = val / rates[frm]
            result = base * rates[to]

        res = (f"{result:.6g}"
               if abs(result) < 1e10 else f"{result:.4e}")

        self.to_entry.configure(state="normal")
        self.to_entry.delete(0, "end")
        self.to_entry.insert(0, res)
        self.to_entry.configure(state="readonly")
        self.result_lbl.configure(
            text=f"  {val:g} {frm}  =  {res} {to}")

    def _temp(self, val, frm, to):
        c = (val if frm == "Celsius"
             else (val-32)*5/9 if frm == "Fahrenheit"
             else val - 273.15)
        return (c if to == "Celsius"
                else c*9/5+32 if to == "Fahrenheit"
                else c + 273.15)

    def _swap(self):
        f, t = self.from_var.get(), self.to_var.get()
        self.from_var.set(t)
        self.to_var.set(f)
        self._convert()

    def _build_ref_table(self):
        C = self.colors
        frame = tk.LabelFrame(
            self, text="  Quick Reference",
            font=("Segoe UI", 10),
            bg=C["bg"], fg=C["txt_gray"],
            bd=1, relief="flat", labelanchor="nw")
        frame.grid(row=4, column=0, sticky="nsew",
                   padx=20, pady=(4, 16))
        frame.grid_columnconfigure((0,1), weight=1)

        for ci, h in enumerate(["Unit","Rate"]):
            tk.Label(frame, text=h,
                     font=("Segoe UI", 9, "bold"),
                     bg=C["bg"], fg=C["accent"],
                     anchor="w").grid(
                         row=0, column=ci,
                         sticky="w", padx=10,
                         pady=(8, 2))

        if self.name == "Temperature":
            rows = [("Celsius","°C base"),
                    ("Fahrenheit","C×9/5+32"),
                    ("Kelvin","C+273.15")]
            for ri, (u, f) in enumerate(rows):
                for ci, v in enumerate([u, f]):
                    tk.Label(frame, text=v,
                             font=("Segoe UI", 9),
                             bg=C["bg"],
                             fg=(C["txt_white"]
                                 if ri%2==0
                                 else C["txt_gray"]),
                             anchor="w").grid(
                                 row=ri+1, column=ci,
                                 sticky="w",
                                 padx=10, pady=2)
        else:
            for ri, (u, r) in enumerate(
                    self.data["rates"].items()):
                fmt = (f"{r:.6g}" if r >= 0.001
                       else f"{r:.3e}")
                for ci, v in enumerate([u, fmt]):
                    tk.Label(frame, text=v,
                             font=("Segoe UI", 9),
                             bg=C["bg"],
                             fg=(C["txt_white"]
                                 if ri%2==0
                                 else C["txt_gray"]),
                             anchor="w").grid(
                                 row=ri+1, column=ci,
                                 sticky="w",
                                 padx=10, pady=2)


# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════
class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("1100x780")
        self.root.minsize(820, 620)
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)

        self.expression   = ""
        self.display_text = tk.StringVar(value="0")
        self.formula_text = tk.StringVar(value="")
        self.memory       = 0.0
        self.history      = []
        self.angle_mode   = "DEG"
        self.sidebar_open = True
        self.fe_mode      = False
        self.hist_visible = False
        self.current_view = "scientific"

        self.C = {
            "bg"        : "#1e1e1e",
            "sidebar"   : "#202020",
            "display"   : "#1e1e1e",
            "btn_sci"   : "#2b2b2b",
            "btn_num"   : "#333333",
            "btn_op"    : "#3d3d3d",
            "btn_eq"    : "#d4855a",
            "btn_eq_h"  : "#bf7048",
            "hover_sci" : "#383838",
            "hover_num" : "#404040",
            "hover_op"  : "#4a4a4a",
            "txt_white" : "#ffffff",
            "txt_gray"  : "#888888",
            "txt_orange": "#d4855a",
            "accent"    : "#d4855a",
            "sep"       : "#333333",
        }

        self._build_ui()
        self.root.bind("<Key>", self._keyboard)
        self.root.bind("<Configure>", self._on_resize)

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = tk.Frame(
            self.root, bg=self.C["sidebar"], width=230)
        self.sidebar_frame.grid(row=0, column=0,
                                sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self._build_sidebar()

        self.main = tk.Frame(self.root, bg=self.C["bg"])
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=0)
        self.main.grid_rowconfigure(1, weight=1)

        self._build_header()

        self.content = tk.Frame(self.main,
                                bg=self.C["bg"])
        self.content.grid(row=1, column=0,
                          sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._show_scientific()

    # ── Sidebar ───────────────────────────────────────────────
    def _build_sidebar(self):
        sb = self.sidebar_frame
        canvas = tk.Canvas(sb, bg=self.C["sidebar"],
                           highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(sb, orient="vertical",
                                  command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=self.C["sidebar"])
        win_id = canvas.create_window(
            (0, 0), window=inner, anchor="nw")

        def _ri(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", _ri)

        def _us(e):
            canvas.configure(
                scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", _us)

        def _wheel(e):
            canvas.yview_scroll(
                int(-1*(e.delta/120)), "units")
        canvas.bind("<MouseWheel>", _wheel)
        inner.bind("<MouseWheel>", _wheel)

        # Hamburger
        top = tk.Frame(inner, bg=self.C["sidebar"])
        top.pack(fill="x", pady=(12, 8))
        tk.Button(top, text="☰",
                  font=("Segoe UI", 15),
                  bg=self.C["sidebar"],
                  fg=self.C["txt_white"],
                  bd=0, padx=14, cursor="hand2",
                  activebackground=self.C["btn_sci"],
                  command=self._toggle_sidebar).pack(
                      side="left")

        items = [
            ("🧮", "Standard",  "standard"),
            ("🔬", "Scientific","scientific"),
            ("📐", "Graphing",  "graphing"),
            ("__sep__","",""),
            ("__hdr__","Converter",""),
        ]
        for key in CONVERTERS:
            items.append(
                (CONVERTERS[key]["icon"], key, key))
        items += [("__sep__","",""),
                  ("⚙","Settings","settings")]

        self._nav_rows = {}

        for icon, label, key in items:
            if icon == "__sep__":
                tk.Frame(inner, bg=self.C["sep"],
                         height=1).pack(
                             fill="x", pady=6,
                             padx=12)
                continue
            if icon == "__hdr__":
                tk.Label(inner, text=label,
                         font=("Segoe UI", 9),
                         bg=self.C["sidebar"],
                         fg=self.C["txt_gray"],
                         anchor="w").pack(
                             fill="x", padx=18,
                             pady=(2, 4))
                continue

            is_active = (key == self.current_view)
            bg_c = (self.C["btn_sci"]
                    if is_active
                    else self.C["sidebar"])

            row = tk.Frame(inner, bg=bg_c,
                           cursor="hand2")
            row.pack(fill="x")

            if is_active:
                tk.Frame(row, bg=self.C["accent"],
                         width=3).place(
                             x=0, y=0, relheight=1)

            il = tk.Label(row, text=icon,
                          font=("Segoe UI", 13),
                          bg=bg_c,
                          fg=self.C["txt_white"])
            il.pack(side="left",
                    padx=(18, 8), pady=9)

            nl = tk.Label(row, text=label,
                          font=("Segoe UI", 11),
                          bg=bg_c,
                          fg=self.C["txt_white"],
                          anchor="w")
            nl.pack(side="left", fill="x")

            self._nav_rows[key] = (row, il, nl)

            def _click(e, k=key):
                self._nav_select(k)

            def _enter(e, f=row, il=il, nl=nl):
                c = self.C["hover_sci"]
                f.configure(bg=c)
                il.configure(bg=c)
                nl.configure(bg=c)

            def _leave(e, f=row, k=key,
                       il=il, nl=nl):
                c = (self.C["btn_sci"]
                     if self.current_view == k
                     else self.C["sidebar"])
                f.configure(bg=c)
                il.configure(bg=c)
                nl.configure(bg=c)

            for w in (row, il, nl):
                w.bind("<Button-1>", _click)
                w.bind("<Enter>", _enter)
                w.bind("<Leave>", _leave)
                w.bind("<MouseWheel>", _wheel)

    def _nav_select(self, key):
        prev = self.current_view
        self.current_view = key

        # Reset old
        if prev in self._nav_rows:
            r, il, nl = self._nav_rows[prev]
            c = self.C["sidebar"]
            r.configure(bg=c)
            il.configure(bg=c)
            nl.configure(bg=c)
            for ch in r.winfo_children():
                if (isinstance(ch, tk.Frame) and
                        ch.cget("bg") ==
                        self.C["accent"]):
                    ch.destroy()

        # Activate new
        if key in self._nav_rows:
            r, il, nl = self._nav_rows[key]
            c = self.C["btn_sci"]
            r.configure(bg=c)
            il.configure(bg=c)
            nl.configure(bg=c)
            bar = tk.Frame(r, bg=self.C["accent"],
                           width=3)
            bar.place(x=0, y=0, relheight=1)

        # Switch view
        if key == "scientific":
            self._show_scientific()
        elif key == "standard":
            self._show_standard()
        elif key == "graphing":
            self._show_graphing()
        elif key in CONVERTERS:
            self._show_converter(key)
        else:
            self._show_coming_soon(key)

    # ── Header ────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.main, bg=self.C["bg"],
                       height=52)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        tk.Button(hdr, text="☰",
                  font=("Segoe UI", 15),
                  bg=self.C["bg"],
                  fg=self.C["txt_white"],
                  bd=0, padx=12, pady=8,
                  cursor="hand2",
                  activebackground=self.C["btn_sci"],
                  command=self._toggle_sidebar).grid(
                      row=0, column=0, sticky="w")

        self.title_lbl = tk.Label(
            hdr, text="Scientific",
            font=("Segoe UI", 17, "bold"),
            bg=self.C["bg"],
            fg=self.C["txt_white"])
        self.title_lbl.grid(row=0, column=1,
                            sticky="w", padx=4)

        tab = tk.Frame(hdr, bg=self.C["bg"])
        tab.grid(row=0, column=2,
                 sticky="e", padx=16)

        self._tab_btn(
            tab, "History",
            self._toggle_history,
            active=True).pack(side="left")
        self._tab_btn(
            tab, "Memory",
            self._show_memory).pack(
                side="left", padx=8)

    def _tab_btn(self, parent, text, cmd,
                 active=False):
        f = tk.Frame(parent, bg=self.C["bg"])
        tk.Button(f, text=text,
                  font=("Segoe UI", 11),
                  bg=self.C["bg"],
                  fg=(self.C["txt_white"] if active
                      else self.C["txt_gray"]),
                  bd=0, padx=6, cursor="hand2",
                  activebackground=self.C["bg"],
                  command=cmd).pack()
        if active:
            tk.Frame(f, bg=self.C["accent"],
                     height=2).pack(fill="x")
        return f

    # ── Views ─────────────────────────────────────────────────
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _show_standard(self):
        self._clear_content()
        self.title_lbl.configure(text="Standard")
        p = StandardPanel(self.content, self.C)
        p.grid(row=0, column=0, sticky="nsew")

    def _show_scientific(self):
        self._clear_content()
        self.title_lbl.configure(text="Scientific")
        sci = tk.Frame(self.content, bg=self.C["bg"])
        sci.grid(row=0, column=0, sticky="nsew")
        sci.grid_columnconfigure(0, weight=1)
        sci.grid_rowconfigure(1, weight=1)
        self._build_display(sci)
        self._build_calc_body(sci)

    def _show_graphing(self):
        self._clear_content()
        self.title_lbl.configure(text="Graphing")
        p = GraphingPanel(self.content, self.C)
        p.grid(row=0, column=0, sticky="nsew")

    def _show_converter(self, name):
        self._clear_content()
        self.title_lbl.configure(text=name)
        ConverterPanel(
            self.content, name,
            CONVERTERS[name], self.C,
            back_cb=lambda:
                self._nav_select("scientific")
        ).grid(row=0, column=0, sticky="nsew")

    def _show_coming_soon(self, name):
        self._clear_content()
        self.title_lbl.configure(
            text=name.capitalize())
        tk.Label(self.content,
                 text=f"🚧\n{name.capitalize()}"
                      f"\nComing Soon",
                 font=("Segoe UI", 20),
                 bg=self.C["bg"],
                 fg=self.C["txt_gray"],
                 justify="center").grid(
                     row=0, column=0)

    # ── Display ───────────────────────────────────────────────
    def _build_display(self, parent):
        disp = tk.Frame(parent, bg=self.C["display"])
        disp.grid(row=0, column=0, sticky="ew",
                  padx=20, pady=(6, 0))
        disp.grid_columnconfigure(0, weight=1)

        self.hist_popup  = tk.Frame(parent,
                                    bg="#252525")
        self.hist_visible = False

        tk.Label(disp,
                 textvariable=self.formula_text,
                 font=("Segoe UI", 11),
                 bg=self.C["display"],
                 fg=self.C["txt_gray"],
                 anchor="e").grid(
                     row=0, column=0, sticky="e")

        self.result_lbl = tk.Label(
            disp, textvariable=self.display_text,
            font=("Segoe UI", 52, "bold"),
            bg=self.C["display"],
            fg=self.C["txt_white"], anchor="e")
        self.result_lbl.grid(
            row=1, column=0, sticky="e")

    # ── Calc body ─────────────────────────────────────────────
    def _build_calc_body(self, parent):
        body = tk.Frame(parent, bg=self.C["bg"])
        body.grid(row=1, column=0, sticky="nsew",
                  padx=6, pady=6)
        body.grid_columnconfigure(
            tuple(range(5)), weight=1)

        # Mode row
        mr = tk.Frame(body, bg=self.C["bg"])
        mr.grid(row=0, column=0, columnspan=5,
                sticky="w", pady=(0, 4))
        self.deg_btn = tk.Button(
            mr, text=self.angle_mode,
            font=("Segoe UI", 10, "bold"),
            bg=self.C["accent"],
            fg=self.C["txt_white"],
            bd=0, padx=12, pady=4,
            cursor="hand2",
            activebackground=self.C["btn_eq_h"],
            relief="flat",
            command=self._toggle_angle)
        self.deg_btn.pack(side="left", padx=4)
        tk.Button(mr, text="F-E",
                  font=("Segoe UI", 10),
                  bg=self.C["btn_sci"],
                  fg=self.C["txt_gray"],
                  bd=0, padx=12, pady=4,
                  cursor="hand2",
                  activebackground=self.C["hover_sci"],
                  relief="flat",
                  command=self._toggle_fe).pack(
                      side="left", padx=4)

        # Memory row
        memr = tk.Frame(body, bg=self.C["bg"])
        memr.grid(row=1, column=0, columnspan=5,
                  sticky="ew", pady=(2, 4))
        for t, cb in [("MC",self._mc),("MR",self._mr),
                      ("M+",self._m_plus),
                      ("M−",self._m_minus),
                      ("MS",self._ms)]:
            tk.Button(memr, text=t,
                      font=("Segoe UI", 10),
                      bg=self.C["bg"],
                      fg=self.C["txt_gray"],
                      bd=0, padx=14, pady=3,
                      cursor="hand2",
                      activebackground=self.C["btn_sci"],
                      relief="flat",
                      command=cb).pack(
                          side="left", padx=4)

        tk.Frame(body, bg=self.C["sep"],
                 height=1).grid(
                     row=2, column=0,
                     columnspan=5,
                     sticky="ew", pady=4)

        sr = tk.Frame(body, bg=self.C["bg"])
        sr.grid(row=3, column=0, columnspan=5,
                sticky="w", pady=(0, 6))
        tk.Button(sr, text="△  Trigonometry  ▾",
                  font=("Segoe UI", 10),
                  bg=self.C["bg"],
                  fg=self.C["txt_white"],
                  bd=0, padx=8, pady=4,
                  cursor="hand2",
                  activebackground=self.C["btn_sci"],
                  relief="flat",
                  command=self._trig_menu).pack(
                      side="left", padx=4)
        tk.Button(sr, text="ƒ  Function  ▾",
                  font=("Segoe UI", 10),
                  bg=self.C["bg"],
                  fg=self.C["txt_white"],
                  bd=0, padx=8, pady=4,
                  cursor="hand2",
                  activebackground=self.C["btn_sci"],
                  relief="flat",
                  command=self._func_menu).pack(
                      side="left", padx=10)

        S, N, O, E = "S","N","O","E"
        grid_def = [
            [("2ⁿᵈ",self._toggle_second,S),
             ("π",lambda:self._insert("math.pi"),S),
             ("e",lambda:self._insert("math.e"),S),
             ("C",self._clear,O),
             ("⌫",self._backspace,O)],
            [("x²",lambda:self._suffix("**2"),S),
             ("¹/x",lambda:self._suffix("**-1"),S),
             ("|x|",lambda:self._wrap("abs("),S),
             ("exp",lambda:self._wrap("math.exp("),N),
             ("mod",lambda:self._insert("%"),N)],
            [("²√x",lambda:self._wrap("math.sqrt("),S),
             ("(",lambda:self._insert("("),N),
             (")",lambda:self._insert(")"),N),
             ("n!",lambda:self._wrap("math.factorial("),N),
             ("÷",lambda:self._insert("/"),O)],
            [("xʸ",lambda:self._insert("**"),S),
             ("7",lambda:self._insert("7"),N),
             ("8",lambda:self._insert("8"),N),
             ("9",lambda:self._insert("9"),N),
             ("×",lambda:self._insert("*"),O)],
            [("10ˣ",lambda:self._wrap("10**("),S),
             ("4",lambda:self._insert("4"),N),
             ("5",lambda:self._insert("5"),N),
             ("6",lambda:self._insert("6"),N),
             ("−",lambda:self._insert("-"),O)],
            [("log",lambda:self._wrap("math.log10("),S),
             ("1",lambda:self._insert("1"),N),
             ("2",lambda:self._insert("2"),N),
             ("3",lambda:self._insert("3"),N),
             ("+",lambda:self._insert("+"),O)],
            [("ln",lambda:self._wrap("math.log("),S),
             ("+/−",self._negate,N),
             ("0",lambda:self._insert("0"),N),
             (".",lambda:self._insert("."),N),
             ("=",self._evaluate,E)],
        ]
        sm = {
            S:(self.C["btn_sci"],self.C["hover_sci"],
               self.C["txt_orange"]),
            N:(self.C["btn_num"],self.C["hover_num"],
               self.C["txt_white"]),
            O:(self.C["btn_op"],self.C["hover_op"],
               self.C["txt_white"]),
            E:(self.C["btn_eq"],self.C["btn_eq_h"],
               self.C["txt_white"]),
        }
        for r, row in enumerate(grid_def):
            body.grid_rowconfigure(r+4, weight=1)
            for c, (lbl, cmd, sty) in enumerate(row):
                bg, hbg, fg = sm[sty]
                tk.Button(body, text=lbl,
                          font=("Segoe UI", 13),
                          bg=bg, fg=fg,
                          activebackground=hbg,
                          activeforeground=fg,
                          bd=0, relief="flat",
                          cursor="hand2",
                          command=cmd).grid(
                              row=r+4, column=c,
                              sticky="nsew",
                              padx=2, pady=2)

    # ── Resize ────────────────────────────────────────────────
    def _on_resize(self, event=None):
        try:
            w = self.root.winfo_width()
            s = max(24, min(52, int(w/22)))
            self.result_lbl.config(
                font=("Segoe UI", s, "bold"))
        except: pass

    # ── Input helpers ─────────────────────────────────────────
    def _insert(self, ch):
        if self.display_text.get() in (
                "Error","Cannot ÷ 0"):
            self.expression = ""
        self.expression += str(ch)
        self._refresh(self.expression)

    def _suffix(self, s):
        self.expression += s
        self._refresh(self.expression)

    def _wrap(self, fn):
        cur = self.expression
        if cur and cur not in ("Error","Cannot ÷ 0"):
            self.expression = fn + cur + ")"
        else:
            self.expression = fn
        self._refresh(self.expression)

    def _refresh(self, val=""):
        if not val:
            self.display_text.set("0"); return
        disp = (val if len(val) <= 20
                else val[-20:] + "…")
        self.display_text.set(disp)

    # ── Actions ───────────────────────────────────────────────
    def _clear(self):
        self.expression = ""
        self.formula_text.set("")
        self._refresh()

    def _backspace(self):
        self.expression = self.expression[:-1]
        self._refresh(self.expression)

    def _negate(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression
        self._refresh(self.expression)

    def _toggle_second(self): pass

    def _toggle_angle(self):
        self.angle_mode = (
            "RAD" if self.angle_mode == "DEG"
            else "DEG")
        try:
            self.deg_btn.config(text=self.angle_mode)
        except: pass

    def _toggle_fe(self):
        try:
            val = float(self.display_text.get())
            self._refresh(f"{val:.4e}"
                          if not self.fe_mode
                          else f"{val:.10g}")
            self.fe_mode = not self.fe_mode
        except: pass

    def _evaluate(self):
        if not self.expression: return
        formula = self.expression
        self.formula_text.set(formula + " =")
        expr = self._preprocess(formula)
        try:
            r = eval(expr, {"__builtins__":{}},
                     {"math":math,"abs":abs,
                      "round":round})
            rs = (str(int(r))
                  if isinstance(r,float)
                  and r.is_integer()
                  and abs(r) < 1e15
                  else f"{r:.10g}")
            self.expression = rs
            self._refresh(rs)
            self.history.append(f"{formula} = {rs}")
            self._update_history_panel()
        except ZeroDivisionError:
            self._refresh("Cannot ÷ 0")
            self.expression = ""
        except:
            self._refresh("Error")
            self.expression = ""

    def _preprocess(self, expr):
        import re
        if self.angle_mode == "DEG":
            for fn in ("sin","cos","tan"):
                expr = re.sub(
                    rf"math\.{fn}\(([^)]+)\)",
                    lambda m,f=fn:
                        f"math.{f}(math.radians"
                        f"({m.group(1)}))",
                    expr)
            for fn in ("asin","acos","atan"):
                expr = re.sub(
                    rf"math\.{fn}\(([^)]+)\)",
                    lambda m,f=fn:
                        f"math.degrees(math.{f}"
                        f"({m.group(1)}))",
                    expr)
        return expr

    # ── Memory ────────────────────────────────────────────────
    def _mc(self):    self.memory = 0.0
    def _mr(self):
        self.expression = str(self.memory)
        self._refresh(self.expression)
    def _ms(self):
        try: self.memory = float(
            self.display_text.get())
        except: pass
    def _m_plus(self):
        try: self.memory += float(
            self.display_text.get())
        except: pass
    def _m_minus(self):
        try: self.memory -= float(
            self.display_text.get())
        except: pass
    def _show_memory(self):
        messagebox.showinfo(
            "Memory", f"Stored: {self.memory}")

    # ── History ───────────────────────────────────────────────
    def _toggle_history(self):
        self.hist_visible = not self.hist_visible
        try:
            if self.hist_visible:
                self.hist_popup.grid(
                    row=0, column=0,
                    sticky="nsew",
                    padx=8, pady=4)
                self.hist_popup\
                    .grid_columnconfigure(0, weight=1)
                self.hist_popup\
                    .grid_rowconfigure(0, weight=1)
                self._update_history_panel()
            else:
                self.hist_popup.grid_remove()
        except: pass

    def _update_history_panel(self):
        try:
            for w in self.hist_popup.winfo_children():
                w.destroy()
            c = tk.Canvas(self.hist_popup,
                           bg="#252525",
                           highlightthickness=0,
                           height=140)
            sb = ttk.Scrollbar(
                self.hist_popup, orient="vertical",
                command=c.yview)
            c.configure(yscrollcommand=sb.set)
            sb.grid(row=0, column=1, sticky="ns")
            c.grid(row=0, column=0, sticky="nsew")
            inner = tk.Frame(c, bg="#252525")
            c.create_window((0,0), window=inner,
                            anchor="nw")
            if not self.history:
                tk.Label(inner,
                         text="No history yet.",
                         font=("Segoe UI",11),
                         bg="#252525",
                         fg=self.C["txt_gray"]).pack(
                             pady=10, padx=10)
            else:
                for h in reversed(
                        self.history[-30:]):
                    tk.Label(inner, text=h,
                             font=("Segoe UI",11),
                             bg="#252525",
                             fg=self.C["txt_white"],
                             anchor="e").pack(
                                 fill="x",
                                 padx=12, pady=2)
            inner.update_idletasks()
            c.configure(
                scrollregion=c.bbox("all"))
        except: pass

    # ── Menus ─────────────────────────────────────────────────
    def _trig_menu(self):
        m = tk.Menu(self.root, tearoff=0,
                    bg="#2b2b2b",
                    fg=self.C["txt_white"],
                    font=("Segoe UI",11),
                    activebackground=self.C["btn_sci"],
                    activeforeground=
                        self.C["txt_white"])
        for fn in ["sin","cos","tan","asin",
                   "acos","atan","sinh",
                   "cosh","tanh"]:
            m.add_command(
                label=fn,
                command=lambda f=fn:
                    self._insert(f"math.{f}("))
        m.post(self.root.winfo_pointerx(),
               self.root.winfo_pointery())

    def _func_menu(self):
        m = tk.Menu(self.root, tearoff=0,
                    bg="#2b2b2b",
                    fg=self.C["txt_white"],
                    font=("Segoe UI",11),
                    activebackground=self.C["btn_sci"],
                    activeforeground=
                        self.C["txt_white"])
        for lbl, code in [
            ("floor(x)","math.floor("),
            ("ceil(x)", "math.ceil("),
            ("round(x)","round("),
            ("log₂(x)", "math.log2("),
            ("log(x,b)","math.log("),
            ("degrees(x)","math.degrees("),
            ("radians(x)","math.radians("),
            ("pow(x,y)","math.pow("),
        ]:
            m.add_command(
                label=lbl,
                command=lambda c=code:
                    self._insert(c))
        m.post(self.root.winfo_pointerx(),
               self.root.winfo_pointery())

    def _toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open
        if self.sidebar_open:
            self.sidebar_frame.grid()
        else:
            self.sidebar_frame.grid_remove()

    def _keyboard(self, event):
        if self.current_view != "scientific":
            return
        k = event.char
        if k in "0123456789.+-*/()%":
            self._insert(k)
        elif event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym == "Escape":
            self._clear()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()