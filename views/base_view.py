import customtkinter as ctk
from tkinter import ttk
import tkinter as tk


class BaseTableView(ctk.CTkFrame):
    """
    Cadre réutilisable contenant un ttk.Treeview avec scrollbars
    et une barre de recherche + boutons d'action communs.
    """

    COLUMNS: tuple = ()
    COL_WIDTHS: dict = {}

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._sort_reverse: dict = {}
        self._build_ui()
        self.refresh()

    # ------------------------------------------------------------------ #
    #  Construction UI                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        # ── Barre du haut ──────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.on_search())

        ctk.CTkLabel(top, text="🔍 Recherche :").pack(side="left", padx=(0, 5))
        ctk.CTkEntry(top, textvariable=self.search_var, width=220).pack(side="left")

        self._build_action_buttons(top)

        # ── Treeview + scrollbars ──────────────────────────────────────
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=28,
            fieldbackground="#2b2b2b",
            borderwidth=0,
        )
        style.configure("Custom.Treeview.Heading",
                         background="#1f538d", foreground="white", relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", "#1f538d")],
                  foreground=[("selected", "white")])

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=self.COLUMNS,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
        )
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        for col in self.COLUMNS:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_column(c))
            self.tree.column(col, width=self.COL_WIDTHS.get(col, 120),
                             anchor="center")

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # ── Compteur de lignes ─────────────────────────────────────────
        self.status_var = ctk.StringVar(value="")
        ctk.CTkLabel(self, textvariable=self.status_var,
                     font=ctk.CTkFont(size=11),
                     text_color="gray").pack(anchor="e", padx=12)

    def _build_action_buttons(self, parent):
        """Surcharger pour ajouter les boutons spécifiques à droite."""
        pass

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.status_var.set(f"{len(rows)} enregistrement(s)")

    def _sort_column(self, col):
        reverse = self._sort_reverse.get(col, False)
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            data.sort(key=lambda x: float(x[0].replace(",", ".")), reverse=reverse)
        except ValueError:
            data.sort(key=lambda x: x[0].lower(), reverse=reverse)
        for i, (_, k) in enumerate(data):
            self.tree.move(k, "", i)
        self._sort_reverse[col] = not reverse
        # met à jour l'entête avec une flèche indicative
        for c in self.COLUMNS:
            label = c.replace(" ▲", "").replace(" ▼", "")
            self.tree.heading(c, text=label)
        arrow = " ▲" if not reverse else " ▼"
        self.tree.heading(col, text=col.replace(" ▲", "").replace(" ▼", "") + arrow)

    def _selected_values(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"]

    # ------------------------------------------------------------------ #
    #  À surcharger                                                        #
    # ------------------------------------------------------------------ #

    def refresh(self):
        raise NotImplementedError

    def on_search(self):
        raise NotImplementedError
