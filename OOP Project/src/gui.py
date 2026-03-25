import tkinter as tk
from tkinter import messagebox
from src.colors import MX, CAT_COLORS
from src.models import menu, Order
from src.strategies import get_discount, NoDiscount
from src.payments import CashPayment, CardPayment
class CheckoutWindow(tk.Toplevel):
    def __init__(self, parent, order, refresh_callback):
        super().__init__(parent)
        self.order = order
        self.refresh_callback = refresh_callback
        self._discount = NoDiscount()
        
        self.title("Secure Checkout")
        self.resizable(False, False)
        self.grab_set()
        self.configure(bg=MX["checkout_bg"])
        
        self._build_ui()
        self.update_idletasks()
        
        w, h = 480, 660
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    def _label(self, parent, text, size=10, bold=False, color=None):
        weight = "bold" if bold else "normal"
        fg = color or MX["text"]
        return tk.Label(parent, text=text, font=("Segoe UI", size, weight),
                        bg=MX["checkout_bg"], fg=fg)

    def _section(self, parent, title):
        f = tk.Frame(parent, bg=MX["checkout_bg"])
        f.pack(fill="x", padx=20, pady=(14, 4))
        tk.Label(f, text=title, font=("Segoe UI", 9, "bold"),
                 bg=MX["checkout_bg"], fg=MX["gold"]).pack(side="left")
        tk.Frame(f, bg=MX["gold"], height=1).pack(side="left", fill="x", expand=True, padx=(8, 0), pady=6)
        return f

    def _build_ui(self):
        bottom = tk.Frame(self, bg=MX["header2"], pady=0)
        bottom.pack(side="bottom", fill="x")
        tk.Frame(bottom, bg=MX["gold"], height=2).pack(fill="x")

        self.total_lbl = tk.Label(bottom, text=f"TOTAL:  {self.order.calculate_total():.2f} EGP",
            font=("Segoe UI", 15, "bold"), bg=MX["header2"], fg=MX["gold_lt"])
        self.total_lbl.pack(pady=(12, 6))

        tk.Button(bottom, text="\u2713  CONFIRM PAYMENT", font=("Segoe UI", 12, "bold"),
                  bg=MX["green"], fg="white", activebackground=MX["green_lt"], activeforeground="white",
                  relief="flat", pady=12, cursor="hand2", command=self._process_payment).pack(fill="x", padx=20, pady=(0, 16))

        hdr = tk.Frame(self, bg=MX["header"], pady=0)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=MX["gold"], height=3).pack(fill="x")
        tk.Label(hdr, text="\U0001F1F2\U0001F1FD  SECURE CHECKOUT", font=("Segoe UI", 13, "bold"),
                 bg=MX["header"], fg=MX["gold_lt"]).pack(side="left", padx=16, pady=10)
        tk.Frame(hdr, bg=MX["gold"], height=3).pack(fill="x", side="bottom")

        self._section(self, "ORDER SUMMARY")
        sf = tk.Frame(self, bg=MX["card"], relief="flat")
        sf.pack(fill="x", padx=20, pady=(0, 4))
        tk.Frame(sf, bg=MX["gold"], height=1).pack(fill="x")

        box = tk.Text(sf, height=5, font=("Courier New", 9), bg=MX["card"], fg=MX["text"], relief="flat", bd=0, padx=8, pady=6)
        box.pack(fill="x")
        
        counts = {}
        for item in self.order.items:
            counts[item.name] = counts.get(item.name, {"qty": 0, "price": item.price})
            counts[item.name]["qty"] += 1
            
        for name, d in counts.items():
            box.insert("end", f"  {name:<24} x{d['qty']}  {d['qty']*d['price']:>7.2f} EGP\n")
        
        box.config(state="disabled")
        tk.Frame(sf, bg=MX["gold"], height=1).pack(fill="x")

        self.subtotal_lbl = tk.Label(self, text=f"Subtotal:  {self.order.calculate_total():.2f} EGP",
            font=("Segoe UI", 10), bg=MX["checkout_bg"], fg=MX["text_dim"], anchor="e")
        self.subtotal_lbl.pack(fill="x", padx=20)

        self._section(self, "PROMO CODE")
        pf = tk.Frame(self, bg=MX["checkout_bg"])
        pf.pack(fill="x", padx=20)

        code_row = tk.Frame(pf, bg=MX["checkout_bg"])
        code_row.pack(fill="x")
        
        self.code_var = tk.StringVar()
        tk.Entry(code_row, textvariable=self.code_var, font=("Segoe UI", 11), width=18,
                 bg=MX["entry_bg"], fg=MX["text"], insertbackground=MX["gold"],
                 relief="solid", bd=1, highlightthickness=1,
                 highlightcolor=MX["gold"], highlightbackground=MX["border"]).pack(side="left", ipady=6)

        tk.Button(code_row, text="Apply", font=("Segoe UI", 10, "bold"),
                  bg=MX["header"], fg="white", activebackground=MX["gold"], activeforeground=MX["header2"],
                  relief="flat", padx=14, pady=6, cursor="hand2", command=self._apply_discount).pack(side="left", padx=(8, 0))

        tk.Label(pf, text="Codes: SAVE20  |  FLAT50  |  WELCOME", font=("Segoe UI", 8, "italic"),
                 bg=MX["checkout_bg"], fg=MX["text_dim"]).pack(anchor="w", pady=(5, 0))

        self.disc_result = tk.Label(pf, text="", font=("Segoe UI", 9, "bold"), bg=MX["checkout_bg"])
        self.disc_result.pack(anchor="w")

        self._section(self, "PAYMENT METHOD")
        pmf = tk.Frame(self, bg=MX["checkout_bg"])
        pmf.pack(fill="x", padx=20)

        self.pay_var = tk.StringVar(value="Cash")
        rb_row = tk.Frame(pmf, bg=MX["checkout_bg"])
        rb_row.pack(anchor="w")
        
        for txt, val in (("Cash Payment", "Cash"), ("Credit Card", "Card")):
            tk.Radiobutton(rb_row, text=txt, variable=self.pay_var, value=val, font=("Segoe UI", 10),
                           bg=MX["checkout_bg"], fg=MX["text"], selectcolor=MX["bg2"],
                           activebackground=MX["checkout_bg"], activeforeground=MX["gold"],
                           command=self._toggle_fields).pack(side="left", padx=(0, 20))

        self.input_container = tk.Frame(pmf, bg=MX["checkout_bg"])
        self.input_container.pack(fill="both", expand=True, pady=(8, 0))
        self._toggle_fields()

    def _entry_styled(self, parent, show=None, vcmd=None):
        kw = dict(font=("Segoe UI", 11), bg=MX["entry_bg"], fg=MX["text"],
                  insertbackground=MX["gold"], relief="solid", bd=1,
                  highlightthickness=1, highlightcolor=MX["gold"], highlightbackground=MX["border"])
        if show:  kw["show"] = show
        if vcmd:  kw["validate"] = "key"; kw["validatecommand"] = vcmd
        return tk.Entry(parent, **kw)

    def _toggle_fields(self):
        for w in self.input_container.winfo_children(): w.destroy()
        if self.pay_var.get() == "Cash":
            tk.Label(self.input_container, text="Cash Received (EGP):", font=("Segoe UI", 10),
                     bg=MX["checkout_bg"], fg=MX["text_dim"]).pack(anchor="w")
            self.entry_val = self._entry_styled(self.input_container)
            self.entry_val.pack(fill="x", ipady=6, pady=4)
        else:
            tk.Label(self.input_container, text="Card Number (16 digits):", font=("Segoe UI", 10),
                     bg=MX["checkout_bg"], fg=MX["text_dim"]).pack(anchor="w")
            
            def only_digits(P): return (P.isdigit() or P == "") and len(P) <= 16
            vcmd = (self.register(only_digits), "%P")
            
            self.entry_val = self._entry_styled(self.input_container, show="*", vcmd=vcmd)
            self.entry_val.pack(fill="x", ipady=6, pady=4)
            
            self.card_counter = tk.Label(self.input_container, text="0 / 16 digits",
                                         font=("Segoe UI", 8), bg=MX["checkout_bg"], fg=MX["text_dim"])
            self.card_counter.pack(anchor="e")
            
            def update_counter(*_):
                n = len(self.entry_val.get())
                col = MX["green"] if n == 16 else (MX["header"] if n > 0 else MX["text_dim"])
                self.card_counter.config(text=f"{n} / 16 digits", fg=col)
                
            self.entry_val.bind("<KeyRelease>", update_counter)

    def _apply_discount(self):
        self._discount = get_discount(self.code_var.get())
        code = self.code_var.get().strip().upper()
        
        if isinstance(self._discount, NoDiscount) and code:
            self.disc_result.config(text="Invalid code.", fg=MX["header"])
        elif isinstance(self._discount, NoDiscount):
            self.disc_result.config(text="", fg=MX["text"])
        else:
            saved = self.order.calculate_total() - self._discount.apply(self.order.calculate_total())
            self.disc_result.config(text=f"\u2713 Applied: {self._discount.label()} (Saved {saved:.2f} EGP)", fg=MX["green"])
                
        final = self._discount.apply(self.order.calculate_total())
        self.total_lbl.config(text=f"TOTAL:  {final:.2f} EGP")

    def _process_payment(self):
        final = self._discount.apply(self.order.calculate_total())
        val   = self.entry_val.get().strip()
        
        if self.pay_var.get() == "Cash":
            try:
                payment = CashPayment(float(val))
            except:
                messagebox.showerror("Error", "Please enter a valid cash amount.", parent=self)
                return
        else:
            if not val.isdigit() or len(val) != 16:
                messagebox.showerror("Invalid Card", f"Card number must be exactly 16 digits.\nYou entered {len(val)}.", parent=self)
                return
            payment = CardPayment(val)

        success, msg = payment.pay(final)
        if success:
            receipt = f"{msg}\n\nDiscount: {self._discount.label()}\nFinal Total: {final:.2f} EGP"
            messagebox.showinfo("Payment Successful", receipt, parent=self)
            self.order.items.clear()
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Payment Failed", msg, parent=self)


