from tkinter import messagebox
import customtkinter as ctk

from views.base_view import BaseTableView
import models.fournisseur as fournisseur_model
from views.categories_view import _SimpleForm


class FournisseursView(BaseTableView):

    COLUMNS = ("ID", "Nom", "Contact")
    COL_WIDTHS = {"ID": 60, "Nom": 200, "Contact": 200}

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
            self._populate(fournisseur_model.get_all())
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def on_search(self):
        kw = self.search_var.get().strip().lower()
        try:
            rows = [r for r in fournisseur_model.get_all()
                    if not kw or kw in r[1].lower() or kw in (r[2] or "").lower()]
            self._populate(rows)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _add(self):
        _SimpleForm(self, title="Ajouter un fournisseur",
                    fields=["Nom *", "Contact"],
                    on_save=self._do_create)

    def _update(self):
        v = self._selected_values()
        if not v:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un fournisseur.")
            return
        _SimpleForm(self, title="Modifier le fournisseur",
                    fields=["Nom *", "Contact"],
                    prefill=[v[1], v[2]],
                    on_save=lambda vals: self._do_update(v[0], vals))

    def _delete(self):
        v = self._selected_values()
        if not v:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un fournisseur.")
            return
        if messagebox.askyesno("Confirmation",
                               f"Supprimer le fournisseur « {v[1]} » ?\n"
                               "Les produits associés perdront leur fournisseur."):
            try:
                fournisseur_model.delete(v[0])
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def _do_create(self, vals):
        nom, contact = vals[0].strip(), vals[1].strip() if len(vals) > 1 else ""
        if not nom:
            return "⚠ Le nom est obligatoire."
        try:
            fournisseur_model.create(nom, contact)
            self.refresh()
        except Exception as e:
            return f"⚠ {e}"

    def _do_update(self, f_id, vals):
        nom, contact = vals[0].strip(), vals[1].strip() if len(vals) > 1 else ""
        if not nom:
            return "⚠ Le nom est obligatoire."
        try:
            fournisseur_model.update(f_id, nom, contact)
            self.refresh()
        except Exception as e:
            return f"⚠ {e}"
