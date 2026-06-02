import tkinter as tk
from tkinter import messagebox, ttk

from db.database import Database
from src.Carro import Carro
from src.Categoria import Categoria
from src.Cliente import Cliente
from src.Venda import Venda


class HinginoRafaelApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VENDAKI — Sistema de Gestão de Stand de Carros")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)

     
        self.COR_BG = "#0F1923"  # fundo muito escuro
        self.COR_PAINEL = "#16232E"  # painel lateral / cards
        self.COR_CARD = "#1C2F3E"  # cards secundários
        self.COR_OURO = "#C9A84C"  # dourado principal
        self.COR_OURO_CLR = "#F0C040"  # dourado mais claro (hover)
        self.COR_BRANCO = "#F4F6F8"
        self.COR_CINZA = "#8A9BAE"
        self.COR_CINZA_ESC = "#4A5A6A"
        self.COR_SUCESSO = "#2ECC71"
        self.COR_PERIGO = "#E74C3C"
        self.COR_ALERTA = "#E67E22"
        self.COR_INFO = "#3498DB"

        self.utilizador_logado = None  # guarda dados do login

        self.root.configure(bg=self.COR_BG)
        self._configurar_estilos()

        self.db = Database()
        self.conn = self.db.conectar()
        if self.conn:
            self.db.criar_tabelas()
            self.db.inserir_dados_iniciais()

        self.tela_login()

    def _configurar_estilos(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background=self.COR_BG)
        s.configure("TLabel", background=self.COR_BG, foreground=self.COR_BRANCO)
        s.configure(
            "Treeview",
            rowheight=27,
            font=("Segoe UI", 10),
            background=self.COR_CARD,
            foreground=self.COR_BRANCO,
            fieldbackground=self.COR_CARD,
        )
        s.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.COR_PAINEL,
            foreground=self.COR_OURO,
        )
        s.map(
            "Treeview",
            background=[("selected", self.COR_OURO)],
            foreground=[("selected", self.COR_BG)],
        )
        s.configure("TNotebook", background=self.COR_BG)
        s.configure(
            "TNotebook.Tab",
            background=self.COR_PAINEL,
            foreground=self.COR_CINZA,
            padding=[12, 5],
            font=("Segoe UI", 10),
        )
        s.map(
            "TNotebook.Tab",
            background=[("selected", self.COR_OURO)],
            foreground=[("selected", self.COR_BG)],
        )
        s.configure(
            "TCombobox",
            fieldbackground=self.COR_CARD,
            background=self.COR_CARD,
            foreground=self.COR_BRANCO,
            selectbackground=self.COR_OURO,
        )
        s.configure(
            "TScrollbar", background=self.COR_CINZA_ESC, troughcolor=self.COR_CARD
        )

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def barra_topo(self, titulo, subtitulo=""):
        barra = tk.Frame(self.root, bg=self.COR_PAINEL, height=58)
        barra.pack(fill=tk.X)
        barra.pack_propagate(False)

        tk.Label(
            barra,
            text="⬡ VENDAKI",
            font=("Segoe UI", 13, "bold"),
            bg=self.COR_PAINEL,
            fg=self.COR_OURO,
        ).pack(side=tk.LEFT, padx=20, pady=14)
        tk.Frame(barra, bg=self.COR_CINZA_ESC, width=1).pack(
            side=tk.LEFT, fill=tk.Y, pady=10
        )
        tk.Label(
            barra,
            text=f"  {titulo}",
            font=("Segoe UI", 14, "bold"),
            bg=self.COR_PAINEL,
            fg=self.COR_BRANCO,
        ).pack(side=tk.LEFT, padx=10)
        if subtitulo:
            tk.Label(
                barra,
                text=subtitulo,
                font=("Segoe UI", 10),
                bg=self.COR_PAINEL,
                fg=self.COR_CINZA,
            ).pack(side=tk.LEFT)

        if self.utilizador_logado:
            tk.Label(
                barra,
                text=f"{self.utilizador_logado['nome']}  [{self.utilizador_logado['cargo']}]",
                font=("Segoe UI", 9),
                bg=self.COR_PAINEL,
                fg=self.COR_CINZA,
            ).pack(side=tk.RIGHT, padx=18)

    def btn(
        self,
        parent,
        texto,
        comando,
        cor=None,
        lado=tk.LEFT,
        padx=5,
        pady=0,
        largura=None,
    ):
        cor = cor or self.COR_OURO
        kw = dict(
            text=texto,
            command=comando,
            bg=cor,
            fg=self.COR_BG if cor == self.COR_OURO else self.COR_BRANCO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            activebackground=self.COR_OURO_CLR,
            activeforeground=self.COR_BG,
        )
        if largura:
            kw["width"] = largura
        b = tk.Button(parent, **kw)
        b.pack(side=lado, padx=padx, pady=pady)
        return b

    def campo(self, parent, label, row, default="", largura=38, show=None):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 10),
            bg=self.COR_CARD,
            fg=self.COR_CINZA,
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=(10, 2))
        kw = dict(
            font=("Segoe UI", 11),
            width=largura,
            relief=tk.FLAT,
            bg="#1E3045",
            fg=self.COR_BRANCO,
            bd=0,
            insertbackground=self.COR_OURO,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
            highlightcolor=self.COR_OURO,
        )
        if show:
            kw["show"] = show
        entry = tk.Entry(parent, **kw)
        entry.grid(row=row, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        if default:
            entry.insert(0, str(default))
        return entry

    def campo_combo(self, parent, label, row, valores, largura=36):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 10),
            bg=self.COR_CARD,
            fg=self.COR_CINZA,
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=(10, 2))
        var = tk.StringVar()
        combo = ttk.Combobox(
            parent,
            textvariable=var,
            values=valores,
            width=largura,
            font=("Segoe UI", 10),
            state="readonly",
        )
        combo.grid(row=row, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        return combo, var

    def card_stat(self, parent, titulo, valor, cor, icone=""):
        c = tk.Frame(parent, bg=cor, padx=18, pady=14)
        c.pack(side=tk.LEFT, padx=6, pady=6, fill=tk.BOTH, expand=True)
        tk.Label(
            c,
            text=f"{icone}  {titulo}" if icone else titulo,
            font=("Segoe UI", 9),
            bg=cor,
            fg="#CCCCCC",
        ).pack(anchor=tk.W)
        tk.Label(
            c,
            text=str(valor),
            font=("Segoe UI", 18, "bold"),
            bg=cor,
            fg=self.COR_BRANCO,
        ).pack(anchor=tk.W)

    def tabela(self, parent, colunas, dados, larguras=None):
        frame = tk.Frame(parent, bg=self.COR_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        sy = ttk.Scrollbar(frame)
        sy.pack(side=tk.RIGHT, fill=tk.Y)
        sx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        sx.pack(side=tk.BOTTOM, fill=tk.X)
        tree = ttk.Treeview(
            frame,
            columns=colunas,
            show="headings",
            yscrollcommand=sy.set,
            xscrollcommand=sx.set,
        )
        tree.pack(fill=tk.BOTH, expand=True)
        sy.config(command=tree.yview)
        sx.config(command=tree.xview)
        for i, col in enumerate(colunas):
            tree.heading(col, text=col)
            w = larguras[i] if larguras and i < len(larguras) else 120
            tree.column(col, width=w, anchor=tk.CENTER)
        for row in dados:
            tree.insert("", tk.END, values=row)
        return tree

    def painel_form(self, titulo):
        outer = tk.Frame(self.root, bg=self.COR_BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        card = tk.Frame(
            outer,
            bg=self.COR_CARD,
            padx=35,
            pady=30,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
        )
        card.pack(fill=tk.BOTH, expand=False)
        tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 15, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_OURO,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        tk.Frame(card, bg=self.COR_CINZA_ESC, height=1).grid(
            row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 8)
        )
        return card

   
    def tela_login(self):
        self.limpar()
        self.root.configure(bg=self.COR_BG)

      
        fundo = tk.Frame(self.root, bg=self.COR_BG)
        fundo.pack(fill=tk.BOTH, expand=True)

     
        esq = tk.Frame(fundo, bg=self.COR_PAINEL, width=440)
        esq.pack(side=tk.LEFT, fill=tk.Y)
        esq.pack_propagate(False)

        tk.Label(
            esq, text="⬡", font=("Segoe UI", 52), bg=self.COR_PAINEL, fg=self.COR_OURO
        ).pack(pady=(80, 0))
        tk.Label(
            esq,
            text="VENDAKI",
            font=("Georgia", 22, "bold"),
            bg=self.COR_PAINEL,
            fg=self.COR_OURO,
        ).pack(pady=(8, 0))
        tk.Label(
            esq,
            text="Stand de Automóveis",
            font=("Segoe UI", 12),
            bg=self.COR_PAINEL,
            fg=self.COR_CINZA,
        ).pack(pady=(4, 0))
        tk.Frame(esq, bg=self.COR_OURO, height=2, width=200).pack(pady=20)
        tk.Label(
            esq,
            text="Gestão inteligente\ndo seu stand de carros",
            font=("Segoe UI", 11),
            bg=self.COR_PAINEL,
            fg=self.COR_CINZA,
            justify=tk.CENTER,
        ).pack(pady=10)
        tk.Label(
            esq,
            text="● Catálogo de Veículos\n● Gestão de Clientes\n● Controlo de Vendas\n● Relatórios Avançados",
            font=("Segoe UI", 10),
            bg=self.COR_PAINEL,
            fg=self.COR_CINZA,
            justify=tk.LEFT,
        ).pack(pady=20, padx=50, anchor=tk.W)

        # Coluna direita — formulário
        dir_ = tk.Frame(fundo, bg=self.COR_BG)
        dir_.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        centro = tk.Frame(dir_, bg=self.COR_CARD, padx=50, pady=50)
        centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(
            centro,
            text="Acesso ao Sistema",
            font=("Segoe UI", 18, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_BRANCO,
        ).pack(pady=(0, 5))
        tk.Label(
            centro,
            text="Insira as suas credenciais",
            font=("Segoe UI", 10),
            bg=self.COR_CARD,
            fg=self.COR_CINZA,
        ).pack(pady=(0, 25))

        # Campo utilizador
        tk.Label(
            centro,
            text="Utilizador",
            font=("Segoe UI", 10),
            bg=self.COR_CARD,
            fg=self.COR_CINZA,
            anchor=tk.W,
        ).pack(fill=tk.X)
        self.e_login_user = tk.Entry(
            centro,
            font=("Segoe UI", 12),
            width=28,
            relief=tk.FLAT,
            bg="#1E3045",
            fg=self.COR_BRANCO,
            insertbackground=self.COR_OURO,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
            highlightcolor=self.COR_OURO,
        )
        self.e_login_user.pack(pady=(4, 14), ipady=6)
        self.e_login_user.insert(0, "admin")

        # Campo senha
        tk.Label(
            centro,
            text="Senha",
            font=("Segoe UI", 10),
            bg=self.COR_CARD,
            fg=self.COR_CINZA,
            anchor=tk.W,
        ).pack(fill=tk.X)
        self.e_login_pass = tk.Entry(
            centro,
            font=("Segoe UI", 12),
            width=28,
            show="●",
            relief=tk.FLAT,
            bg="#1E3045",
            fg=self.COR_BRANCO,
            insertbackground=self.COR_OURO,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
            highlightcolor=self.COR_OURO,
        )
        self.e_login_pass.pack(pady=(4, 20), ipady=6)

        self.lbl_erro_login = tk.Label(
            centro, text="", font=("Segoe UI", 9), bg=self.COR_CARD, fg=self.COR_PERIGO
        )
        self.lbl_erro_login.pack()

        btn_login = tk.Button(
            centro,
            text="ENTRAR NO SISTEMA",
            command=self._fazer_login,
            bg=self.COR_OURO,
            fg=self.COR_BG,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground=self.COR_OURO_CLR,
            activeforeground=self.COR_BG,
            width=25,
        )
        btn_login.pack(pady=(10, 0))

        # Bind Enter
        self.root.bind("<Return>", lambda e: self._fazer_login())

        tk.Label(
            centro,
            text="Credenciais padrão: admin / admin123",
            font=("Segoe UI", 8),
            bg=self.COR_CARD,
            fg=self.COR_CINZA_ESC,
        ).pack(pady=(12, 0))

    def _fazer_login(self):
        user = self.e_login_user.get().strip()
        senha = self.e_login_pass.get().strip()
        if not user or not senha:
            self.lbl_erro_login.config(text="Preencha todos os campos.")
            return
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT ID, NomeCompleto, Cargo FROM utilizadores WHERE Usuario = ? AND Senha = ?",
            (user, senha),
        )
        row = cursor.fetchone()
        if row:
            self.utilizador_logado = {"id": row[0], "nome": row[1], "cargo": row[2]}
            self.root.unbind("<Return>")
            self.menu_principal()
        else:
            self.lbl_erro_login.config(text="Utilizador ou senha incorretos!")

    # ─────────────────────────── MENU PRINCIPAL ───────────────────────────
    def menu_principal(self):
        self.limpar()
        self.barra_topo("PAINEL PRINCIPAL")

        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=14)

        # ── Cards de estatísticas ──
        tk.Label(
            main,
            text="RESUMO DO STAND",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_BG,
            fg=self.COR_OURO,
        ).pack(anchor=tk.W)
        cards_f = tk.Frame(main, bg=self.COR_BG)
        cards_f.pack(fill=tk.X, pady=(4, 14))

        cursor = self.conn.cursor()
        estados = Carro.total_por_estado(self.conn)
        n_disponiveis = estados.get("Disponivel", 0)
        n_vendidos = estados.get("Vendido", 0)
        n_reservados = estados.get("Reservado", 0)
        cursor.execute("SELECT COUNT(*) FROM clientes")
        n_clientes = cursor.fetchone()[0]

        self.card_stat(cards_f, "Carros Disponíveis", n_disponiveis, "#1A6B3A", "")
        self.card_stat(cards_f, "Carros Vendidos", n_vendidos, "#7B2D1A", "")
        self.card_stat(cards_f, "Reservados", n_reservados, "#4A3A0A", "")
        self.card_stat(cards_f, "Clientes", n_clientes, "#1A3A6B", "")
        self.card_stat(
            cards_f,
            "Vendas Totais",
            f"{Venda.total_vendas(self.conn):,.0f} KZ",
            "#4A1A6B",
            "",
        )
        self.card_stat(
            cards_f,
            "Vendas Mês Actual",
            f"{Venda.total_mes_atual(self.conn):,.0f} KZ",
            "#1A4A4A",
            "",
        )

        # ── Painéis informativos ──
        paineis = tk.Frame(main, bg=self.COR_BG)
        paineis.pack(fill=tk.X, pady=(0, 14))

        # Top carros mais vendidos por marca
        p_left = tk.Frame(
            paineis,
            bg=self.COR_CARD,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
        )
        p_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        tk.Label(
            p_left,
            text="Top Marcas Vendidas",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_OURO,
        ).pack(anchor=tk.W, pady=(0, 6))
        top = Venda.vendas_por_marca(self.conn)[:5]
        if top:
            for i, (marca, qt, valor) in enumerate(top, 1):
                r = tk.Frame(p_left, bg=self.COR_CARD)
                r.pack(fill=tk.X, pady=1)
                tk.Label(
                    r,
                    text=f"{i}. {marca}",
                    font=("Segoe UI", 10),
                    bg=self.COR_CARD,
                    fg=self.COR_BRANCO,
                    anchor=tk.W,
                ).pack(side=tk.LEFT)
                tk.Label(
                    r,
                    text=f"{valor:,.0f} KZ  ({qt} vend.)",
                    font=("Segoe UI", 9),
                    bg=self.COR_CARD,
                    fg=self.COR_CINZA,
                ).pack(side=tk.RIGHT)
        else:
            tk.Label(
                p_left,
                text="Sem vendas ainda.",
                font=("Segoe UI", 9),
                bg=self.COR_CARD,
                fg=self.COR_CINZA,
            ).pack()

        # Carros recém adicionados
        p_right = tk.Frame(
            paineis,
            bg=self.COR_CARD,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
        )
        p_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(
            p_right,
            text="Últimos Carros em Stock",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_OURO,
        ).pack(anchor=tk.W, pady=(0, 6))
        cursor.execute(
            "SELECT Marca, Modelo, Ano, PrecoVenda FROM carros WHERE Estado = 'Disponivel' ORDER BY ID DESC LIMIT 5"
        )
        ultimos = cursor.fetchall()
        if ultimos:
            for marca, modelo, ano, preco in ultimos:
                r = tk.Frame(p_right, bg=self.COR_CARD)
                r.pack(fill=tk.X, pady=1)
                tk.Label(
                    r,
                    text=f"{marca} {modelo} ({ano})",
                    font=("Segoe UI", 10),
                    bg=self.COR_CARD,
                    fg=self.COR_BRANCO,
                    anchor=tk.W,
                ).pack(side=tk.LEFT)
                tk.Label(
                    r,
                    text=f"{preco:,.0f} KZ",
                    font=("Segoe UI", 9),
                    bg=self.COR_CARD,
                    fg=self.COR_OURO,
                ).pack(side=tk.RIGHT)
        else:
            tk.Label(
                p_right,
                text="Nenhum carro disponível.",
                font=("Segoe UI", 9),
                bg=self.COR_CARD,
                fg=self.COR_CINZA,
            ).pack()

        # ── Botões de navegação ──
        tk.Label(
            main,
            text="MÓDULOS DO SISTEMA",
            font=("Segoe UI", 11, "bold"),
            bg=self.COR_BG,
            fg=self.COR_OURO,
        ).pack(anchor=tk.W, pady=(6, 4))
        nav = tk.Frame(main, bg=self.COR_BG)
        nav.pack(fill=tk.X)

        botoes = [
            ("Categorias", self.menu_categorias, self.COR_PAINEL),
            ("Carros", self.menu_carros, "#1C3A28"),
            ("Clientes", self.menu_clientes, "#1A2850"),
            ("Realizar Venda", self.realizar_venda, "#2A4A1A"),
            ("Histórico Vendas", self.visualizar_vendas, "#1A3A4A"),
            ("Relatórios", self.menu_relatorios, "#2A1A40"),
            ("Utilizadores", self.menu_utilizadores, "#3A2A10"),
            ("Sair", self._confirmar_sair, "#4A1A1A"),
        ]
        for texto, cmd, cor in botoes:
            tk.Button(
                nav,
                text=texto,
                command=cmd,
                bg=cor,
                fg=self.COR_BRANCO,
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT,
                padx=8,
                pady=9,
                cursor="hand2",
                width=16,
                activebackground=self.COR_OURO,
                activeforeground=self.COR_BG,
            ).pack(side=tk.LEFT, padx=3)

    # ─────────────────────────── CATEGORIAS ───────────────────────────
    def menu_categorias(self):
        self.limpar()
        self.barra_topo("CATEGORIAS DE CARROS")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_categoria, self.COR_SUCESSO)
        dados = Categoria.listar_todos(self.conn)
        self.cat_tree = self.tabela(
            main, ["ID", "Nome", "Descrição"], dados, [60, 200, 450]
        )
        barra2 = tk.Frame(main, bg=self.COR_BG)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(
            barra2, "Editar", lambda: self.tela_editar_categoria(), self.COR_INFO
        )
        self.btn(barra2, "Apagar", lambda: self._apagar_categoria(), self.COR_PERIGO)

    def tela_cadastrar_categoria(self):
        self.limpar()
        self.barra_topo("NOVA CATEGORIA")
        card = self.painel_form("Cadastrar Categoria de Carros")
        e_nome = self.campo(card, "Nome da Categoria", 2)
        e_desc = self.campo(card, "Descrição", 3)

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome da categoria.")
                return
            if Categoria(Nome=nome, Descricao=e_desc.get().strip()).cadastrar(
                self.conn
            ):
                messagebox.showinfo("Sucesso", f"Categoria '{nome}' cadastrada.")
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar. Nome já existe?")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_categorias, self.COR_CINZA_ESC)

    def tela_editar_categoria(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria na tabela.")
            return
        vals = self.cat_tree.item(sel[0])["values"]
        id_cat, nome_a, desc_a = vals[0], vals[1], vals[2] if len(vals) > 2 else ""
        self.limpar()
        self.barra_topo("EDITAR CATEGORIA")
        card = self.painel_form("Editar Categoria")
        e_nome = self.campo(card, "Nome da Categoria", 2, default=nome_a)
        e_desc = self.campo(card, "Descrição", 3, default=str(desc_a))

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome não pode estar vazio.")
                return
            if Categoria(
                ID=id_cat, Nome=nome, Descricao=e_desc.get().strip()
            ).atualizar(self.conn):
                messagebox.showinfo("Sucesso", "Categoria atualizada.")
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar categoria.")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_categorias, self.COR_CINZA_ESC)

    def _apagar_categoria(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        vals = self.cat_tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"Apagar a categoria '{vals[1]}'?"):
            if Categoria(ID=vals[0]).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Categoria apagada.")
                self.menu_categorias()
            else:
                messagebox.showerror(
                    "Erro", "Não foi possível apagar.\nExistem carros nesta categoria."
                )

    # ─────────────────────────── CARROS ───────────────────────────
    def menu_carros(self):
        self.limpar()
        self.barra_topo("GESTÃO DE CARROS")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_carro, self.COR_SUCESSO)
        self.btn(barra, "Pesquisar", self.tela_pesquisar_carro, self.COR_INFO)

        dados = Carro.listar_todos(self.conn)
        colunas = [
            "ID",
            "Marca",
            "Modelo",
            "Ano",
            "Cor",
            "Combustível",
            "Câmbio",
            "Km",
            "Chassis",
            "Preço (KZ)",
            "Categoria",
            "Estado",
        ]
        self.carro_tree = self.tabela(
            main, colunas, dados, [40, 100, 110, 55, 80, 90, 85, 75, 110, 130, 100, 90]
        )
        self._colorir_estado(self.carro_tree)

        barra2 = tk.Frame(main, bg=self.COR_BG)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(barra2, "Editar", lambda: self.tela_editar_carro(), self.COR_INFO)
        self.btn(barra2, "Apagar", lambda: self._apagar_carro(), self.COR_PERIGO)
        self.btn(
            barra2, "Reservar", lambda: self._alterar_estado("Reservado"), "#7B6010"
        )
        self.btn(
            barra2,
            "Disponível",
            lambda: self._alterar_estado("Disponivel"),
            self.COR_SUCESSO,
        )

    def _colorir_estado(self, tree):
        for item in tree.get_children():
            estado = tree.item(item)["values"][11]
            if estado == "Vendido":
                tree.item(item, tags=("vendido",))
            elif estado == "Reservado":
                tree.item(item, tags=("reservado",))
            elif estado == "Disponivel":
                tree.item(item, tags=("disponivel",))
        tree.tag_configure("vendido", background="#2D0F0F", foreground="#FF9090")
        tree.tag_configure("reservado", background="#2D2A0F", foreground="#FFD080")
        tree.tag_configure("disponivel", background="#0F2D1A", foreground="#90FFB0")

    def tela_cadastrar_carro(self):
        self.limpar()
        self.barra_topo("CADASTRAR NOVO CARRO")
        cats = Categoria.listar_todos(self.conn)
        if not cats:
            messagebox.showerror("Erro", "Cadastre uma categoria primeiro.")
            self.menu_carros()
            return
        card = self.painel_form("Dados do Veículo")
        e_marca = self.campo(card, "Marca", 2)
        e_modelo = self.campo(card, "Modelo", 3)
        e_ano = self.campo(card, "Ano", 4, default="2024")
        e_cor = self.campo(card, "Cor", 5)
        cb_comb, var_comb = self.campo_combo(
            card,
            "Combustível",
            6,
            ["Gasolina", "Diesel", "Híbrido", "Eléctrico", "GPL"],
        )
        cb_trans, var_trans = self.campo_combo(
            card, "Transmissão", 7, ["Manual", "Automático", "Semi-Automático"]
        )
        e_km = self.campo(card, "Quilometragem", 8, default="0")
        e_chassi = self.campo(card, "N.º Chassis", 9)
        e_motor = self.campo(card, "N.º Motor", 10)
        e_preco = self.campo(card, "Preço de Venda (KZ)", 11)
        cat_vals = [f"{c[0]} - {c[1]}" for c in cats]
        cb_cat, var_cat = self.campo_combo(card, "Categoria", 12, cat_vals)
        cb_est, var_est = self.campo_combo(
            card, "Estado", 13, ["Disponivel", "Reservado", "Em Reparação"]
        )
        e_obs = self.campo(card, "Observações", 14)

        def salvar():
            marca = e_marca.get().strip()
            modelo = e_modelo.get().strip()
            if not marca or not modelo:
                messagebox.showerror("Erro", "Marca e Modelo são obrigatórios.")
                return
            if not var_cat.get():
                messagebox.showerror("Erro", "Selecione uma categoria.")
                return
            try:
                ano = int(e_ano.get())
                km = int(e_km.get() or 0)
                preco = float(e_preco.get().replace(",", "."))
                if preco <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Erro", "Ano, Km e Preço devem ser números válidos."
                )
                return
            id_cat = int(var_cat.get().split(" - ")[0])
            ok = Carro(
                Marca=marca,
                Modelo=modelo,
                Ano=ano,
                Cor=e_cor.get().strip(),
                Combustivel=var_comb.get(),
                Transmissao=var_trans.get(),
                Quilometragem=km,
                NumChassi=e_chassi.get().strip() or None,
                NumMotor=e_motor.get().strip(),
                PrecoVenda=preco,
                IDCategoria=id_cat,
                Estado=var_est.get() or "Disponivel",
                Observacoes=e_obs.get().strip(),
            ).cadastrar(self.conn)
            if ok:
                messagebox.showinfo(
                    "Sucesso", f"{marca} {modelo} cadastrado com sucesso!"
                )
                self.menu_carros()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar. Chassis já existente?")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=20, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_carros, self.COR_CINZA_ESC)

    def tela_editar_carro(self):
        sel = self.carro_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um carro na tabela.")
            return
        vals = self.carro_tree.item(sel[0])["values"]
        id_c = vals[0]
        carro = Carro.buscar_por_id(self.conn, id_c)
        cats = Categoria.listar_todos(self.conn)
        self.limpar()
        self.barra_topo("EDITAR CARRO")
        card = self.painel_form("Editar Dados do Veículo")
        e_marca = self.campo(card, "Marca", 2, default=carro[1])
        e_modelo = self.campo(card, "Modelo", 3, default=carro[2])
        e_ano = self.campo(card, "Ano", 4, default=carro[3])
        e_cor = self.campo(card, "Cor", 5, default=carro[4])
        cb_comb, var_comb = self.campo_combo(
            card,
            "Combustível",
            6,
            ["Gasolina", "Diesel", "Híbrido", "Eléctrico", "GPL"],
        )
        var_comb.set(carro[5] or "")
        cb_trans, var_trans = self.campo_combo(
            card, "Transmissão", 7, ["Manual", "Automático", "Semi-Automático"]
        )
        var_trans.set(carro[6] or "")
        e_km = self.campo(card, "Quilometragem", 8, default=carro[7])
        e_chassi = self.campo(card, "N.º Chassis", 9, default=carro[8] or "")
        e_motor = self.campo(card, "N.º Motor", 10, default=carro[9] or "")
        e_preco = self.campo(card, "Preço de Venda (KZ)", 11, default=carro[10])
        cat_vals = [f"{c[0]} - {c[1]}" for c in cats]
        cb_cat, var_cat = self.campo_combo(card, "Categoria", 12, cat_vals)
        for v in cat_vals:
            if str(carro[11]) in v or (carro[15] and carro[15] in v):
                cb_cat.set(v)
                break
        cb_est, var_est = self.campo_combo(
            card, "Estado", 13, ["Disponivel", "Reservado", "Em Reparação", "Vendido"]
        )
        var_est.set(carro[12] or "Disponivel")
        e_obs = self.campo(card, "Observações", 14, default=carro[14] or "")

        def salvar():
            try:
                ano = int(e_ano.get())
                km = int(e_km.get() or 0)
                preco = float(e_preco.get().replace(",", "."))
                if preco <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Erro", "Ano, Km e Preço devem ser números válidos."
                )
                return
            if not var_cat.get():
                messagebox.showerror("Erro", "Selecione uma categoria.")
                return
            id_cat = int(var_cat.get().split(" - ")[0])
            ok = Carro(
                ID=id_c,
                Marca=e_marca.get().strip(),
                Modelo=e_modelo.get().strip(),
                Ano=ano,
                Cor=e_cor.get().strip(),
                Combustivel=var_comb.get(),
                Transmissao=var_trans.get(),
                Quilometragem=km,
                NumChassi=e_chassi.get().strip() or None,
                NumMotor=e_motor.get().strip(),
                PrecoVenda=preco,
                IDCategoria=id_cat,
                Estado=var_est.get() or "Disponivel",
                Observacoes=e_obs.get().strip(),
            ).atualizar(self.conn)
            if ok:
                messagebox.showinfo("Sucesso", "Carro actualizado com sucesso!")
                self.menu_carros()
            else:
                messagebox.showerror("Erro", "Erro ao actualizar. Chassis duplicado?")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=20, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_carros, self.COR_CINZA_ESC)

    def _apagar_carro(self):
        sel = self.carro_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um carro.")
            return
        vals = self.carro_tree.item(sel[0])["values"]
        if messagebox.askyesno(
            "Confirmar", f"Apagar o {vals[1]} {vals[2]} ({vals[3]})?"
        ):
            if Carro(ID=vals[0]).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Carro apagado.")
                self.menu_carros()
            else:
                messagebox.showerror(
                    "Erro",
                    "Não é possível apagar. Existem vendas associadas a este carro.",
                )

    def _alterar_estado(self, novo_estado):
        sel = self.carro_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um carro.")
            return
        vals = self.carro_tree.item(sel[0])["values"]
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE carros SET Estado = ? WHERE ID = ?", (novo_estado, vals[0])
        )
        self.conn.commit()
        self.menu_carros()

    def tela_pesquisar_carro(self):
        self.limpar()
        self.barra_topo("PESQUISAR CARRO")
        card = self.painel_form("Pesquisar Veículo")
        e_termo = self.campo(card, "Marca / Modelo / Cor / Chassis", 2)
        result_f = tk.Frame(self.root, bg=self.COR_BG)

        def pesquisar():
            for w in result_f.winfo_children():
                w.destroy()
            termo = e_termo.get().strip()
            if not termo:
                messagebox.showerror("Erro", "Digite um termo de pesquisa.")
                return
            res = Carro.pesquisar(self.conn, termo)
            result_f.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)
            if res:
                self.tabela(
                    result_f,
                    [
                        "ID",
                        "Marca",
                        "Modelo",
                        "Ano",
                        "Cor",
                        "Comb.",
                        "Câmbio",
                        "Km",
                        "Chassis",
                        "Preço (KZ)",
                        "Categoria",
                        "Estado",
                    ],
                    res,
                    [40, 100, 110, 55, 80, 80, 85, 75, 110, 130, 100, 90],
                )
            else:
                tk.Label(
                    result_f,
                    text=f"Nenhum veículo encontrado para '{termo}'.",
                    font=("Segoe UI", 11),
                    bg=self.COR_BG,
                    fg=self.COR_CINZA,
                ).pack(pady=20)

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Pesquisar", pesquisar, self.COR_OURO, padx=0)
        self.btn(btns, "Voltar", self.menu_carros, self.COR_CINZA_ESC)

    # ─────────────────────────── CLIENTES ───────────────────────────
    def menu_clientes(self):
        self.limpar()
        self.barra_topo("GESTÃO DE CLIENTES")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        self.btn(barra, "Cadastrar", self.tela_cadastrar_cliente, self.COR_SUCESSO)
        dados = Cliente.listar_todos(self.conn)
        self.cli_tree = self.tabela(
            main,
            ["ID", "Nome", "Telefone", "Email", "BI"],
            dados,
            [50, 200, 120, 200, 120],
        )
        barra2 = tk.Frame(main, bg=self.COR_BG)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(barra2, "Editar", lambda: self.tela_editar_cliente(), self.COR_INFO)
        self.btn(barra2, "Apagar", lambda: self._apagar_cliente(), self.COR_PERIGO)

    def tela_cadastrar_cliente(self):
        self.limpar()
        self.barra_topo("NOVO CLIENTE")
        card = self.painel_form("Cadastrar Cliente")
        e_nome = self.campo(card, "Nome Completo", 2)
        e_tel = self.campo(card, "Telefone", 3)
        e_email = self.campo(card, "Email", 4)
        e_end = self.campo(card, "Endereço", 5)
        e_bi = self.campo(card, "Nº BI", 6)

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome é obrigatório.")
                return
            if Cliente(
                Nome=nome,
                Telefone=e_tel.get().strip(),
                Email=e_email.get().strip(),
                Endereco=e_end.get().strip(),
                BI=e_bi.get().strip() or None,
            ).cadastrar(self.conn):
                messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado.")
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar. BI já existente?")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_clientes, self.COR_CINZA_ESC)

    def tela_editar_cliente(self):
        sel = self.cli_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        vals = self.cli_tree.item(sel[0])["values"]
        id_c = vals[0]
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE ID = ?", (id_c,))
        c = cursor.fetchone()
        self.limpar()
        self.barra_topo("EDITAR CLIENTE")
        card = self.painel_form("Editar Dados do Cliente")
        e_nome = self.campo(card, "Nome Completo", 2, default=c[1])
        e_tel = self.campo(card, "Telefone", 3, default=c[2] or "")
        e_email = self.campo(card, "Email", 4, default=c[3] or "")
        e_end = self.campo(card, "Endereço", 5, default=c[4] or "")
        e_bi = self.campo(card, "Nº BI", 6, default=c[5] or "")

        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome é obrigatório.")
                return
            if Cliente(
                ID=id_c,
                Nome=nome,
                Telefone=e_tel.get().strip(),
                Email=e_email.get().strip(),
                Endereco=e_end.get().strip(),
                BI=e_bi.get().strip() or None,
            ).atualizar(self.conn):
                messagebox.showinfo("Sucesso", "Cliente atualizado.")
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar cliente.")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_clientes, self.COR_CINZA_ESC)

    def _apagar_cliente(self):
        sel = self.cli_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        vals = self.cli_tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"Apagar o cliente '{vals[1]}'?"):
            if Cliente(ID=vals[0]).apagar(self.conn):
                messagebox.showinfo("Sucesso", "Cliente apagado.")
                self.menu_clientes()
            else:
                messagebox.showerror(
                    "Erro",
                    "Não é possível apagar.\nExistem vendas associadas a este cliente.",
                )

    # ─────────────────────────── REALIZAR VENDA ───────────────────────────
    def realizar_venda(self):
        self.limpar()
        self.barra_topo("REALIZAR VENDA")

        clientes = Cliente.listar_todos(self.conn)
        carros = Carro.listar_todos(self.conn, apenas_disponiveis=True)

        if not clientes:
            messagebox.showerror("Erro", "Nenhum cliente cadastrado.")
            self.menu_principal()
            return
        if not carros:
            messagebox.showerror("Erro", "Nenhum carro disponível em stock.")
            self.menu_principal()
            return

        outer = tk.Frame(self.root, bg=self.COR_BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        card = tk.Frame(
            outer,
            bg=self.COR_CARD,
            padx=35,
            pady=30,
            highlightthickness=1,
            highlightbackground=self.COR_CINZA_ESC,
        )
        card.pack(fill=tk.BOTH, expand=False)

        tk.Label(
            card,
            text="Registar Nova Venda",
            font=("Segoe UI", 15, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_OURO,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        tk.Frame(card, bg=self.COR_CINZA_ESC, height=1).grid(
            row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 12)
        )

        def lbl(r, txt):
            tk.Label(
                card,
                text=txt,
                font=("Segoe UI", 10),
                bg=self.COR_CARD,
                fg=self.COR_CINZA,
                anchor=tk.W,
            ).grid(row=r, column=0, sticky=tk.W, pady=(10, 2))

        def entry_widget(r, w=50, default=""):
            e = tk.Entry(
                card,
                font=("Segoe UI", 11),
                width=w,
                relief=tk.FLAT,
                bg="#1E3045",
                fg=self.COR_BRANCO,
                insertbackground=self.COR_OURO,
                highlightthickness=1,
                highlightbackground=self.COR_CINZA_ESC,
                highlightcolor=self.COR_OURO,
            )
            e.grid(row=r, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
            if default:
                e.insert(0, default)
            return e

        lbl(2, "Cliente")
        var_cli = tk.StringVar()
        cb_cli = ttk.Combobox(
            card,
            textvariable=var_cli,
            width=55,
            values=[f"{c[0]} - {c[1]} | Tel: {c[2]}" for c in clientes],
            font=("Segoe UI", 10),
            state="readonly",
        )
        cb_cli.grid(row=2, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))

        lbl(3, "Veículo")
        var_carro = tk.StringVar()
        cb_carro = ttk.Combobox(
            card,
            textvariable=var_carro,
            width=55,
            values=[
                f"{c[0]} - {c[1]} {c[2]} {c[3]} {c[4]} | {c[9]:,.0f} KZ" for c in carros
            ],
            font=("Segoe UI", 10),
            state="readonly",
        )
        cb_carro.grid(row=3, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))

        lbl(4, "Desconto (KZ)")
        e_desc = entry_widget(4, w=20, default="0")

        lbl(5, "Forma de Pagamento")
        var_pag = tk.StringVar()
        cb_pag = ttk.Combobox(
            card,
            textvariable=var_pag,
            width=25,
            values=[
                "Dinheiro",
                "Transferência Bancária",
                "Cheque",
                "Crédito Automóvel",
                "Misto",
            ],
            font=("Segoe UI", 10),
            state="readonly",
        )
        cb_pag.grid(row=5, column=1, sticky=tk.W, padx=(12, 0), pady=(10, 2))
        cb_pag.set("Dinheiro")

        lbl(6, "Observações")
        e_obs = entry_widget(6, default="")

        lbl_total = tk.Label(
            card,
            text="Preço Final:  — KZ",
            font=("Segoe UI", 15, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_OURO,
        )
        lbl_total.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(16, 4))

        def atualizar_total(*_):
            try:
                c_sel = var_carro.get()
                desc = float(e_desc.get() or 0)
                if c_sel:
                    id_c = int(c_sel.split(" - ")[0])
                    carro_sel = next((c for c in carros if c[0] == id_c), None)
                    if carro_sel:
                        final = carro_sel[9] - desc
                        lbl_total.config(text=f"Preço Final:  {final:,.2f} KZ")
            except Exception:
                pass

        cb_carro.bind("<<ComboboxSelected>>", atualizar_total)
        e_desc.bind("<KeyRelease>", atualizar_total)

        def confirmar():
            if not var_cli.get():
                messagebox.showerror("Erro", "Selecione um cliente.")
                return
            if not var_carro.get():
                messagebox.showerror("Erro", "Selecione um veículo.")
                return
            try:
                desc = float(e_desc.get() or 0)
                if desc < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Desconto inválido.")
                return

            id_cli = int(var_cli.get().split(" - ")[0])
            id_carro = int(var_carro.get().split(" - ")[0])
            carro_sel = next((c for c in carros if c[0] == id_carro), None)
            preco_final = (carro_sel[9] if carro_sel else 0) - desc

            ok, msg = Venda(
                IDCarro=id_carro,
                IDCliente=id_cli,
                PrecoVenda=carro_sel[9] if carro_sel else 0,
                Desconto=desc,
                PrecoFinal=preco_final,
                FormaPagamento=var_pag.get(),
                IDVendedor=self.utilizador_logado["id"],
                Observacoes=e_obs.get().strip(),
            ).realizar_venda(self.conn)

            if ok:
                messagebox.showinfo("Venda Concluída!", msg)
                self.menu_principal()
            else:
                messagebox.showerror("Erro na Venda", msg)

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(16, 0))
        self.btn(btns, "Confirmar Venda", confirmar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_principal, self.COR_CINZA_ESC)

    # ─────────────────────────── HISTÓRICO VENDAS ───────────────────────────
    def visualizar_vendas(self):
        self.limpar()
        self.barra_topo("HISTÓRICO DE VENDAS")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        dados = Venda.listar_todos(self.conn)
        if dados:
            self.tabela(
                main,
                [
                    "ID",
                    "Veículo",
                    "Cliente",
                    "Preço Final (KZ)",
                    "Desconto (KZ)",
                    "Pagamento",
                    "Data",
                    "Vendedor",
                ],
                dados,
                [45, 220, 160, 130, 100, 130, 140, 140],
            )
        else:
            tk.Label(
                main,
                text="Nenhuma venda registada ainda.",
                font=("Segoe UI", 13),
                bg=self.COR_BG,
                fg=self.COR_CINZA,
            ).pack(pady=60)

    # ─────────────────────────── RELATÓRIOS ───────────────────────────
    def menu_relatorios(self):
        self.limpar()
        self.barra_topo("RELATÓRIOS")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        nb = ttk.Notebook(main)
        nb.pack(fill=tk.BOTH, expand=True, pady=8)

        # Tab vendas por mês
        t1 = tk.Frame(nb, bg=self.COR_BG)
        nb.add(t1, text="Vendas por Mês")
        d1 = Venda.vendas_por_mes(self.conn)
        if d1:
            self.tabela(t1, ["Mês", "Qtd Vendas", "Total (KZ)"], d1, [140, 110, 180])
            self._grafico(t1, [(r[0], r[2]) for r in d1], self.COR_OURO)
        else:
            tk.Label(
                t1,
                text="Sem dados.",
                bg=self.COR_BG,
                font=("Segoe UI", 11),
                fg=self.COR_CINZA,
            ).pack(pady=30)

        # Tab vendas por marca
        t2 = tk.Frame(nb, bg=self.COR_BG)
        nb.add(t2, text="Por Marca")
        d2 = Venda.vendas_por_marca(self.conn)
        if d2:
            self.tabela(t2, ["Marca", "Qtd Vendas", "Total (KZ)"], d2, [200, 110, 180])
            self._grafico(t2, [(r[0], r[2]) for r in d2], self.COR_SUCESSO)
        else:
            tk.Label(
                t2,
                text="Sem dados.",
                bg=self.COR_BG,
                font=("Segoe UI", 11),
                fg=self.COR_CINZA,
            ).pack(pady=30)

        # Tab vendas por vendedor
        t3 = tk.Frame(nb, bg=self.COR_BG)
        nb.add(t3, text="Por Vendedor")
        d3 = Venda.vendas_por_vendedor(self.conn)
        if d3:
            self.tabela(
                t3, ["Vendedor", "Qtd Vendas", "Total (KZ)"], d3, [220, 110, 180]
            )
        else:
            tk.Label(
                t3,
                text="Sem dados.",
                bg=self.COR_BG,
                font=("Segoe UI", 11),
                fg=self.COR_CINZA,
            ).pack(pady=30)

        # Tab stock actual
        t4 = tk.Frame(nb, bg=self.COR_BG)
        nb.add(t4, text="Stock Actual")
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT c.Marca, c.Modelo, c.Ano, c.Cor, cat.Nome, c.Quilometragem, c.PrecoVenda, c.Estado "
            "FROM carros c LEFT JOIN categoria_carros cat ON c.IDCategoria = cat.ID "
            "ORDER BY c.Estado, c.Marca"
        )
        d4 = cursor.fetchall()
        if d4:
            tree4 = self.tabela(
                t4,
                [
                    "Marca",
                    "Modelo",
                    "Ano",
                    "Cor",
                    "Categoria",
                    "Km",
                    "Preço (KZ)",
                    "Estado",
                ],
                d4,
                [100, 110, 55, 80, 110, 80, 130, 90],
            )
            self._colorir_estado(tree4)
        else:
            tk.Label(
                t4,
                text="Sem carros.",
                bg=self.COR_BG,
                font=("Segoe UI", 11),
                fg=self.COR_CINZA,
            ).pack(pady=30)

    def _grafico(self, parent, dados, cor):
        if not dados:
            return
        valores = [float(r[1]) for r in dados]
        nomes = [str(r[0])[:13] for r in dados]
        max_val = max(valores) if valores else 1
        h, pl, pb, pt = 190, 70, 52, 20
        w = max(500, len(dados) * 90)
        bh = h - pb - pt
        bw = max(32, (w - pl - 20) // max(len(dados), 1) - 10)
        frame = tk.Frame(parent, bg=self.COR_BG)
        frame.pack(fill=tk.X, pady=4)
        cv = tk.Canvas(frame, height=h, bg=self.COR_CARD, highlightthickness=0)
        cv.pack(fill=tk.X, padx=14)
        for i in range(5):
            y = pt + bh - (bh * i // 4)
            cv.create_line(pl, y, w, y, fill=self.COR_CINZA_ESC, dash=(3, 5))
            cv.create_text(
                pl - 6,
                y,
                text=f"{max_val * i / 4:,.0f}",
                anchor=tk.E,
                font=("Segoe UI", 7),
                fill=self.COR_CINZA,
            )
        for i, (nome, val) in enumerate(zip(nomes, valores)):
            x = pl + i * (bw + 12) + 8
            bar_h = int(bh * val / max_val) if max_val > 0 else 0
            cv.create_rectangle(
                x, pt + bh - bar_h, x + bw, pt + bh, fill=cor, outline=""
            )
            cv.create_text(
                x + bw // 2,
                pt + bh - bar_h - 6,
                text=f"{val:,.0f}",
                font=("Segoe UI", 7, "bold"),
                fill=self.COR_BRANCO,
            )
            cv.create_text(
                x + bw // 2,
                pt + bh + 10,
                text=nome,
                font=("Segoe UI", 7),
                fill=self.COR_CINZA,
            )

    # ─────────────────────────── UTILIZADORES ───────────────────────────
    def menu_utilizadores(self):
        if self.utilizador_logado["cargo"] != "Administrador":
            messagebox.showwarning(
                "Acesso Negado", "Apenas o Administrador pode gerir utilizadores."
            )
            return
        self.limpar()
        self.barra_topo("GESTÃO DE UTILIZADORES")
        main = tk.Frame(self.root, bg=self.COR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        barra = tk.Frame(main, bg=self.COR_BG)
        barra.pack(fill=tk.X, pady=6)
        self.btn(barra, "Voltar", self.menu_principal, self.COR_CINZA_ESC)
        self.btn(
            barra, "Novo Utilizador", self.tela_novo_utilizador, self.COR_SUCESSO
        )
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT ID, NomeCompleto, Usuario, Cargo FROM utilizadores ORDER BY ID"
        )
        dados = cursor.fetchall()
        self.util_tree = self.tabela(
            main,
            ["ID", "Nome Completo", "Utilizador", "Cargo"],
            dados,
            [50, 220, 160, 130],
        )
        barra2 = tk.Frame(main, bg=self.COR_BG)
        barra2.pack(fill=tk.X, pady=4)
        self.btn(
            barra2,
            "Alterar Senha",
            lambda: self.tela_alterar_senha(),
            self.COR_ALERTA,
        )
        self.btn(barra2, "Apagar", lambda: self._apagar_utilizador(), self.COR_PERIGO)

    def tela_novo_utilizador(self):
        self.limpar()
        self.barra_topo("NOVO UTILIZADOR")
        card = self.painel_form("Criar Utilizador")
        e_nome = self.campo(card, "Nome Completo", 2)
        e_user = self.campo(card, "Nome de Utilizador", 3)
        e_senha = self.campo(card, "Senha", 4, show="●")
        cb_cargo, var_cargo = self.campo_combo(
            card, "Cargo", 5, ["Administrador", "Vendedor", "Recepcionista"]
        )

        def salvar():
            nome = e_nome.get().strip()
            user = e_user.get().strip()
            senha = e_senha.get().strip()
            if not nome or not user or not senha:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO utilizadores (NomeCompleto, Usuario, Senha, Cargo) VALUES (?,?,?,?)",
                    (nome, user, senha, var_cargo.get() or "Vendedor"),
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"Utilizador '{user}' criado.")
                self.menu_utilizadores()
            except Exception:
                messagebox.showerror("Erro", "Nome de utilizador já existe.")

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_utilizadores, self.COR_CINZA_ESC)

    def tela_alterar_senha(self):
        sel = self.util_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um utilizador.")
            return
        vals = self.util_tree.item(sel[0])["values"]
        id_u = vals[0]
        self.limpar()
        self.barra_topo("ALTERAR SENHA")
        card = self.painel_form(f"Alterar Senha — {vals[1]}")
        e_nova = self.campo(card, "Nova Senha", 2, show="●")
        e_conf = self.campo(card, "Confirmar Senha", 3, show="●")

        def salvar():
            nova = e_nova.get().strip()
            conf = e_conf.get().strip()
            if not nova:
                messagebox.showerror("Erro", "A senha não pode estar vazia.")
                return
            if nova != conf:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE utilizadores SET Senha = ? WHERE ID = ?", (nova, id_u)
            )
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso.")
            self.menu_utilizadores()

        btns = tk.Frame(card, bg=self.COR_CARD)
        btns.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        self.btn(btns, "Salvar", salvar, self.COR_SUCESSO, padx=0)
        self.btn(btns, "Cancelar", self.menu_utilizadores, self.COR_CINZA_ESC)

    def _apagar_utilizador(self):
        sel = self.util_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um utilizador.")
            return
        vals = self.util_tree.item(sel[0])["values"]
        if vals[0] == self.utilizador_logado["id"]:
            messagebox.showerror("Erro", "Não pode apagar o próprio utilizador.")
            return
        if messagebox.askyesno("Confirmar", f"Apagar o utilizador '{vals[2]}'?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM utilizadores WHERE ID = ?", (vals[0],))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Utilizador apagado.")
            self.menu_utilizadores()

    # ─────────────────────────── SAIR ───────────────────────────
    def _confirmar_sair(self):
        if messagebox.askyesno("Sair", "Tem a certeza que deseja sair?"):
            if self.conn:
                self.db.fechar()
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HinginoRafaelApp()
    app.run()
