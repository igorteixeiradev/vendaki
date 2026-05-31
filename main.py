import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from db.database import Database
from src.Categoria import Categoria
from src.Cliente import Cliente
from src.Produto import Produto
from src.Venda import Venda


class SistemaVendasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Vendas")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Conectar ao banco de dados
        self.db = Database()
        self.conn = self.db.conectar()
        if self.conn:
            self.db.criar_tabelas()
            self.db.inserir_dados_iniciais()

        # Criar interface
        self.criar_menu_principal()

    def criar_menu_principal(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="SISTEMA DE VENDAS", font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # Frame para botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        # Botões principais (agora um embaixo do outro)
        botoes = [
            ("Gerenciar Categorias", self.menu_categorias),
            ("Gerenciar Produtos", self.menu_produtos),
            ("Gerenciar Clientes", self.menu_clientes),
            ("Realizar Venda", self.realizar_venda),
            ("Visualizar Vendas", self.visualizar_vendas),
            ("Sair", self.fechar_sistema),
        ]

        for texto, comando in botoes:
            btn = ttk.Button(
                buttons_frame, text=texto, command=comando, width=30, padding=10
            )
            btn.pack(pady=5)  # pady=5 cria espaçamento vertical entre os botões

    def criar_tabela(self, parent, colunas, dados):
        # Frame para tabela e scrollbar
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        tree = ttk.Treeview(
            frame,
            columns=colunas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        tree.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Configurar colunas
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Inserir dados
        for dado in dados:
            tree.insert("", tk.END, values=dado)

        return tree

    def menu_categorias(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="GERENCIAR CATEGORIAS", font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Frame para botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Botões
        ttk.Button(
            buttons_frame, text="Cadastrar", command=self.cadastrar_categoria
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Atualizar", command=self.atualizar_categoria
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Apagar", command=self.apagar_categoria).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            buttons_frame,
            text="Atualizar Lista",
            command=lambda: self.atualizar_lista_categorias(tree),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Voltar", command=self.criar_menu_principal
        ).pack(side=tk.LEFT, padx=5)

        # Lista de categorias
        colunas = ["ID", "Nome"]
        dados = Categoria.listar_todos(self.conn)
        tree = self.criar_tabela(main_frame, colunas, dados)

        # Armazenar referência da tree
        self.categories_tree = tree

    def atualizar_lista_categorias(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        dados = Categoria.listar_todos(self.conn)
        for dado in dados:
            tree.insert("", tk.END, values=dado)

    def cadastrar_categoria(self):
        nome = simpledialog.askstring("Nova Categoria", "Digite o nome da categoria:")
        if nome:
            categoria = Categoria(Nome=nome)
            if categoria.cadastrar(self.conn):
                messagebox.showinfo(
                    "Sucesso", f"Categoria '{nome}' cadastrada com sucesso!"
                )
                self.menu_categorias()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar categoria!")

    def atualizar_categoria(self):
        # Primeiro, listar categorias para o usuário ver
        categorias = Categoria.listar_todos(self.conn)
        if not categorias:
            messagebox.showwarning("Aviso", "Nenhuma categoria cadastrada!")
            return

        id_cat = simpledialog.askinteger(
            "Atualizar Categoria",
            f"Categorias disponiveis (ID - Nome):\n"
            + "\n".join([f"{cat[0]} - {cat[1]}" for cat in categorias])
            + "\n\nDigite o ID da categoria:",
        )
        if id_cat:
            novo_nome = simpledialog.askstring(
                "Atualizar Categoria", "Digite o novo nome:"
            )
            if novo_nome:
                categoria = Categoria(ID=id_cat, Nome=novo_nome)
                if categoria.atualizar(self.conn):
                    messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
                    self.menu_categorias()
                else:
                    messagebox.showerror(
                        "Erro", f"Categoria com ID {id_cat} nao encontrada!"
                    )

    def apagar_categoria(self):
        # Primeiro, listar categorias para o usuário ver
        categorias = Categoria.listar_todos(self.conn)
        if not categorias:
            messagebox.showwarning("Aviso", "Nenhuma categoria cadastrada!")
            return

        id_cat = simpledialog.askinteger(
            "Apagar Categoria",
            f"Categorias disponiveis (ID - Nome):\n"
            + "\n".join([f"{cat[0]} - {cat[1]}" for cat in categorias])
            + "\n\nDigite o ID da categoria:",
        )
        if id_cat:
            if messagebox.askyesno(
                "Confirmar", f"Tem certeza que deseja apagar a categoria {id_cat}?"
            ):
                categoria = Categoria(ID=id_cat)
                if categoria.apagar(self.conn):
                    messagebox.showinfo("Sucesso", "Categoria apagada com sucesso!")
                    self.menu_categorias()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Nao foi possivel apagar a categoria!\n\nMotivos possiveis:\n- Categoria nao encontrada\n- Existem produtos vinculados a esta categoria",
                    )

    def menu_produtos(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="GERENCIAR PRODUTOS", font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Frame para botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Botões
        ttk.Button(
            buttons_frame, text="Cadastrar", command=self.cadastrar_produto
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Atualizar", command=self.atualizar_produto
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Apagar", command=self.apagar_produto).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            buttons_frame, text="Pesquisar", command=self.pesquisar_produto
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame,
            text="Atualizar",
            command=lambda: self.atualizar_lista_produtos(tree),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Voltar", command=self.criar_menu_principal
        ).pack(side=tk.LEFT, padx=5)

        # Lista de produtos
        colunas = ["ID", "Nome", "Preco (€)", "Categoria"]
        dados = Produto.listar_todos(self.conn)
        tree = self.criar_tabela(main_frame, colunas, dados)

        # Armazenar referência da tree
        self.products_tree = tree

    def atualizar_lista_produtos(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        dados = Produto.listar_todos(self.conn)
        for dado in dados:
            tree.insert("", tk.END, values=dado)

    def cadastrar_produto(self):
        nome = simpledialog.askstring("Novo Produto", "Digite o nome do produto:")
        if nome:
            try:
                preco = simpledialog.askfloat(
                    "Novo Produto", "Digite o preco (€):", minvalue=0
                )
                if preco is not None:
                    # Mostrar categorias disponíveis
                    categorias = Categoria.listar_todos(self.conn)
                    if categorias:
                        cat_list = "\n".join(
                            [f"ID: {cat[0]} - {cat[1]}" for cat in categorias]
                        )
                        id_cat = simpledialog.askinteger(
                            "Nova Categoria",
                            f"Categorias disponiveis:\n{cat_list}\n\nDigite o ID da categoria:",
                        )
                        if id_cat:
                            produto = Produto(
                                Nome=nome, Preco=preco, IDCategoria=id_cat
                            )
                            if produto.cadastrar(self.conn):
                                messagebox.showinfo(
                                    "Sucesso",
                                    f"Produto '{nome}' cadastrado com sucesso!",
                                )
                                self.menu_produtos()
                            else:
                                messagebox.showerror(
                                    "Erro",
                                    "Erro ao cadastrar produto!\nVerifique se a categoria existe.",
                                )
                    else:
                        messagebox.showerror(
                            "Erro",
                            "Nenhuma categoria cadastrada!\nCadastre uma categoria primeiro.",
                        )
            except ValueError:
                messagebox.showerror("Erro", "Preco invalido!")

    def atualizar_produto(self):
        # Primeiro, listar produtos para o usuário ver
        produtos = Produto.listar_todos(self.conn)
        if not produtos:
            messagebox.showwarning("Aviso", "Nenhum produto cadastrado!")
            return

        id_prod = simpledialog.askinteger(
            "Atualizar Produto",
            f"Produtos disponiveis (ID - Nome):\n"
            + "\n".join([f"{p[0]} - {p[1]}" for p in produtos])
            + "\n\nDigite o ID do produto:",
        )
        if id_prod:
            novo_nome = simpledialog.askstring(
                "Atualizar Produto", "Digite o novo nome:"
            )
            if novo_nome:
                try:
                    novo_preco = simpledialog.askfloat(
                        "Atualizar Produto", "Digite o novo preco (€):", minvalue=0
                    )
                    if novo_preco is not None:
                        # Mostrar categorias disponíveis
                        categorias = Categoria.listar_todos(self.conn)
                        cat_list = "\n".join(
                            [f"ID: {cat[0]} - {cat[1]}" for cat in categorias]
                        )
                        nova_cat = simpledialog.askinteger(
                            "Atualizar Categoria",
                            f"Categorias disponiveis:\n{cat_list}\n\nDigite o novo ID da categoria:",
                        )
                        if nova_cat:
                            produto = Produto(
                                ID=id_prod,
                                Nome=novo_nome,
                                Preco=novo_preco,
                                IDCategoria=nova_cat,
                            )
                            if produto.atualizar(self.conn):
                                messagebox.showinfo(
                                    "Sucesso", "Produto atualizado com sucesso!"
                                )
                                self.menu_produtos()
                            else:
                                messagebox.showerror(
                                    "Erro", f"Produto com ID {id_prod} nao encontrado!"
                                )
                except ValueError:
                    messagebox.showerror("Erro", "Preco invalido!")

    def apagar_produto(self):
        # Primeiro, listar produtos para o usuário ver
        produtos = Produto.listar_todos(self.conn)
        if not produtos:
            messagebox.showwarning("Aviso", "Nenhum produto cadastrado!")
            return

        id_prod = simpledialog.askinteger(
            "Apagar Produto",
            f"Produtos disponiveis (ID - Nome):\n"
            + "\n".join([f"{p[0]} - {p[1]}" for p in produtos])
            + "\n\nDigite o ID do produto:",
        )
        if id_prod:
            if messagebox.askyesno(
                "Confirmar", f"Tem certeza que deseja apagar o produto {id_prod}?"
            ):
                produto = Produto(ID=id_prod)
                if produto.apagar(self.conn):
                    messagebox.showinfo("Sucesso", "Produto apagado com sucesso!")
                    self.menu_produtos()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Nao foi possivel apagar o produto!\n\nMotivos possiveis:\n- Produto nao encontrado\n- Existem vendas vinculadas a este produto",
                    )

    def pesquisar_produto(self):
        nome = simpledialog.askstring(
            "Pesquisar Produto", "Digite o nome (ou parte) do produto:"
        )
        if nome:
            resultados = Produto.pesquisar_por_nome(self.conn, nome)
            if resultados:
                # Criar janela de resultados
                result_window = tk.Toplevel(self.root)
                result_window.title("Resultados da Pesquisa")
                result_window.geometry("600x400")

                colunas = ["ID", "Nome", "Preco (€)", "Categoria"]
                self.criar_tabela(result_window, colunas, resultados)
            else:
                messagebox.showinfo(
                    "Pesquisa", f"Nenhum produto encontrado com o nome '{nome}'!"
                )

    def menu_clientes(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="GERENCIAR CLIENTES", font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Frame para botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Botões
        ttk.Button(
            buttons_frame, text="Cadastrar", command=self.cadastrar_cliente
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Atualizar", command=self.atualizar_cliente
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Apagar", command=self.apagar_cliente).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            buttons_frame,
            text="Atualizar",
            command=lambda: self.atualizar_lista_clientes(tree),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            buttons_frame, text="Voltar", command=self.criar_menu_principal
        ).pack(side=tk.LEFT, padx=5)

        # Lista de clientes
        colunas = ["ID", "Nome"]
        dados = Cliente.listar_todos(self.conn)
        tree = self.criar_tabela(main_frame, colunas, dados)

        # Armazenar referência da tree
        self.clients_tree = tree

    def atualizar_lista_clientes(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        dados = Cliente.listar_todos(self.conn)
        for dado in dados:
            tree.insert("", tk.END, values=dado)

    def cadastrar_cliente(self):
        nome = simpledialog.askstring("Novo Cliente", "Digite o nome do cliente:")
        if nome:
            cliente = Cliente(Nome=nome)
            if cliente.cadastrar(self.conn):
                messagebox.showinfo(
                    "Sucesso", f"Cliente '{nome}' cadastrado com sucesso!"
                )
                self.menu_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar cliente!")

    def atualizar_cliente(self):
        # Primeiro, listar clientes para o usuário ver
        clientes = Cliente.listar_todos(self.conn)
        if not clientes:
            messagebox.showwarning("Aviso", "Nenhum cliente cadastrado!")
            return

        id_cli = simpledialog.askinteger(
            "Atualizar Cliente",
            f"Clientes disponiveis (ID - Nome):\n"
            + "\n".join([f"{c[0]} - {c[1]}" for c in clientes])
            + "\n\nDigite o ID do cliente:",
        )
        if id_cli:
            novo_nome = simpledialog.askstring(
                "Atualizar Cliente", "Digite o novo nome:"
            )
            if novo_nome:
                cliente = Cliente(ID=id_cli, Nome=novo_nome)
                if cliente.atualizar(self.conn):
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                    self.menu_clientes()
                else:
                    messagebox.showerror(
                        "Erro", f"Cliente com ID {id_cli} nao encontrado!"
                    )

    def apagar_cliente(self):
        # Primeiro, listar clientes para o usuário ver
        clientes = Cliente.listar_todos(self.conn)
        if not clientes:
            messagebox.showwarning("Aviso", "Nenhum cliente cadastrado!")
            return

        id_cli = simpledialog.askinteger(
            "Apagar Cliente",
            f"Clientes disponiveis (ID - Nome):\n"
            + "\n".join([f"{c[0]} - {c[1]}" for c in clientes])
            + "\n\nDigite o ID do cliente:",
        )
        if id_cli:
            if messagebox.askyesno(
                "Confirmar", f"Tem certeza que deseja apagar o cliente {id_cli}?"
            ):
                cliente = Cliente(ID=id_cli)
                if cliente.apagar(self.conn):
                    messagebox.showinfo("Sucesso", "Cliente apagado com sucesso!")
                    self.menu_clientes()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Nao foi possivel apagar o cliente!\n\nMotivos possiveis:\n- Cliente nao encontrado\n- Existem vendas vinculadas a este cliente",
                    )

    def realizar_venda(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="REALIZAR VENDA", font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Frame para seleção
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(pady=20)

        # Selecionar cliente
        ttk.Label(
            selection_frame, text="1. Selecione o Cliente:", font=("Arial", 12)
        ).pack(pady=10)

        clientes = Cliente.listar_todos(self.conn)
        if not clientes:
            messagebox.showerror(
                "Erro", "Nenhum cliente cadastrado!\nCadastre um cliente primeiro."
            )
            self.criar_menu_principal()
            return

        cliente_var = tk.StringVar()
        cliente_combo = ttk.Combobox(
            selection_frame, textvariable=cliente_var, width=50
        )
        cliente_combo["values"] = [f"{c[0]} - {c[1]}" for c in clientes]
        cliente_combo.pack(pady=5)

        # Selecionar produto
        ttk.Label(
            selection_frame, text="2. Selecione o Produto:", font=("Arial", 12)
        ).pack(pady=10)

        produtos = Produto.listar_todos(self.conn)
        if not produtos:
            messagebox.showerror(
                "Erro", "Nenhum produto cadastrado!\nCadastre um produto primeiro."
            )
            self.criar_menu_principal()
            return

        produto_var = tk.StringVar()
        produto_combo = ttk.Combobox(
            selection_frame, textvariable=produto_var, width=50
        )
        produto_combo["values"] = [f"{p[0]} - {p[1]} - €{p[2]:.2f}" for p in produtos]
        produto_combo.pack(pady=5)

        # Quantidade
        ttk.Label(selection_frame, text="3. Quantidade:", font=("Arial", 12)).pack(
            pady=10
        )
        quantidade_entry = ttk.Entry(selection_frame, width=20)
        quantidade_entry.pack(pady=5)

        def confirmar_venda():
            try:
                # Extrair IDs
                cliente_selecionado = cliente_var.get()
                if not cliente_selecionado:
                    messagebox.showerror("Erro", "Selecione um cliente!")
                    return
                id_cliente = int(cliente_selecionado.split(" - ")[0])

                produto_selecionado = produto_var.get()
                if not produto_selecionado:
                    messagebox.showerror("Erro", "Selecione um produto!")
                    return
                id_produto = int(produto_selecionado.split(" - ")[0])

                quantidade = int(quantidade_entry.get())
                if quantidade <= 0:
                    messagebox.showerror(
                        "Erro", "Quantidade invalida! Digite um numero positivo."
                    )
                    return

                # Realizar venda
                venda = Venda(IDCliente=id_cliente, IDProduto=id_produto, Qt=quantidade)
                if venda.realizar_venda(self.conn):
                    messagebox.showinfo(
                        "Sucesso",
                        f"Venda realizada com sucesso!\n\nCliente: {cliente_selecionado}\nProduto: {produto_selecionado}\nQuantidade: {quantidade}",
                    )
                    self.criar_menu_principal()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Erro ao realizar venda!\nVerifique se o cliente e produto existem.",
                    )

            except ValueError:
                messagebox.showerror("Erro", "Dados invalidos! Verifique a quantidade.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao realizar venda: {str(e)}")

        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="Confirmar Venda", command=confirmar_venda).pack(
            side=tk.LEFT, padx=10
        )
        ttk.Button(
            buttons_frame, text="Cancelar", command=self.criar_menu_principal
        ).pack(side=tk.LEFT, padx=10)

    def visualizar_vendas(self):
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = ttk.Label(
            main_frame, text="VISUALIZAR VENDAS", font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Botão voltar
        ttk.Button(
            main_frame, text="Voltar ao Menu", command=self.criar_menu_principal
        ).pack(pady=10)

        # Lista de vendas
        colunas = ["ID", "Total (€)", "Cliente", "Produto", "Quantidade"]
        dados = Venda.listar_todos(self.conn)
        if dados:
            self.criar_tabela(main_frame, colunas, dados)
        else:
            ttk.Label(
                main_frame, text="Nenhuma venda realizada ainda!", font=("Arial", 12)
            ).pack(pady=50)

    def fechar_sistema(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?"):
            if self.conn:
                self.db.fechar()
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SistemaVendasGUI()
    app.run()
