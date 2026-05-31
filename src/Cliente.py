import sqlite3

class Cliente:
    def __init__(self, ID=None, Nome=None):
        self.ID = ID
        self.Nome = Nome
    
    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (Nome) VALUES (?)", (self.Nome,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
    
    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE clientes SET Nome = ? WHERE ID = ?", (self.Nome, self.ID))
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
            # Verificar se existem vendas usando este cliente
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE IDCliente = ?", (self.ID,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False
            
            cursor.execute("DELETE FROM clientes WHERE ID = ?", (self.ID,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except sqlite3.Error:           
            return False
    
    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nome FROM clientes ORDER BY ID")
        clientes = cursor.fetchall()
        
        return clientes