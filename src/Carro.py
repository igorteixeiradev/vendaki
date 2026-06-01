import sqlite3

class Carro:
    def __init__(self, ID=None, Marca=None, Modelo=None, Ano=None, Cor=None,
                 Combustivel=None, Transmissao=None, Quilometragem=0,
                 NumChassi=None, NumMotor=None, PrecoVenda=None,
                 IDCategoria=None, Estado="Disponivel", Observacoes=""):
        self.ID = ID
        self.Marca = Marca
        self.Modelo = Modelo
        self.Ano = Ano
        self.Cor = Cor
        self.Combustivel = Combustivel
        self.Transmissao = Transmissao
        self.Quilometragem = Quilometragem
        self.NumChassi = NumChassi
        self.NumMotor = NumMotor
        self.PrecoVenda = PrecoVenda
        self.IDCategoria = IDCategoria
        self.Estado = Estado
        self.Observacoes = Observacoes

    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO carros (Marca, Modelo, Ano, Cor, Combustivel, Transmissao, Quilometragem, NumChassi, NumMotor, PrecoVenda, IDCategoria, Estado, Observacoes) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.Marca, self.Modelo, self.Ano, self.Cor, self.Combustivel,
                 self.Transmissao, self.Quilometragem, self.NumChassi, self.NumMotor,
                 self.PrecoVenda, self.IDCategoria, self.Estado, self.Observacoes)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False

    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE carros SET Marca=?, Modelo=?, Ano=?, Cor=?, Combustivel=?, Transmissao=?, "
                "Quilometragem=?, NumChassi=?, NumMotor=?, PrecoVenda=?, IDCategoria=?, Estado=?, Observacoes=? "
                "WHERE ID=?",
                (self.Marca, self.Modelo, self.Ano, self.Cor, self.Combustivel,
                 self.Transmissao, self.Quilometragem, self.NumChassi, self.NumMotor,
                 self.PrecoVenda, self.IDCategoria, self.Estado, self.Observacoes, self.ID)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def apagar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE IDCarro = ?", (self.ID,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM carros WHERE ID = ?", (self.ID,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def listar_todos(conn, apenas_disponiveis=False):
        cursor = conn.cursor()
        filtro = "WHERE c.Estado = 'Disponivel'" if apenas_disponiveis else ""
        cursor.execute(
            f"SELECT c.ID, c.Marca, c.Modelo, c.Ano, c.Cor, c.Combustivel, c.Transmissao, "
            f"c.Quilometragem, c.NumChassi, c.PrecoVenda, cat.Nome, c.Estado "
            f"FROM carros c LEFT JOIN categoria_carros cat ON c.IDCategoria = cat.ID "
            f"{filtro} ORDER BY c.Marca, c.Modelo"
        )
        return cursor.fetchall()

    @staticmethod
    def buscar_por_id(conn, id_carro):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.*, cat.Nome FROM carros c LEFT JOIN categoria_carros cat ON c.IDCategoria = cat.ID WHERE c.ID = ?",
            (id_carro,)
        )
        return cursor.fetchone()

    @staticmethod
    def pesquisar(conn, termo):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.ID, c.Marca, c.Modelo, c.Ano, c.Cor, c.Combustivel, c.Transmissao, "
            "c.Quilometragem, c.NumChassi, c.PrecoVenda, cat.Nome, c.Estado "
            "FROM carros c LEFT JOIN categoria_carros cat ON c.IDCategoria = cat.ID "
            "WHERE c.Marca LIKE ? OR c.Modelo LIKE ? OR c.Cor LIKE ? OR c.NumChassi LIKE ? "
            "ORDER BY c.Marca",
            (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")
        )
        return cursor.fetchall()

    @staticmethod
    def total_por_estado(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT Estado, COUNT(*) FROM carros GROUP BY Estado")
        return dict(cursor.fetchall())

    @staticmethod
    def valor_estoque(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(PrecoVenda), 0) FROM carros WHERE Estado = 'Disponivel'")
        return cursor.fetchone()[0]
