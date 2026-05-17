import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth_ok import * 

def executar_login():
    u, p = entry_user.get(), entry_pass.get()
    usuari_valid = login_user_db(u, p)
    if usuari_valid:
        messagebox.showinfo("Login Correcte", f"Benvingut/da, {usuari_valid[1]}")
        ventana_login.destroy()
        obrir_interfaz_principal()
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

def obrir_interfaz_principal():
    root = tk.Tk()
    root.title("UA Hospital Blanes - Sistema de Gestió")
    root.geometry("600x750")
    root.configure(bg="#f0f4f7")

    header = tk.Frame(root, bg="#2c3e50", height=80)
    header.pack(fill="x")
    tk.Label(header, text="🏥 GESTIÓ HOSPITALÀRIA", font=("Segoe UI", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=20)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=20, pady=20)

    # --- PESTANYA GESTIÓ ---
    f_gestio = tk.Frame(notebook, bg="white")
    notebook.add(f_gestio, text=" ⚙️ Gestió ")

    def ui_alta_personal():
        dialeg = tk.Toplevel(root); dialeg.title("Alta Personal"); dialeg.geometry("400x600"); dialeg.grab_set()
        fields = ["DNI", "Nom", "Primer Cognom", "Email", "Usuari", "Contrasenya"]
        entries = {}
        for f in fields:
            tk.Label(dialeg, text=f).pack(pady=2)
            e = tk.Entry(dialeg, show="*" if f == "Contrasenya" else ""); e.pack(pady=5); entries[f] = e
        
        combo_rol = ttk.Combobox(dialeg, values=["metge", "infermer", "vario"], state="readonly")
        combo_rol.current(0); combo_rol.pack(pady=10)

        def guardar_p():
            if register_personal_db(entries["DNI"].get(), entries["Nom"].get(), entries["Primer Cognom"].get(), "", 
                                    entries["Email"].get(), entries["Usuari"].get(), entries["Contrasenya"].get(), combo_rol.get()):
                messagebox.showinfo("Èxit", "Personal registrat."); dialeg.destroy()
            else: messagebox.showerror("Error", "Dades incorrectes.")
        tk.Button(dialeg, text="GUARDAR", command=guardar_p, bg="#27ae60", fg="white", pady=10).pack(fill="x", padx=50)

    def ui_alta_pacient():
        dialeg = tk.Toplevel(root); dialeg.title("Alta Pacient"); dialeg.geometry("400x550"); dialeg.grab_set()
        fields = [("Targeta Sanitària", "ts"), ("Nom", "nom"), ("Primer Cognom", "c1"), ("Segon Cognom", "c2"), ("Data (AAAA-MM-DD)", "data")]
        entries = {}
        for label, key in fields:
            tk.Label(dialeg, text=label).pack(pady=2)
            e = tk.Entry(dialeg); e.pack(pady=5, ipady=3); entries[key] = e

        def validar_i_executar_alta():
            # Crida a la funció de auth_ok.py (evitem conflicte de noms)
            exit = insertar_pacient_db(entries["ts"].get(), entries["nom"].get(), entries["c1"].get(), entries["c2"].get(), entries["data"].get())
            if exit:
                messagebox.showinfo("Èxit", "Pacient d'alta."); dialeg.destroy()
            else: messagebox.showerror("Error", "Error al registre.")

        tk.Button(dialeg, text="REGISTRAR PACIENT", command=validar_i_executar_alta, bg="#34495e", fg="white", pady=10).pack(fill="x", padx=50, pady=20)

    tk.Button(f_gestio, text="➕ REGISTRAR NOU PERSONAL", command=ui_alta_personal, bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), pady=12, width=35).pack(pady=20)
    tk.Button(f_gestio, text="📋 DONAR D'ALTA PACIENT", command=ui_alta_pacient, bg="#2c3e50", fg="white", font=("Segoe UI", 10, "bold"), pady=12, width=35).pack(pady=10)

    # --- PESTANYA INFORMES ---
    f_inf = tk.Frame(notebook, bg="white")
    notebook.add(f_inf, text=" 📊 Informes ")

    def mostrar_cens():
        dades = get_informe_personal_db()
        txt = "LLISTAT DE PERSONAL:\n" + "-"*30 + "\n"
        for d in dades: txt += f"• {d[1]} {d[2]}\n  DNI: {d[0]} | Email: {d[3]}\n\n"
        messagebox.showinfo("Cens", txt)

    def mostrar_visites():
        dades = get_visites_per_dia_db()
        txt = "VISITES PER DIA:\n" + "-"*30 + "\n"
        for d in dades: txt += f"Data: {d[0]} --> {d[1]} visites\n"
        messagebox.showinfo("Visites", txt)

    def ui_planta():
        p = simpledialog.askinteger("Planta", "Número de planta:")
        if p is not None:
            r = get_recursos_planta_db(p)
            messagebox.showinfo("Recursos", f"PLANTA {p}:\nHabitacions: {r['h']}\nQuiròfans: {r['q']}\nInfermeria: {r['i']}")

    def mostrar_rank():
        dades = get_ranking_metges_db()
        txt = "RANKING METGES:\n" + "-"*30 + "\n"
        for i, d in enumerate(dades, 1): txt += f"{i}. {d[0]} {d[1]}: {d[2]} visites\n"
        messagebox.showinfo("Ranking", txt)

    opts = [("🔍 Recursos per Planta", ui_planta), ("👥 Informe de Personal (Cens)", mostrar_cens), ("📅 Visites per Dia", mostrar_visites), ("🏆 Rànquing Metges", mostrar_rank)]
    for t, c in opts:
        tk.Button(f_inf, text=t, command=c, bg="white", fg="#2c3e50", relief="flat", highlightthickness=1, pady=10, width=40).pack(pady=5)

    root.mainloop()

# --- LOGIN ---
ventana_login = tk.Tk()
ventana_login.title("UA Hospital")
ventana_login.geometry("400x550")
ventana_login.configure(bg="#2c3e50")

tk.Label(ventana_login, text="🏥 UA-HOSPITAL", font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="white").pack(pady=50)
entry_user = tk.Entry(ventana_login, font=("Segoe UI", 12), justify='center'); entry_user.pack(pady=10, ipady=5)
entry_pass = tk.Entry(ventana_login, font=("Segoe UI", 12), justify='center', show="*"); entry_pass.pack(pady=10, ipady=5)
tk.Button(ventana_login, text="ACCEDIR", command=executar_login, bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), pady=12, width=20).pack(pady=40)

ventana_login.mainloop()
