import csv
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk

from views.base_view import BaseTableView
import models.produit as produit_model
import models.categorie as categorie_model
import models.fournisseur as fournisseur_model


class ProduitsView(BaseTableView):

    COLUMNS = ("ID", "Nom", "Prix (€)", "Quantité", "Catégorie", "Fournisseur")
    COL_WIDTHS = {
        "ID": 50, "Nom": 180, "Prix (€)": 90,
        "Quantité": 90, "Catégorie": 130, "Fournisseur": 130
    }

    # ------------------------------------------------------------------ #
    #  Boutons d'action                                                    #
    # ------------------------------------------------------------------ #

    def _build_action_buttons(self, parent):
        right = ctk.CTkFrame(parent, fg_color="transparent")
        right.pack(side="right")

        ctk.CTkButton(right, text="➕ Ajouter",   width=110,
                      command=self._add).pack(side="left", padx=3)
        ctk.CTkButton(right, text="✏️ Modifier",  width=110,
                      command=self._update).pack(side="left", padx=3)
        ctk.CTkButton(right, text="🗑 Supprimer", width=110,
                      fg_color="#c0392b", hover_color="#922b21",
                      command=self._delete).pack(side="left", padx=3)
        ctk.CTkButton(right, text="📊 Statistiques", width=120,
                      command=self._stats).pack(side="left", padx=3)
        ctk.CTkButton(right, text="📥 Export CSV",   width=120,
                      command=self._export_csv).pack(side="left", padx=3)

    # ------------------------------------------------------------------ #
    #  Données                                                             #
    # ------------------------------------------------------------------ #

    def refresh(self):
        try:
            rows = produit_model.get_all()
            self._populate(rows)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def on_search(self):
        keyword = self.search_var.get().strip()
        try:
            rows = produit_model.search(keyword) if keyword else produit_model.get_all()
            self._populate(rows)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ------------------------------------------------------------------ #
    #  CRUD                                                                #
    # ------------------------------------------------------------------ #

    def _add(self):
        ProductForm(self, title="Ajouter un produit", on_save=self.refresh)

    def _update(self):
        values = self._selected_values()
        if not values:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un produit.")
            return
        ProductForm(self, title="Modifier le produit",
                    data=values, on_save=self.refresh)

    def _delete(self):
        values = self._selected_values()
        if not values:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un produit.")
            return
        if messagebox.askyesno("Confirmation",
                               f"Supprimer le produit « {values[1]} » ?\nCette action est irréversible."):
            try:
                produit_model.delete(values[0])
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def _stats(self):
        try:
            count, total, avg = produit_model.get_stats()
            messagebox.showinfo(
                "Statistiques Produits",
                f"Nombre de produits    : {count}\n"
                f"Valeur totale du stock : {total:,.2f} €\n"
                f"Prix moyen            : {avg:,.2f} €"
            )
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _export_csv(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="produits_export"
        )
        if not file:
            return
        try:
            with open(file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(self.COLUMNS)
                for row_id in self.tree.get_children():
                    writer.writerow(self.tree.item(row_id)["values"])
            messagebox.showinfo("Export réussi", f"Fichier enregistré :\n{file}")
        except Exception as e:
            messagebox.showerror("Erreur export", str(e))


# ====================================================================== #
#  Formulaire Produit                                                     #
# ====================================================================== #

class ProductForm(ctk.CTkToplevel):

    def __init__(self, master, title: str, on_save,
                 data: tuple | None = None):
        super().__init__(master)
        self.title(title)
        self.geometry("420x480")
        self.resizable(False, False)
        self.grab_set()          # modal
        self.lift()

        self._data = data
        self._on_save = on_save
        self._cats = categorie_model.get_all()    # [(id, nom), ...]
        self._fours = fournisseur_model.get_all()  # [(id, nom, contact), ...]

        self._build()

    def _build(self):
        ctk.CTkLabel(self, text=self.title(),
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        form = ctk.CTkFrame(self)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        def row(label, widget_fn, **kw):
            ctk.CTkLabel(form, text=label, anchor="w").pack(fill="x", padx=10, pady=(8, 0))
            w = widget_fn(form, **kw)
            w.pack(fill="x", padx=10)
            return w

        self.entry_nom  = row("Nom du produit *", ctk.CTkEntry, placeholder_text="Ex : Laptop Dell")
        self.entry_prix = row("Prix (€) *",       ctk.CTkEntry, placeholder_text="Ex : 999.99")
        self.entry_qte  = row("Quantité *",        ctk.CTkEntry, placeholder_text="Ex : 10")

        # Catégorie dropdown
        cat_names = ["— aucune —"] + [c[1] for c in self._cats]
        ctk.CTkLabel(form, text="Catégorie", anchor="w").pack(fill="x", padx=10, pady=(8, 0))
        self.combo_cat = ctk.CTkComboBox(form, values=cat_names, state="readonly")
        self.combo_cat.set(cat_names[0])
        self.combo_cat.pack(fill="x", padx=10)

        # Fournisseur dropdown
        four_names = ["— aucun —"] + [f[1] for f in self._fours]
        ctk.CTkLabel(form, text="Fournisseur", anchor="w").pack(fill="x", padx=10, pady=(8, 0))
        self.combo_four = ctk.CTkComboBox(form, values=four_names, state="readonly")
        self.combo_four.set(four_names[0])
        self.combo_four.pack(fill="x", padx=10)

        # Pré-remplissage en mode édition
        if self._data:
            self.entry_nom.insert(0, self._data[1])
            self.entry_prix.insert(0, self._data[2])
            self.entry_qte.insert(0, self._data[3])
            # Catégorie
            cat_val = self._data[4]
            if cat_val in cat_names:
                self.combo_cat.set(cat_val)
            # Fournisseur
            four_val = self._data[5]
            if four_val in four_names:
                self.combo_four.set(four_val)

        # Label erreur
        self.error_var = ctk.StringVar()
        ctk.CTkLabel(form, textvariable=self.error_var,
                     text_color="#e74c3c",
                     font=ctk.CTkFont(size=11)).pack(pady=(6, 0))

        # Bouton enregistrer
        ctk.CTkButton(self, text="💾 Enregistrer",
                      command=self._save).pack(pady=15)

    # ------------------------------------------------------------------ #

    def _save(self):
        nom  = self.entry_nom.get().strip()
        prix_str = self.entry_prix.get().strip()
        qte_str  = self.entry_qte.get().strip()

        # Validation
        if not nom:
            self.error_var.set("⚠ Le nom est obligatoire.")
            return
        try:
            prix = float(prix_str)
            if prix < 0:
                raise ValueError
        except ValueError:
            self.error_var.set("⚠ Le prix doit être un nombre positif.")
            return
        try:
            qte = int(qte_str)
            if qte < 0:
                raise ValueError
        except ValueError:
            self.error_var.set("⚠ La quantité doit être un entier positif.")
            return

        # Résolution IDs catégorie / fournisseur
        cat_sel  = self.combo_cat.get()
        four_sel = self.combo_four.get()
        cat_id  = next((c[0] for c in self._cats  if c[1] == cat_sel),  None)
        four_id = next((f[0] for f in self._fours if f[1] == four_sel), None)

        try:
            if self._data:
                produit_model.update(self._data[0], nom, prix, qte, cat_id, four_id)
            else:
                produit_model.create(nom, prix, qte, cat_id, four_id)
            self._on_save()
            self.destroy()
        except Exception as e:
            self.error_var.set(f"⚠ {e}")
