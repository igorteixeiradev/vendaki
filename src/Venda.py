import sqlite3


class Venda:
    def __init__(self, ID=None, Preco=None, IDCliente=None, IDProduto=None, Qt=None):
        self.ID = ID
        self.Preco = Preco
        self.IDCliente = IDCliente
        self.IDProduto = IDProduto
        self.Qt = Qt
    
    def realizar_venda(self, conn):
        cursor = conn.cursor()
        try:
            # Verificar se produto existe
            cursor.execute("SELECT Nome, Preco FROM produtos WHERE ID = ?", (self.IDProduto,))
            produto = cursor.fetchone()
            if not produto:
                return False
            
            # Verificar se cliente existe
            cursor.execute("SELECT Nome FROM clientes WHERE ID = ?", (self.IDCliente,))
            cliente = cursor.fetchone()
            if not cliente:
                return False
            
            # Calcular preço total
            preco_unitario = produto[1]
            preco_total = preco_unitario * self.Qt
            
            # Inserir venda
            cursor.execute("INSERT INTO vendas (Preco, IDCliente, IDProduto, Qt) VALUES (?, ?, ?, ?)",
                         (preco_total, self.IDCliente, self.IDProduto, self.Qt))
            conn.commit()
            return True
            
        except sqlite3.Error:
            return False
    
    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT v.ID, v.Preco, c.Nome, p.Nome, v.Qt FROM vendas v "
                      "JOIN clientes c ON v.IDCliente = c.ID "
                      "JOIN produtos p ON v.IDProduto = p.ID ORDER BY v.ID")
        vendas = cursor.fetchall()
        return vendas