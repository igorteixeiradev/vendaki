import sqlite3
from datetime import datetime

class Venda:
    def __init__(self, ID=None, IDCarro=None, IDCliente=None, PrecoVenda=None,
                 Desconto=0, PrecoFinal=None, FormaPagamento="Dinheiro",
                 DataVenda=None, IDVendedor=None, Observacoes=""):
        self.ID = ID
        self.IDCarro = IDCarro
        self.IDCliente = IDCliente
        self.PrecoVenda = PrecoVenda
        self.Desconto = Desconto
        self.PrecoFinal = PrecoFinal
        self.FormaPagamento = FormaPagamento
        self.DataVenda = DataVenda or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.IDVendedor = IDVendedor
        self.Observacoes = Observacoes

    def realizar_venda(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Marca, Modelo, PrecoVenda, Estado FROM carros WHERE ID = ?", (self.IDCarro,))
            carro = cursor.fetchone()
            if not carro:
                return False, "Carro não encontrado."
            if carro[3] != "Disponivel":
                return False, f"Este carro não está disponível! Estado actual: {carro[3]}."

            cursor.execute("SELECT Nome FROM clientes WHERE ID = ?", (self.IDCliente,))
            cliente = cursor.fetchone()
            if not cliente:
                return False, "Cliente não encontrado."

            preco_final = self.PrecoFinal if self.PrecoFinal else (carro[2] - self.Desconto)

            cursor.execute(
                "INSERT INTO vendas (IDCarro, IDCliente, PrecoVenda, Desconto, PrecoFinal, FormaPagamento, DataVenda, IDVendedor, Observacoes) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.IDCarro, self.IDCliente, self.PrecoVenda or carro[2], self.Desconto,
                 preco_final, self.FormaPagamento, self.DataVenda, self.IDVendedor, self.Observacoes)
            )
            cursor.execute("UPDATE carros SET Estado = 'Vendido' WHERE ID = ?", (self.IDCarro,))
            conn.commit()
            return True, f"Venda do {carro[0]} {carro[1]} realizada com sucesso!\nValor final: {preco_final:,.2f} KZ"
        except sqlite3.Error as e:
            return False, str(e)

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT v.ID, c.Marca || ' ' || c.Modelo || ' (' || c.Ano || ')', "
            "cl.Nome, v.PrecoFinal, v.Desconto, v.FormaPagamento, v.DataVenda, u.NomeCompleto "
            "FROM vendas v "
            "JOIN carros c ON v.IDCarro = c.ID "
            "JOIN clientes cl ON v.IDCliente = cl.ID "
            "LEFT JOIN utilizadores u ON v.IDVendedor = u.ID "
            "ORDER BY v.DataVenda DESC"
        )
        return cursor.fetchall()

    @staticmethod
    def total_vendas(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(PrecoFinal), 0) FROM vendas")
        return cursor.fetchone()[0]

    @staticmethod
    def total_mes_atual(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(PrecoFinal), 0) FROM vendas WHERE strftime('%Y-%m', DataVenda) = strftime('%Y-%m', 'now', 'localtime')"
        )
        return cursor.fetchone()[0]

    @staticmethod
    def contagem_vendas(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendas")
        return cursor.fetchone()[0]

    @staticmethod
    def vendas_por_mes(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y-%m', DataVenda) as mes, COUNT(*) as qtd, SUM(PrecoFinal) as total "
            "FROM vendas GROUP BY mes ORDER BY mes DESC LIMIT 12"
        )
        return cursor.fetchall()

    @staticmethod
    def vendas_por_vendedor(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT u.NomeCompleto, COUNT(v.ID), SUM(v.PrecoFinal) "
            "FROM vendas v LEFT JOIN utilizadores u ON v.IDVendedor = u.ID "
            "GROUP BY v.IDVendedor ORDER BY SUM(v.PrecoFinal) DESC"
        )
        return cursor.fetchall()

    @staticmethod
    def vendas_por_marca(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.Marca, COUNT(v.ID), SUM(v.PrecoFinal) "
            "FROM vendas v JOIN carros c ON v.IDCarro = c.ID "
            "GROUP BY c.Marca ORDER BY SUM(v.PrecoFinal) DESC LIMIT 10"
        )
        return cursor.fetchall()
