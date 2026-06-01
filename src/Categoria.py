import sqlite3

class Categoria:
    def __init__(self, ID=None, Nome=None):
        self.ID = ID
        self.Nome = Nome
    
    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categoria (Nome) VALUES (?)", (self.Nome,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
    
    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE categoria SET Nome = ? WHERE ID = ?", (self.Nome, self.ID))
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
            # Verificar se existem produtos usando esta categoria
            cursor.execute("SELECT COUNT(*) FROM produtos WHERE IDCategoria = ?", (self.ID,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False
            
            cursor.execute("DELETE FROM categoria WHERE ID = ?", (self.ID,))
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
        cursor.execute("SELECT ID, Nome FROM categoria ORDER BY ID")
        categorias = cursor.fetchall()
      
        return categorias