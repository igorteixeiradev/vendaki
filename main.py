import tkinter as tk
from tkinter import messagebox, ttk

from db.database import Database
from src.Categoria import Categoria
from src.Cliente import Cliente
from src.Produto import Produto
from src.Venda import Venda


class SistemaVendasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vendaki - Sistema de Vendas")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        self.COR_PRIMARIA   = "#2C3E50"
        self.COR_SECUNDARIA = "#2980B9"
        self.COR_SUCESSO    = "#27AE60"
        self.COR_ALERTA     = "#E67E22"
        self.COR_PERIGO     = "#C0392B"
        self.COR_FUNDO      = "#F0F2F5"
        self.COR_BRANCO     = "#FFFFFF"
        self.COR_TEXTO      = "#2C3E50"
        self.COR_CINZA      = "#BDC3C7"
        self.COR_CINZA_ESC  = "#7F8C8D"

        self.root.configure(bg=self.COR_FUNDO)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame",           background=self.COR_FUNDO)
        self.style.configure("TLabel",           background=self.COR_FUNDO, foreground=self.COR_TEXTO)
        self.style.configure("Treeview",         rowheight=26, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.COR_PRIMARIA, foreground=self.COR_BRANCO)
        self.style.map("Treeview", background=[("selected", self.COR_SECUNDARIA)])

        self.db   = Database()
        self.conn = self.db.conectar()
        if self.conn:
            self.db.criar_tabelas()
            self.db.inserir_dados_iniciais()

        self.criar_menu_principal()

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def barra_topo(self, titulo, subtitulo=""):
        barra = tk.Frame(self.root, bg=self.COR_PRIMARIA, height=55)
        barra.pack(fill=tk.X)
        barra.pack_propagate(False)
        tk.Label(barra, text="VENDAKI", font=("Segoe UI", 12, "bold"),
                 bg=self.COR_PRIMARIA, fg=self.COR_CINZA).pack(side=tk.LEFT, padx=18, pady=15)
        tk.Label(barra, text="|", font=("Segoe UI", 14),
                 bg=self.COR_PRIMARIA, fg=self.COR_CINZA_ESC).pack(side=tk.LEFT)
        tk.Label(barra, text=titulo, font=("Segoe UI", 14, "bold"),
                 bg=self.COR_PRIMARIA, fg=self.COR_BRANCO).pack(side=tk.LEFT, padx=12)
        if subtitulo:
            tk.Label(barra, text=subtitulo, font=("Segoe UI", 10),
                     bg=self.COR_PRIMARIA, fg=self.COR_CINZA).pack(side=tk.LEFT)

    def btn(self, parent, texto, comando, cor=None, lado=tk.LEFT, padx=5, pady=0):
        cor = cor or self.COR_SECUNDARIA
        b = tk.Button(parent, text=texto, command=comando,
                      bg=cor, fg=self.COR_BRANCO,
                      font=("Segoe UI", 10, "bold"),
                      relief=tk.FLAT, padx=14, pady=7,
                      cursor="hand2", activebackground=cor,
                      activeforeground=self.COR_BRANCO)
        b.pack(side=lado, padx=padx, pady=pady)
        return b

    def campo(self, parent, label, row, default="", largura=35):
        tk.Label(parent, text=label, font=("Segoe UI", 10),
                 bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC,
                 anchor=tk.W).grid(row=row, column=0, sticky=tk.W, pady=(10, 2))
        entry = tk.Entry(parent, font=("Segoe UI", 11), width=largura,
                         relief=tk.FLAT, bg="#EEF2F5", bd=0,
                         highlightthickness=1, highlightbackground=self.COR_CINZA,
                         highlightcolor=self.COR_SECUNDARIA)
        entry.grid(row=row, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        if default:
            entry.insert(0, str(default))
        return entry

    def campo_combo(self, parent, label, row, valores, largura=33):
        tk.Label(parent, text=label, font=("Segoe UI", 10),
                 bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC,
                 anchor=tk.W).grid(row=row, column=0, sticky=tk.W, pady=(10, 2))
        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var, values=valores,
                             width=largura, font=("Segoe UI", 10), state="readonly")
        combo.grid(row=row, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        return combo, var

    def card(self, parent, titulo, valor, cor):
        c = tk.Frame(parent, bg=cor, padx=18, pady=12)
        c.pack(side=tk.LEFT, padx=6, pady=6, fill=tk.BOTH, expand=True)
        tk.Label(c, text=titulo, font=("Segoe UI", 9),
                 bg=cor, fg=self.COR_BRANCO).pack(anchor=tk.W)
        tk.Label(c, text=str(valor), font=("Segoe UI", 18, "bold"),
                 bg=cor, fg=self.COR_BRANCO).pack(anchor=tk.W)

    def tabela(self, parent, colunas, dados, larguras=None):
        frame = tk.Frame(parent, bg=self.COR_FUNDO)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        sy = ttk.Scrollbar(frame)
        sy.pack(side=tk.RIGHT, fill=tk.Y)
        sx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        sx.pack(side=tk.BOTTOM, fill=tk.X)

        tree = ttk.Treeview(frame, columns=colunas, show="headings",
                            yscrollcommand=sy.set, xscrollcommand=sx.set)
        tree.pack(fill=tk.BOTH, expand=True)
        sy.config(command=tree.yview)
        sx.config(command=tree.xview)

        for i, col in enumerate(colunas):
            tree.heading(col, text=col)
            w = (larguras[i] if larguras and i < len(larguras) else 120)
            tree.column(col, width=w, anchor=tk.CENTER)

        for row in dados:
            tree.insert("", tk.END, values=row)

        return tree

    def painel_form(self, titulo):
        """Cria um painel de formulario centralizado com fundo branco."""
        outer = tk.Frame(self.root, bg=self.COR_FUNDO)
        outer.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        card = tk.Frame(outer, bg=self.COR_BRANCO, padx=35, pady=30,
                        relief=tk.FLAT, bd=0,
                        highlightthickness=1, highlightbackground=self.COR_CINZA)
        card.pack(fill=tk.BOTH, expand=False)

        tk.Label(card, text=titulo, font=("Segoe UI", 15, "bold"),
                 bg=self.COR_BRANCO, fg=self.COR_TEXTO).grid(
                 row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        sep = tk.Frame(card, bg=self.COR_CINZA, height=1)
        sep.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 8))

        return card

    def criar_menu_principal(self):
        self.limpar()

      
        topo = tk.Frame(self.root, bg=self.COR_PRIMARIA)
        topo.pack(fill=tk.X)
        tk.Label(topo, text="VENDAKI", font=("Segoe UI", 22, "bold"),
                 bg=self.COR_PRIMARIA, fg=self.COR_BRANCO).pack(side=tk.LEFT, padx=20, pady=14)
        tk.Label(topo, text="Sistema de Vendas", font=("Segoe UI", 11),
                 bg=self.COR_PRIMARIA, fg=self.COR_CINZA).pack(side=tk.LEFT, pady=14)

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=14)

       
        tk.Label(main, text="Resumo", font=("Segoe UI", 12, "bold"),
                 bg=self.COR_FUNDO, fg=self.COR_TEXTO).pack(anchor=tk.W)

        cards_frame = tk.Frame(main, bg=self.COR_FUNDO)
        cards_frame.pack(fill=tk.X, pady=(4, 14))

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        n_clientes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM produtos")
        n_produtos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE Stock <= 5")
        n_stock_baixo = cursor.fetchone()[0]

        self.card(cards_frame, "Total de Vendas",  f"{Venda.total_vendas(self.conn):,.2f} KZ", self.COR_SECUNDARIA)
        self.card(cards_frame, "Vendas Hoje",       f"{Venda.total_hoje(self.conn):,.2f} KZ",   self.COR_SUCESSO)
        self.card(cards_frame, "Nr de Transacções", str(Venda.contagem_vendas(self.conn)),       self.COR_PRIMARIA)
        self.card(cards_frame, "Clientes",          str(n_clientes),                             "#8E44AD")
        self.card(cards_frame, "Produtos",          str(n_produtos),                             "#16A085")
        if n_stock_baixo > 0:
            self.card(cards_frame, "Stock Baixo", f"{n_stock_baixo} produto(s)", self.COR_PERIGO)

        paineis = tk.Frame(main, bg=self.COR_FUNDO)
        paineis.pack(fill=tk.X, pady=(0, 14))

      
        p_left = tk.Frame(paineis, bg=self.COR_BRANCO, padx=14, pady=12,
                          highlightthickness=1, highlightbackground=self.COR_CINZA)
        p_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        tk.Label(p_left, text="Top Produtos Vendidos", font=("Segoe UI", 11, "bold"),
                 bg=self.COR_BRANCO, fg=self.COR_TEXTO).pack(anchor=tk.W, pady=(0, 6))
        top_prods = Venda.vendas_por_produto(self.conn)[:5]
        if top_prods:
            for i, (nome, qt, valor) in enumerate(top_prods, 1):
                r = tk.Frame(p_left, bg=self.COR_BRANCO)
                r.pack(fill=tk.X, pady=1)
                tk.Label(r, text=f"{i}. {nome}", font=("Segoe UI", 9),
                         bg=self.COR_BRANCO, fg=self.COR_TEXTO, anchor=tk.W).pack(side=tk.LEFT)
                tk.Label(r, text=f"{valor:,.0f} KZ  ({qt} un.)", font=("Segoe UI", 9),
                         bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC).pack(side=tk.RIGHT)
        else:
            tk.Label(p_left, text="Sem vendas ainda.", font=("Segoe UI", 9),
                     bg=self.COR_BRANCO, fg=self.COR_CINZA).pack()

    
        p_right = tk.Frame(paineis, bg=self.COR_BRANCO, padx=14, pady=12,
                           highlightthickness=1, highlightbackground=self.COR_CINZA)
        p_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(p_right, text="Stock Baixo (5 ou menos)", font=("Segoe UI", 11, "bold"),
                 bg=self.COR_BRANCO, fg=self.COR_TEXTO).pack(anchor=tk.W, pady=(0, 6))
        cursor.execute("SELECT Nome, Stock FROM produtos WHERE Stock <= 5 ORDER BY Stock ASC LIMIT 6")
        baixo = cursor.fetchall()
        if baixo:
            for nome, stock in baixo:
                r = tk.Frame(p_right, bg=self.COR_BRANCO)
                r.pack(fill=tk.X, pady=1)
                tk.Label(r, text=nome, font=("Segoe UI", 9),
                         bg=self.COR_BRANCO, fg=self.COR_TEXTO, anchor=tk.W).pack(side=tk.LEFT)
                cor_s = self.COR_PERIGO if stock == 0 else self.COR_ALERTA
                tk.Label(r, text="Esgotado" if stock == 0 else f"{stock} un.",
                         font=("Segoe UI", 9, "bold"), bg=self.COR_BRANCO, fg=cor_s).pack(side=tk.RIGHT)
        else:
            tk.Label(p_right, text="Todos os produtos com stock OK.", font=("Segoe UI", 9),
                     bg=self.COR_BRANCO, fg=self.COR_SUCESSO).pack()

     
        tk.Label(main, text="Menu Principal", font=("Segoe UI", 12, "bold"),
                 bg=self.COR_FUNDO, fg=self.COR_TEXTO).pack(anchor=tk.W, pady=(6, 4))

        nav = tk.Frame(main, bg=self.COR_FUNDO)
        nav.pack(fill=tk.X)

        botoes = [
            ("Categorias",      self.menu_categorias,   self.COR_PRIMARIA),
            ("Produtos",        self.menu_produtos,      "#16A085"),
            ("Clientes",        self.menu_clientes,      "#8E44AD"),
            ("Realizar Venda",  self.realizar_venda,     self.COR_SUCESSO),
            ("Historico Vendas",self.visualizar_vendas,  self.COR_SECUNDARIA),
            ("Relatorios",      self.menu_relatorios,    self.COR_ALERTA),
            ("Sair",            self.fechar_sistema,     self.COR_PERIGO),
        ]
        for texto, cmd, cor in botoes:
            tk.Button(nav, text=texto, command=cmd,
                      bg=cor, fg=self.COR_BRANCO,
                      font=("Segoe UI", 10, "bold"),
                      relief=tk.FLAT, padx=12, pady=8,
                      cursor="hand2", width=15).pack(side=tk.LEFT, padx=4)


    def menu_categorias(self):
        self.limpar()
        self.barra_topo("CATEGORIAS")

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        barra = tk.Frame(main, bg=self.COR_FUNDO)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar",    self.criar_menu_principal, self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_categoria, self.COR_SUCESSO)

        dados = Categoria.listar_todos(self.conn)
        self.cat_tree = self.tabela(main, ["ID", "Nome"], dados, [60, 350])

        barra2 = tk.Frame(main, bg=self.COR_FUNDO)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(barra2, "Editar Selecionado", lambda: self.tela_editar_categoria(), self.COR_SECUNDARIA)
        self.btn(barra2, "Apagar Selecionado", lambda: self.apagar_categoria(),      self.COR_PERIGO)

    def tela_cadastrar_categoria(self):
        self.limpar()
        self.barra_topo("NOVA CATEGORIA")
        card = self.painel_form("Cadastrar Categoria")

        entry_nome = self.campo(card, "Nome da Categoria", 2)

        def salvar():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome da categoria.")
                return
            if Categoria(Nome=nome).cadastrar(self.conn):
                messagebox.showinfo("Sucesso", f"Categoria '{nome}' cadastrada.")
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar. Nome ja existe?")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,               self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_categorias, self.COR_CINZA_ESC)

    def tela_editar_categoria(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria na tabela.")
            return
        vals = self.cat_tree.item(sel[0])["values"]
        id_cat, nome_atual = vals[0], vals[1]

        self.limpar()
        self.barra_topo("EDITAR CATEGORIA")
        card = self.painel_form("Editar Categoria")

        entry_nome = self.campo(card, "Nome da Categoria", 2, default=nome_atual)

        def salvar():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome nao pode estar vazio.")
                return
            if Categoria(ID=id_cat, Nome=nome).atualizar(self.conn):
                messagebox.showinfo("Sucesso", "Categoria atualizada.")
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar categoria.")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,               self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_categorias, self.COR_CINZA_ESC)

    def apagar_categoria(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria na tabela.")
            return
        vals = self.cat_tree.item(sel[0])["values"]
        id_cat, nome = vals[0], vals[1]
        if messagebox.askyesno("Confirmar", f"Apagar a categoria '{nome}'?"):
            if Categoria(ID=id_cat).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Categoria apagada.")
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Nao foi possivel apagar.\nExistem produtos nesta categoria.")

    def menu_produtos(self):
        self.limpar()
        self.barra_topo("PRODUTOS")

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        barra = tk.Frame(main, bg=self.COR_FUNDO)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar",    self.criar_menu_principal,   self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_produto,  self.COR_SUCESSO)
        self.btn(barra, "Pesquisar", self.tela_pesquisar_produto,  self.COR_PRIMARIA)

        dados = Produto.listar_todos(self.conn)
        self.prod_tree = self.tabela(
            main,
            ["ID", "Nome", "Preco (KZ)", "Categoria", "Stock"],
            dados, [50, 260, 110, 160, 70]
        )
        self._colorir_stock(self.prod_tree)

        barra2 = tk.Frame(main, bg=self.COR_FUNDO)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(barra2, "Editar Selecionado",      lambda: self.tela_editar_produto(),  self.COR_SECUNDARIA)
        self.btn(barra2, "Repor Stock Selecionado", lambda: self.tela_repor_stock(),     self.COR_ALERTA)
        self.btn(barra2, "Apagar Selecionado",      lambda: self.apagar_produto(),       self.COR_PERIGO)

    def _colorir_stock(self, tree):
        for item in tree.get_children():
            stock = tree.item(item)["values"][4]
            if stock == 0:
                tree.item(item, tags=("esgotado",))
            elif stock <= 5:
                tree.item(item, tags=("baixo",))
        tree.tag_configure("esgotado", background="#FADBD8")
        tree.tag_configure("baixo",    background="#FDEBD0")

    def tela_cadastrar_produto(self):
        self.limpar()
        self.barra_topo("NOVO PRODUTO")
        card = self.painel_form("Cadastrar Produto")

        cats = Categoria.listar_todos(self.conn)
        if not cats:
            messagebox.showerror("Erro", "Cadastre uma categoria primeiro.")
            self.menu_produtos()
            return

        e_nome  = self.campo(card, "Nome do Produto",  2)
        e_preco = self.campo(card, "Preco (KZ)",        3)
        e_stock = self.campo(card, "Stock Inicial",     4, default="0")
        cat_vals = [f"{c[0]} - {c[1]}" for c in cats]
        cb_cat, var_cat = self.campo_combo(card, "Categoria", 5, cat_vals)

        def salvar():
            nome  = e_nome.get().strip()
            preco_str = e_preco.get().strip()
            stock_str = e_stock.get().strip()
            cat_sel   = var_cat.get()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome do produto."); return
            if not cat_sel:
                messagebox.showerror("Erro", "Selecione uma categoria."); return
            try:
                preco = float(preco_str.replace(",", "."))
                stock = int(stock_str)
                if preco < 0 or stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Preco e Stock devem ser numeros validos e positivos."); return
            id_cat = int(cat_sel.split(" - ")[0])
            if Produto(Nome=nome, Preco=preco, IDCategoria=id_cat, Stock=stock).cadastrar(self.conn):
                messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado.")
                self.menu_produtos()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar produto.")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,              self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_produtos,  self.COR_CINZA_ESC)

    def tela_editar_produto(self):
        sel = self.prod_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela."); return
        vals = self.prod_tree.item(sel[0])["values"]
        id_p, nome_a, preco_a, cat_nome_a, stock_a = vals

        cats = Categoria.listar_todos(self.conn)
        self.limpar()
        self.barra_topo("EDITAR PRODUTO")
        card = self.painel_form("Editar Produto")

        e_nome  = self.campo(card, "Nome do Produto", 2, default=nome_a)
        e_preco = self.campo(card, "Preco (KZ)",       3, default=str(preco_a))
        e_stock = self.campo(card, "Stock",             4, default=str(stock_a))
        cat_vals = [f"{c[0]} - {c[1]}" for c in cats]
        cb_cat, var_cat = self.campo_combo(card, "Categoria", 5, cat_vals)
        # Pre-selecionar categoria atual
        for v in cat_vals:
            if cat_nome_a in v:
                cb_cat.set(v)
                break

        def salvar():
            nome  = e_nome.get().strip()
            preco_str = e_preco.get().strip()
            stock_str = e_stock.get().strip()
            cat_sel   = var_cat.get()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome do produto."); return
            if not cat_sel:
                messagebox.showerror("Erro", "Selecione uma categoria."); return
            try:
                preco = float(preco_str.replace(",", "."))
                stock = int(stock_str)
                if preco < 0 or stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Preco e Stock devem ser numeros validos e positivos."); return
            id_cat = int(cat_sel.split(" - ")[0])
            if Produto(ID=id_p, Nome=nome, Preco=preco, IDCategoria=id_cat, Stock=stock).atualizar(self.conn):
                messagebox.showinfo("Sucesso", "Produto atualizado.")
                self.menu_produtos()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar produto.")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,             self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_produtos, self.COR_CINZA_ESC)

    def tela_repor_stock(self):
        sel = self.prod_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela."); return
        vals = self.prod_tree.item(sel[0])["values"]
        id_p, nome, _, _, stock_atual = vals

        self.limpar()
        self.barra_topo("REPOR STOCK")
        card = self.painel_form(f"Repor Stock — {nome}")

        tk.Label(card, text=f"Stock actual: {stock_atual} unidades",
                 font=("Segoe UI", 11), bg=self.COR_BRANCO,
                 fg=self.COR_CINZA_ESC).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        e_qty = self.campo(card, "Quantidade a adicionar", 3, default="0")

        def salvar():
            try:
                qty = int(e_qty.get().strip())
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Digite uma quantidade positiva."); return
            cursor = self.conn.cursor()
            cursor.execute("UPDATE produtos SET Stock = Stock + ? WHERE ID = ?", (qty, id_p))
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Stock atualizado. Novo stock: {stock_atual + qty} unidades.")
            self.menu_produtos()

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Confirmar", salvar,             self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar",  self.menu_produtos, self.COR_CINZA_ESC)

    def tela_pesquisar_produto(self):
        self.limpar()
        self.barra_topo("PESQUISAR PRODUTO")
        card = self.painel_form("Pesquisar Produto")

        e_nome = self.campo(card, "Nome (ou parte do nome)", 2)

        result_frame = tk.Frame(self.root, bg=self.COR_FUNDO)

        def pesquisar():
            for w in result_frame.winfo_children():
                w.destroy()
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite um termo de pesquisa."); return
            res = Produto.pesquisar_por_nome(self.conn, nome)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)
            if res:
                self.tabela(result_frame,
                            ["ID", "Nome", "Preco (KZ)", "Categoria", "Stock"],
                            res, [50, 260, 110, 160, 70])
            else:
                tk.Label(result_frame, text=f"Nenhum produto encontrado para '{nome}'.",
                         font=("Segoe UI", 11), bg=self.COR_FUNDO,
                         fg=self.COR_CINZA_ESC).pack(pady=20)

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Pesquisar", pesquisar,          self.COR_PRIMARIA, padx=0)
        self.btn(btns, "Voltar",    self.menu_produtos, self.COR_CINZA_ESC)

    def apagar_produto(self):
        sel = self.prod_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela."); return
        vals = self.prod_tree.item(sel[0])["values"]
        id_p, nome = vals[0], vals[1]
        if messagebox.askyesno("Confirmar", f"Apagar o produto '{nome}'?"):
            if Produto(ID=id_p).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Produto apagado.")
                self.menu_produtos()
            else:
                messagebox.showerror("Erro", "Nao foi possivel apagar.\nExistem vendas com este produto.")

 
    def menu_clientes(self):
        self.limpar()
        self.barra_topo("CLIENTES")

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        barra = tk.Frame(main, bg=self.COR_FUNDO)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar",    self.criar_menu_principal,   self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_cliente,  self.COR_SUCESSO)

        dados = Cliente.listar_todos(self.conn)
        self.cli_tree = self.tabela(main, ["ID", "Nome"], dados, [60, 360])

        barra2 = tk.Frame(main, bg=self.COR_FUNDO)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(barra2, "Editar Selecionado", lambda: self.tela_editar_cliente(), self.COR_SECUNDARIA)
        self.btn(barra2, "Apagar Selecionado", lambda: self.apagar_cliente(),      self.COR_PERIGO)

    def tela_cadastrar_cliente(self):
        self.limpar()
        self.barra_topo("NOVO CLIENTE")
        card = self.painel_form("Cadastrar Cliente")

        e_nome = self.campo(card, "Nome do Cliente", 2)

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome do cliente."); return
            if Cliente(Nome=nome).cadastrar(self.conn):
                messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado.")
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar cliente.")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,              self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_clientes,  self.COR_CINZA_ESC)

    def tela_editar_cliente(self):
        sel = self.cli_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela."); return
        vals = self.cli_tree.item(sel[0])["values"]
        id_c, nome_a = vals[0], vals[1]

        self.limpar()
        self.barra_topo("EDITAR CLIENTE")
        card = self.painel_form("Editar Cliente")

        e_nome = self.campo(card, "Nome do Cliente", 2, default=nome_a)

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome nao pode estar vazio."); return
            if Cliente(ID=id_c, Nome=nome).atualizar(self.conn):
                messagebox.showinfo("Sucesso", "Cliente atualizado.")
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar cliente.")

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar",   salvar,             self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_clientes, self.COR_CINZA_ESC)

    def apagar_cliente(self):
        sel = self.cli_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela."); return
        vals = self.cli_tree.item(sel[0])["values"]
        id_c, nome = vals[0], vals[1]
        if messagebox.askyesno("Confirmar", f"Apagar o cliente '{nome}'?"):
            if Cliente(ID=id_c).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Cliente apagado.")
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Nao foi possivel apagar.\nExistem vendas deste cliente.")


    def realizar_venda(self):
        self.limpar()
        self.barra_topo("REALIZAR VENDA")

        clientes = Cliente.listar_todos(self.conn)
        produtos = Produto.listar_todos(self.conn)

        if not clientes:
            messagebox.showerror("Erro", "Nenhum cliente cadastrado.")
            self.criar_menu_principal(); return
        if not produtos:
            messagebox.showerror("Erro", "Nenhum produto cadastrado.")
            self.criar_menu_principal(); return

        outer = tk.Frame(self.root, bg=self.COR_FUNDO)
        outer.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        card = tk.Frame(outer, bg=self.COR_BRANCO, padx=35, pady=30,
                        highlightthickness=1, highlightbackground=self.COR_CINZA)
        card.pack(fill=tk.BOTH, expand=False)

        tk.Label(card, text="Nova Venda", font=("Segoe UI", 15, "bold"),
                 bg=self.COR_BRANCO, fg=self.COR_TEXTO).grid(
                 row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        tk.Frame(card, bg=self.COR_CINZA, height=1).grid(
                 row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 8))

        # Cliente
        tk.Label(card, text="Cliente", font=("Segoe UI", 10),
                 bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC).grid(
                 row=2, column=0, sticky=tk.W, pady=(10, 2))
        var_cli = tk.StringVar()
        cb_cli = ttk.Combobox(card, textvariable=var_cli, width=50,
                              values=[f"{c[0]} - {c[1]}" for c in clientes],
                              font=("Segoe UI", 10), state="readonly")
        cb_cli.grid(row=2, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))

      
        tk.Label(card, text="Produto", font=("Segoe UI", 10),
                 bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC).grid(
                 row=3, column=0, sticky=tk.W, pady=(10, 2))
        var_prod = tk.StringVar()
        cb_prod = ttk.Combobox(card, textvariable=var_prod, width=50,
                               values=[f"{p[0]} - {p[1]}  |  {p[2]:,.2f} KZ  |  Stock: {p[4]}" for p in produtos],
                               font=("Segoe UI", 10), state="readonly")
        cb_prod.grid(row=3, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))

        
        tk.Label(card, text="Quantidade", font=("Segoe UI", 10),
                 bg=self.COR_BRANCO, fg=self.COR_CINZA_ESC).grid(
                 row=4, column=0, sticky=tk.W, pady=(10, 2))
        e_qty = tk.Entry(card, font=("Segoe UI", 11), width=12,
                         relief=tk.FLAT, bg="#EEF2F5", bd=0,
                         highlightthickness=1, highlightbackground=self.COR_CINZA,
                         highlightcolor=self.COR_SECUNDARIA)
        e_qty.grid(row=4, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        e_qty.insert(0, "1")

        # Total
        lbl_total = tk.Label(card, text="Total:  0,00 KZ",
                             font=("Segoe UI", 14, "bold"),
                             bg=self.COR_BRANCO, fg=self.COR_SUCESSO)
        lbl_total.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(14, 4))

        def atualizar_total(*_):
            try:
                p_sel = var_prod.get()
                qty   = int(e_qty.get() or 0)
                if p_sel and qty > 0:
                    id_p = int(p_sel.split(" - ")[0])
                    prod = next((p for p in produtos if p[0] == id_p), None)
                    if prod:
                        lbl_total.config(text=f"Total:  {prod[2] * qty:,.2f} KZ")
            except Exception:
                pass

        cb_prod.bind("<<ComboboxSelected>>", atualizar_total)
        e_qty.bind("<KeyRelease>", atualizar_total)

        def confirmar():
            c_sel = var_cli.get()
            p_sel = var_prod.get()
            if not c_sel:
                messagebox.showerror("Erro", "Selecione um cliente."); return
            if not p_sel:
                messagebox.showerror("Erro", "Selecione um produto."); return
            try:
                qty = int(e_qty.get())
                if qty <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Quantidade invalida."); return

            id_c = int(c_sel.split(" - ")[0])
            id_p = int(p_sel.split(" - ")[0])
            ok, msg = Venda(IDCliente=id_c, IDProduto=id_p, Qt=qty).realizar_venda(self.conn)
            if ok:
                messagebox.showinfo("Venda Concluida", msg)
                self.criar_menu_principal()
            else:
                messagebox.showerror("Erro na Venda", msg)

        btns = tk.Frame(card, bg=self.COR_BRANCO)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(16, 0))
        self.btn(btns, "Confirmar Venda",      confirmar,                 self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.criar_menu_principal, self.COR_CINZA_ESC)

    def visualizar_vendas(self):
        self.limpar()
        self.barra_topo("HISTORICO DE VENDAS")

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        barra = tk.Frame(main, bg=self.COR_FUNDO)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.criar_menu_principal, self.COR_CINZA_ESC)

        dados = Venda.listar_todos(self.conn)
        if dados:
            self.tabela(main,
                        ["ID", "Total (KZ)", "Cliente", "Produto", "Qtd", "Data / Hora"],
                        dados, [50, 120, 180, 200, 50, 140])
        else:
            tk.Label(main, text="Nenhuma venda registada ainda.",
                     font=("Segoe UI", 12), bg=self.COR_FUNDO,
                     fg=self.COR_CINZA_ESC).pack(pady=60)


    def menu_relatorios(self):
        self.limpar()
        self.barra_topo("RELATORIOS")

        main = tk.Frame(self.root, bg=self.COR_FUNDO)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        barra = tk.Frame(main, bg=self.COR_FUNDO)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.criar_menu_principal, self.COR_CINZA_ESC)

        nb = ttk.Notebook(main)
        nb.pack(fill=tk.BOTH, expand=True, pady=8)

  
        tab1 = tk.Frame(nb, bg=self.COR_FUNDO)
        nb.add(tab1, text="Por Produto")
        dados1 = Venda.vendas_por_produto(self.conn)
        if dados1:
            self.tabela(tab1, ["Produto", "Qtd Vendida", "Total (KZ)"], dados1, [280, 110, 140])
            self._grafico(tab1, dados1, self.COR_SECUNDARIA)
        else:
            tk.Label(tab1, text="Sem dados.", bg=self.COR_FUNDO, font=("Segoe UI", 11),
                     fg=self.COR_CINZA_ESC).pack(pady=30)

      
        tab2 = tk.Frame(nb, bg=self.COR_FUNDO)
        nb.add(tab2, text="Por Mês")
        dados2 = Venda.vendas_por_mes(self.conn)
        if dados2:
            self.tabela(tab2, ["Mês", "Total (KZ)"], dados2, [160, 160])
            self._grafico(tab2, dados2, self.COR_SUCESSO)
        else:
            tk.Label(tab2, text="Sem dados.", bg=self.COR_FUNDO, font=("Segoe UI", 11),
                     fg=self.COR_CINZA_ESC).pack(pady=30)

       
        tab3 = tk.Frame(nb, bg=self.COR_FUNDO)
        nb.add(tab3, text="Por Cliente")
        dados3 = Venda.vendas_por_cliente(self.conn)
        if dados3:
            self.tabela(tab3, ["Cliente", "Nr Vendas", "Total (KZ)"], dados3, [250, 110, 140])
            self._grafico(tab3, dados3, "#8E44AD")
        else:
            tk.Label(tab3, text="Sem dados.", bg=self.COR_FUNDO, font=("Segoe UI", 11),
                     fg=self.COR_CINZA_ESC).pack(pady=30)

        # Stock
        tab4 = tk.Frame(nb, bg=self.COR_FUNDO)
        nb.add(tab4, text="Stock Actual")
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT p.Nome, c.Nome, p.Stock, p.Preco "
            "FROM produtos p LEFT JOIN categoria c ON p.IDCategoria = c.ID "
            "ORDER BY p.Stock ASC"
        )
        dados4 = cursor.fetchall()
        if dados4:
            tree4 = self.tabela(tab4,
                ["Produto", "Categoria", "Stock", "Preco (KZ)"],
                dados4, [260, 160, 80, 120])
            self._colorir_stock(tree4)
        else:
            tk.Label(tab4, text="Sem produtos.", bg=self.COR_FUNDO, font=("Segoe UI", 11),
                     fg=self.COR_CINZA_ESC).pack(pady=30)

    def _grafico(self, parent, dados, cor):
        if not dados:
            return
        valores = [float(row[-1]) for row in dados]
        nomes   = [str(row[0])[:14] for row in dados]
        max_val = max(valores) if valores else 1

        h = 180
        w = max(500, len(dados) * 85)
        pl, pb, pt = 65, 50, 18
        bh = h - pb - pt
        bw = max(32, (w - pl - 20) // len(dados) - 10)

        frame = tk.Frame(parent, bg=self.COR_FUNDO)
        frame.pack(fill=tk.X, pady=4)
        cv = tk.Canvas(frame, height=h, bg=self.COR_BRANCO, highlightthickness=0)
        cv.pack(fill=tk.X, padx=14)

        for i in range(5):
            y = pt + bh - (bh * i // 4)
            cv.create_line(pl, y, w, y, fill="#ECF0F1", dash=(2, 4))
            cv.create_text(pl - 5, y, text=f"{max_val * i / 4:,.0f}",
                           anchor=tk.E, font=("Segoe UI", 7), fill=self.COR_CINZA_ESC)

        for i, (nome, val) in enumerate(zip(nomes, valores)):
            x = pl + i * (bw + 10) + 10
            bar_h = int(bh * val / max_val) if max_val > 0 else 0
            cv.create_rectangle(x, pt + bh - bar_h, x + bw, pt + bh, fill=cor, outline="")
            cv.create_text(x + bw // 2, pt + bh - bar_h - 5,
                           text=f"{val:,.0f}", font=("Segoe UI", 7, "bold"), fill=self.COR_TEXTO)
            cv.create_text(x + bw // 2, pt + bh + 10,
                           text=nome, font=("Segoe UI", 7), fill=self.COR_TEXTO)

 
    def fechar_sistema(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            if self.conn:
                self.db.fechar()
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SistemaVendasGUI()
    app.run()
