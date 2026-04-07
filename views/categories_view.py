from tkinter import messagebox
import customtkinter as ctk

from views.base_view import BaseTableView
import models.categorie as categorie_model


class CategoriesView(BaseTableView):

    COLUMNS = ("ID", "Nom")
    COL_WIDTHS = {"ID": 60, "Nom": 280}

    def _build_action_buttons(self, parent):
        right = ctk.CTkFrame(parent, fg_color="transparent")
        right.pack(side="right")
        ctk.CTkButton(right, text="➕ Ajouter",   width=110, command=self._add).pack(side="left", padx=3)
        ctk.CTkButton(right, text="✏️ Modifier",  width=110, command=self._update).pack(side="left", padx=3)
        ctk.CTkButton(right, text="🗑 Supprimer", width=110,
                      fg_color="#c0392b", hover_color="#922b21",
                      command=self._delete).pack(side="left", padx=3)

    def refresh(self):
        try:
            self._populate(categorie_model.get_all())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def on_search(self):
        kw = self.search_var.get().strip().lower()
        try:
            rows = [r for r in categorie_model.get_all()
                    if not kw or kw in r[1].lower()]
            self._populate(rows)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _add(self):
        _SimpleForm(self, title="Ajouter une catégorie",
                    fields=["Nom *"], on_save=self._do_create)

    def _update(self):
        v = self._selected_values()
        if not v:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une catégorie.")
            return
        _SimpleForm(self, title="Modifier la catégorie",
                    fields=["Nom *"], prefill=[v[1]],
                    on_save=lambda vals: self._do_update(v[0], vals))

    def _delete(self):
        v = self._selected_values()
        if not v:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une catégorie.")
            return
        if messagebox.askyesno("Confirmation",
                               f"Supprimer la catégorie « {v[1]} » ?\n"
                               "Les produits associés perdront leur catégorie."):
            try:
                categorie_model.delete(v[0])
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def _do_create(self, vals):
        nom = vals[0].strip()
        if not nom:
            return "⚠ Le nom est obligatoire."
        try:
            categorie_model.create(nom)
            self.refresh()
        except Exception as e:
            return f"⚠ {e}"

    def _do_update(self, cat_id, vals):
        nom = vals[0].strip()
        if not nom:
            return "⚠ Le nom est obligatoire."
        try:
            categorie_model.update(cat_id, nom)
            self.refresh()
        except Exception as e:
            return f"⚠ {e}"


# ====================================================================== #

class _SimpleForm(ctk.CTkToplevel):
    """Formulaire générique pour 1 à N champs texte."""

    def __init__(self, master, title, fields, on_save,
                 prefill=None):
        super().__init__(master)
        self.title(title)
        self.geometry("360x280")
        self.resizable(False, False)
        self.grab_set()
        self.lift()

        self._fields = fields
        self._on_save = on_save

        ctk.CTkLabel(self, text=title,
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(18, 8))

        form = ctk.CTkFrame(self)
        form.pack(fill="both", expand=True, padx=20)

        self._entries = []
        for i, label in enumerate(fields):
            ctk.CTkLabel(form, text=label, anchor="w").pack(fill="x", padx=8, pady=(8, 0))
            e = ctk.CTkEntry(form)
            e.pack(fill="x", padx=8)
            if prefill and i < len(prefill):
                e.insert(0, prefill[i])
            self._entries.append(e)

        self.error_var = ctk.StringVar()
        ctk.CTkLabel(form, textvariable=self.error_var,
                     text_color="#e74c3c",
                     font=ctk.CTkFont(size=11)).pack(pady=4)

        ctk.CTkButton(self, text="💾 Enregistrer",
                      command=self._save).pack(pady=12)

    def _save(self):
        vals = [e.get() for e in self._entries]
        result = self._on_save(vals)
        if result:                  # un message d'erreur a été retourné
            self.error_var.set(result)
        else:
            self.destroy()
