import sqlite3
class Produto:
    def __init__(self, ID=None, Nome=None, Preco=None, IDCategoria=None):
        self.ID = ID
        self.Nome = Nome
        self.Preco = Preco
        self.IDCategoria = IDCategoria
    
    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO produtos (Nome, Preco, IDCategoria) VALUES (?, ?, ?)", 
                         (self.Nome, self.Preco, self.IDCategoria))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
    
    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE produtos SET Nome = ?, Preco = ?, IDCategoria = ? WHERE ID = ?", 
                         (self.Nome, self.Preco, self.IDCategoria, self.ID))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except sqlite3.Error:
            return False
    
    def apagar(self, conn):
        cursor = conn.cursor()
        try:
            # Verificar se existem vendas usando este produto
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE IDProduto = ?", (self.ID,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False
            
            cursor.execute("DELETE FROM produtos WHERE ID = ?", (self.ID,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except sqlite3.Error:
            return False
    
    @staticmethod
    def pesquisar_por_nome(conn, nome):
        cursor = conn.cursor()
        cursor.execute("SELECT p.ID, p.Nome, p.Preco, c.Nome FROM produtos p "
                      "LEFT JOIN categoria c ON p.IDCategoria = c.ID "
                      "WHERE p.Nome LIKE ? ORDER BY p.ID", (f'%{nome}%',))
        produtos = cursor.fetchall()
        
        return produtos
    
    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT p.ID, p.Nome, p.Preco, c.Nome FROM produtos p "
                      "LEFT JOIN categoria c ON p.IDCategoria = c.ID ORDER BY p.ID")
        produtos = cursor.fetchall()
        return produtos

    @staticmethod
    def pesquisar_por_nome_retorno(conn, nome):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produto WHERE Nome LIKE ?", (f'%{nome}%',))
        return cursor.fetchall()    