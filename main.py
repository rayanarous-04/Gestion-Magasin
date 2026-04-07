import customtkinter as ctk
from config import APP_TITLE, APP_GEOMETRY, APP_MIN_SIZE, THEME, COLOR_THEME

from views.produits_view import ProduitsView
from views.categories_view import CategoriesView
from views.fournisseurs_view import FournisseursView

ctk.set_appearance_mode(THEME)
ctk.set_default_color_theme(COLOR_THEME)


class MainApp(ctk.CTk):

    PAGES = {
        "🛒  Produits":      ProduitsView,
        "🏷  Catégories":    CategoriesView,
        "🚚  Fournisseurs":  FournisseursView,
    }

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(*APP_MIN_SIZE)

        self._active_btn: ctk.CTkButton | None = None
        self._current_frame: ctk.CTkFrame | None = None

        self._build_layout()
        # Affiche la première page par défaut
        first_name = next(iter(self.PAGES))
        self._show_page(first_name)

    # ------------------------------------------------------------------ #

    def _build_layout(self):
        # ── Sidebar ────────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / titre
        ctk.CTkLabel(
            self.sidebar,
            text="🏪 Magasin Pro",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 20))

        ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        ).pack(anchor="w", padx=18, pady=(0, 4))

        # Boutons de navigation
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        for name in self.PAGES:
            btn = ctk.CTkButton(
                self.sidebar,
                text=name,
                anchor="w",
                height=40,
                fg_color="transparent",
                hover_color=("gray80", "gray25"),
                text_color=("gray10", "gray90"),
                corner_radius=6,
                command=lambda n=name: self._show_page(n),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_buttons[name] = btn

        # Séparateur + bas de sidebar
        ctk.CTkLabel(self.sidebar, text="").pack(expand=True)
        ctk.CTkLabel(
            self.sidebar,
            text="Projet Semestriel · 2024",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        ).pack(pady=10)

        # ── Zone de contenu principale ─────────────────────────────────
        self.content_area = ctk.CTkFrame(self, corner_radius=0,
                                         fg_color=("gray95", "gray10"))
        self.content_area.pack(side="left", fill="both", expand=True)

    # ------------------------------------------------------------------ #

    def _show_page(self, name: str):
        # Mise à jour visuelle du bouton actif
        if self._active_btn:
            self._active_btn.configure(fg_color="transparent")
        self._active_btn = self._nav_buttons[name]
        self._active_btn.configure(fg_color=("gray75", "gray30"))

        # Destruction de la vue précédente
        if self._current_frame:
            self._current_frame.destroy()

        # Instanciation de la nouvelle vue
        view_class = self.PAGES[name]
        self._current_frame = view_class(self.content_area)
        self._current_frame.pack(fill="both", expand=True)


# ====================================================================== #

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
