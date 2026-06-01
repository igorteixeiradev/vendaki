import sqlite3
from datetime import datetime

class Venda:
    def __init__(self, ID=None, Preco=None, IDCliente=None, IDProduto=None, Qt=None, DataHora=None):
        self.ID = ID
        self.Preco = Preco
        self.IDCliente = IDCliente
        self.IDProduto = IDProduto
        self.Qt = Qt
        self.DataHora = DataHora or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def realizar_venda(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Nome, Preco, Stock FROM produtos WHERE ID = ?", (self.IDProduto,))
            produto = cursor.fetchone()
            if not produto:
                return False, "Produto não encontrado."

            cursor.execute("SELECT Nome FROM clientes WHERE ID = ?", (self.IDCliente,))
            cliente = cursor.fetchone()
            if not cliente:
                return False, "Cliente não encontrado."

            stock_atual = produto[2]
            if stock_atual < self.Qt:
                return False, f"Stock insuficiente! Disponível: {stock_atual} unidade(s)."

            preco_total = produto[1] * self.Qt

            cursor.execute(
                "INSERT INTO vendas (Preco, IDCliente, IDProduto, Qt, DataHora) VALUES (?, ?, ?, ?, ?)",
                (preco_total, self.IDCliente, self.IDProduto, self.Qt, self.DataHora)
            )
            cursor.execute(
                "UPDATE produtos SET Stock = Stock - ? WHERE ID = ?",
                (self.Qt, self.IDProduto)
            )
            conn.commit()
            return True, "Venda realizada com sucesso!"

        except sqlite3.Error as e:
            return False, str(e)

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT v.ID, v.Preco, c.Nome, p.Nome, v.Qt, v.DataHora "
            "FROM vendas v "
            "JOIN clientes c ON v.IDCliente = c.ID "
            "JOIN produtos p ON v.IDProduto = p.ID "
            "ORDER BY v.DataHora DESC"
        )
        return cursor.fetchall()

    @staticmethod
    def total_vendas(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(Preco), 0) FROM vendas")
        return cursor.fetchone()[0]

    @staticmethod
    def total_hoje(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(Preco), 0) FROM vendas WHERE date(DataHora) = date('now','localtime')"
        )
        return cursor.fetchone()[0]

    @staticmethod
    def contagem_vendas(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendas")
        return cursor.fetchone()[0]

    @staticmethod
    def vendas_por_produto(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.Nome, SUM(v.Qt) as total_qt, SUM(v.Preco) as total_valor "
            "FROM vendas v JOIN produtos p ON v.IDProduto = p.ID "
            "GROUP BY p.ID ORDER BY total_valor DESC LIMIT 10"
        )
        return cursor.fetchall()

    @staticmethod
    def vendas_por_mes(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y-%m', DataHora) as mes, SUM(Preco) as total "
            "FROM vendas GROUP BY mes ORDER BY mes DESC LIMIT 12"
        )
        return cursor.fetchall()

    @staticmethod
    def vendas_por_cliente(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.Nome, COUNT(v.ID) as num_vendas, SUM(v.Preco) as total "
            "FROM vendas v JOIN clientes c ON v.IDCliente = c.ID "
            "GROUP BY c.ID ORDER BY total DESC LIMIT 10"
        )
        return cursor.fetchall()