class App:
    def __init__(self, root):
        self.root  = root
        self.root.title("The Mexican Flavor  \U0001F1F2\U0001F1FD")
        self.root.configure(bg=MX["bg"])
        self.order = Order()

        self.menu_items = [
            menu("Beef Barbacoa Tacos", 110.00, "Tacos"),
            menu("Chicken Tinga Tacos", 95.00, "Tacos"),
            menu("Shrimp Al Pastor", 130.00, "Tacos"),
            menu("Crispy Fish Tacos", 120.00, "Tacos"),
            menu("Mushroom Veggie Tacos", 85.00, "Tacos"),
            menu("Steak Burrito Grande", 165.00, "Burritos"),
            menu("Chicken Fajita Burrito", 145.00, "Burritos"),
            menu("Burrito Bowl", 130.00, "Burritos"),
            menu("Chili Con Carne Bowl", 155.00, "Burritos"),
            menu("Cheese Quesadilla", 85.00, "Appetizers"),
            menu("Chicken Quesadilla", 115.00, "Appetizers"),
            menu("Beef Quesadilla", 125.00, "Appetizers"),
            menu("Nachos Supreme", 110.00, "Appetizers"),
            menu("Chips & Guacamole", 75.00, "Appetizers"),
            menu("Jalapeno Poppers", 80.00, "Appetizers"),
            menu("Beef Sizzling Fajitas",   210.00, "Mains"),
            menu("Chicken Fajitas", 185.00, "Mains"),
            menu("Cheese Enchiladas", 140.00, "Mains"),
            menu("Chicken Mole", 175.00, "Mains"),
            menu("Mexican Red Rice", 40.00, "Sides"),
            menu("Refried Beans", 35.00, "Sides"),
            menu("Elote (Corn on the Cob)", 50.00, "Sides"),
            menu("Extra Sour Cream", 15.00, "Sides"),
            menu("Churros con Chocolate", 65.00, "Desserts"),
            menu("Tres Leches Cake", 90.00, "Desserts"),
            menu("Caramel Flan", 60.00, "Desserts"),
            menu("Fried Ice Cream", 75.00, "Desserts"),
            menu("Classic Horchata", 50.00, "Drinks"),
            menu("Jarritos Soda", 45.00, "Drinks"),
            menu("Fresh Hibiscus Water", 40.00, "Drinks"),
            menu("Virgin Margarita", 65.00, "Drinks"),
            menu("Mineral Water", 20.00, "Drinks"),
        ]

        self._setup_ui()
        w, h = 1150, 740
        self.root.geometry(f"{w}x{h}+{(self.root.winfo_screenwidth()-w)//2}+{(self.root.winfo_screenheight()-h)//2}")

    def _setup_ui(self):
        self._build_header()
        body = tk.Frame(self.root, bg=MX["bg"])
        body.pack(fill="both", expand=True)
        self._build_menu_panel(body)
        self._build_cart_panel(body)

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=MX["header"])
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=MX["gold"], height=4).pack(fill="x")
        inner = tk.Frame(hdr, bg=MX["header"])
        inner.pack(fill="x", padx=16, pady=10)
        tk.Label(inner, text="\U0001F1F2\U0001F1FD  THE MEXICAN FLAVOR", font=("Segoe UI", 17, "bold"), bg=MX["header"], fg=MX["gold_lt"]).pack(side="left")
        tk.Frame(hdr, bg=MX["gold"], height=4).pack(fill="x")

    def _build_menu_panel(self, parent):
        left = tk.Frame(parent, bg=MX["bg"])
        left.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        sh = tk.Frame(left, bg=MX["bg"]); sh.pack(fill="x", pady=(0, 8))
        tk.Label(sh, text="MENU", font=("Segoe UI", 13, "bold"), bg=MX["bg"], fg=MX["gold"]).pack(side="left")
        
        canvas = tk.Canvas(left, bg=MX["bg"], highlightthickness=0)
        sb     = tk.Scrollbar(left, orient="vertical", command=canvas.yview)
        sf     = tk.Frame(canvas, bg=MX["bg"])
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        categories = {}
        for item in self.menu_items:
            categories.setdefault(item.category, []).append(item)

        for cat, items in categories.items():
            cat_color = CAT_COLORS.get(cat, "#888")
            rf = tk.Frame(sf, bg=MX["bg"]); rf.pack(fill="x", pady=(10, 4))
            tk.Label(rf, text=f"  {cat.upper()}  ", font=("Segoe UI", 8, "bold"), bg=cat_color, fg="white", padx=6, pady=3).pack(side="left")

            grid = tk.Frame(sf, bg=MX["bg"]); grid.pack(fill="x", pady=(0, 4))
            for idx, item in enumerate(items):
                self._make_card(grid, item, idx // 4, idx % 4)

    def _make_card(self, parent, item, row, col):
        cat_color = CAT_COLORS.get(item.category, "#888")
        card = tk.Frame(parent, bg=MX["card"], cursor="hand2", highlightbackground=MX["border"], highlightthickness=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        tk.Frame(card, bg=cat_color, height=4).pack(fill="x")
        tk.Label(card, text=item.name, font=("Segoe UI", 9, "bold"), bg=MX["card"], fg=MX["text"], wraplength=118).pack(pady=(8, 2), padx=6)
        tk.Label(card, text=f"{item.price:.2f} EGP", font=("Segoe UI", 9), bg=MX["card"], fg=MX["gold"]).pack(pady=(0, 8))

        def click(e, i=item): self._add_item(i)
        card.bind("<Button-1>", click)
        for w in card.winfo_children(): w.bind("<Button-1>", click)

    def _build_cart_panel(self, parent):
        right = tk.Frame(parent, bg=MX["sidebar"], width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="\U0001F6D2  YOUR ORDER", font=("Segoe UI", 12, "bold"), bg=MX["sidebar"], fg=MX["gold"]).pack(pady=(12, 4))
        
        lo = tk.Frame(right, bg=MX["sidebar"])
        lo.pack(fill="both", expand=True, padx=8, pady=6)
        
        self.cart_listbox = tk.Listbox(lo, font=("Courier New", 9), bg=MX["sidebar"], fg=MX["text"], relief="flat", bd=0, highlightthickness=0)
        self.cart_listbox.pack(side="left", fill="both", expand=True)

        footer = tk.Frame(right, bg=MX["bg2"])
        footer.pack(fill="x", side="bottom")

        self.lbl_total = tk.Label(footer, text="TOTAL:  0.00 EGP", font=("Segoe UI", 14, "bold"), bg=MX["bg2"], fg=MX["gold_lt"])
        self.lbl_total.pack(pady=(10, 6))

        tk.Button(footer, text="\U0001F4B3  PROCEED TO CHECKOUT", font=("Segoe UI", 11, "bold"), bg=MX["green"], fg=MX["gold_lt"],
                  relief="flat", pady=12, cursor="hand2", command=self._open_checkout).pack(fill="x", padx=16, pady=(0, 16))

    def _add_item(self, item):
        self.order.add_item(item)
        self._refresh_cart()

    def _refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)
        if not self.order.items:
            self.cart_listbox.insert(tk.END, "  Cart is empty...")
            self.lbl_total.config(text="TOTAL:  0.00 EGP")
            return
        counts = {}
        for item in self.order.items:
            if item.name not in counts:
                counts[item.name] = {"qty": 0, "price": item.price}
            counts[item.name]["qty"] += 1
        for name, data in counts.items():
            qty = data["qty"]
            total_price = qty * data["price"]
            line = f"  {name[:20]:<20}  x{qty}  {total_price:.2f}"
            self.cart_listbox.insert(tk.END, line)
        self.lbl_total.config(text=f"TOTAL:  {self.order.calculate_total():.2f} EGP")

    def _open_checkout(self):
        if self.order.item_count() == 0:
            messagebox.showwarning("Empty Cart", "Please add items before proceeding to payment.")
            return
        CheckoutWindow(self.root, self.order, self._refresh_cart)