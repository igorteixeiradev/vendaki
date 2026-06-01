import sqlite3

class Produto:
    def __init__(self, ID=None, Nome=None, Preco=None, IDCategoria=None, Stock=0):
        self.ID = ID
        self.Nome = Nome
        self.Preco = Preco
        self.IDCategoria = IDCategoria
        self.Stock = Stock

    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO produtos (Nome, Preco, IDCategoria, Stock) VALUES (?, ?, ?, ?)",
                (self.Nome, self.Preco, self.IDCategoria, self.Stock)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False

    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE produtos SET Nome = ?, Preco = ?, IDCategoria = ?, Stock = ? WHERE ID = ?",
                (self.Nome, self.Preco, self.IDCategoria, self.Stock, self.ID)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def apagar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE IDProduto = ?", (self.ID,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM produtos WHERE ID = ?", (self.ID,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def pesquisar_por_nome(conn, nome):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.ID, p.Nome, p.Preco, c.Nome, p.Stock FROM produtos p "
            "LEFT JOIN categoria c ON p.IDCategoria = c.ID "
            "WHERE p.Nome LIKE ? ORDER BY p.ID",
            (f'%{nome}%',)
        )
        return cursor.fetchall()

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.ID, p.Nome, p.Preco, c.Nome, p.Stock FROM produtos p "
            "LEFT JOIN categoria c ON p.IDCategoria = c.ID ORDER BY p.ID"
        )
        return cursor.fetchall()

    @staticmethod
    def atualizar_stock(conn, id_produto, quantidade_vendida):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE produtos SET Stock = Stock - ? WHERE ID = ? AND Stock >= ?",
                (quantidade_vendida, id_produto, quantidade_vendida)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False
