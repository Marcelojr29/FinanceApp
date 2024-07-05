import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCalendarWidget, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import QDate
import sqlite3
import pickle

def init_db():
    conn = sqlite3.connect('financas.db')
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    valor REAL NOT NULL)''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS despesas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data_vencimento TEXT NOT NULL,
                    nome_receita TEXT NOT NULL,
                    parcelas REAL NOT NULL)''')
    conn.commit()
    conn.close()

class FinanceSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.init_db() # inicializa o banco de dados
        self.conn = sqlite3.connect('financas.db')  # Conectar ao banco de dados
        self.cursor = self.conn.cursor()  # Cursor para executar consultas SQL
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistema Financeiro')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()  # Layout principal

        # Layout para entrada de receita
        layout_receita = QHBoxLayout()

        self.receita_nome_label = QLabel('Nome da Receita:')
        self.receita_nome_input = QLineEdit()
        self.receita_valor_label = QLabel('Valor:')
        self.receita_valor_input = QLineEdit()
        self.receita_adicionar_button = QPushButton('Adicionar Receita')
        self.receita_adicionar_button.clicked.connect(self.adicionar_receita)
        self.receita_limpar_button = QPushButton('Limpar campo')
        self.receita_limpar_button.clicked.connect(self.limpar_campos_receita)

        layout_receita.addWidget(self.receita_nome_label)
        layout_receita.addWidget(self.receita_nome_input)
        layout_receita.addWidget(self.receita_valor_label)
        layout_receita.addWidget(self.receita_valor_input)
        layout_receita.addWidget(self.receita_adicionar_button)
        layout_receita.addWidget(self.receita_limpar_button)

        # Layout para entrada de despesa
        layout_despesa = QHBoxLayout()

        self.despesa_nome_label = QLabel('Nome da Despesa:')
        self.despesa_nome_input = QLineEdit()
        self.despesa_valor_label = QLabel('Valor:')
        self.despesa_valor_input = QLineEdit()
        self.despesa_data_vencimento_label = QLabel('Data de Vencimento:')
        self.despesa_data_vencimento_input = QLineEdit()
        self.despesa_selecionar_data_button = QPushButton('Selecionar Data')
        self.despesa_selecionar_data_button.clicked.connect(self.mostrar_calendario)
        self.despesa_nome_receita_label = QLabel('Nome da Receita:')
        self.despesa_nome_receita_input = QLineEdit()
        self.despesa_parcelas_label = QLabel('Parcelas:')
        self.despesa_parcelas_input = QLineEdit()
        self.despesa_adicionar_button = QPushButton('Adicionar Despesa')
        self.despesa_adicionar_button.clicked.connect(self.adicionar_despesa)
        self.despesa_limpar_button = QPushButton('Limpar Campo')
        self.despesa_limpar_button.clicked.connect(self.limpar_campos_despesa)

        layout_despesa.addWidget(self.despesa_nome_label)
        layout_despesa.addWidget(self.despesa_nome_input)
        layout_despesa.addWidget(self.despesa_valor_label)
        layout_despesa.addWidget(self.despesa_valor_input)
        layout_despesa.addWidget(self.despesa_data_vencimento_label)
        layout_despesa.addWidget(self.despesa_data_vencimento_input)
        layout_despesa.addWidget(self.despesa_selecionar_data_button)
        layout_despesa.addWidget(self.despesa_nome_receita_label)
        layout_despesa.addWidget(self.despesa_nome_receita_input)
        layout_despesa.addWidget(self.despesa_parcelas_label)
        layout_despesa.addWidget(self.despesa_parcelas_input)
        layout_despesa.addWidget(self.despesa_adicionar_button)
        layout_despesa.addWidget(self.despesa_limpar_button)

        # Tabelas para exibir balanço e despesas
        self.tabela_balanco = QTableWidget()
        self.tabela_balanco.setColumnCount(2)
        self.tabela_balanco.setHorizontalHeaderLabels(['Receita', 'Valor'])

        self.tabela_despesas = QTableWidget()
        self.tabela_despesas.setColumnCount(5)
        self.tabela_despesas.setHorizontalHeaderLabels(['Despesa', 'Valor', 'Data de Vencimento', 'Nome da Receita', 'Parcelas'])

        self.botao_atualizar = QPushButton('Atualizar Dados')
        self.botao_atualizar.clicked.connect(self.atualizar_dados)

        layout.addLayout(layout_receita)
        layout.addLayout(layout_despesa)
        layout.addWidget(self.tabela_balanco)
        layout.addWidget(self.tabela_despesas)
        layout.addWidget(self.botao_atualizar)

        self.setLayout(layout)

    def init_db(self):
        # Chama a função para inicializar o banco de dados
        init_db()

    def mostrar_calendario(self):
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.clicked.connect(self.definir_data_vencimento)
        self.calendario.show()

    def definir_data_vencimento(self, data):
        self.despesa_data_vencimento_input.setText(data.toString('yyyy-MM-dd'))
        self.calendario.close()

    def adicionar_receita(self):
        try:
            nome = self.receita_nome_input.text()
            valor = self.receita_valor_input.text()

            if not nome or not valor:
                QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
                return

            valor = float(valor)

            # Inserir receita no banco de dados
            self.cursor.execute("INSERT INTO receitas (nome, valor) VALUES (?, ?)", (nome, valor))
            self.conn.commit()
            self.atualizar_dados()

            QMessageBox.information(self, 'Sucesso', f'Receita {nome} adicionada.')

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro: {str(e)}')

    def adicionar_despesa(self):
        nome = self.despesa_nome_input.text()
        valor = self.despesa_valor_input.text()
        data_vencimento = self.despesa_data_vencimento_input.text()
        nome_receita = self.despesa_nome_receita_input.text()
        parcelas = self.despesa_parcelas_input.text()

        if not nome or not valor or not data_vencimento or not nome_receita or not parcelas:
            QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
            return

        try:
            valor = float(valor)
            parcelas = int(parcelas)
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira números válidos para valor e parcelas.')
            return

        # Calcular despesa total
        despesa_total = valor * parcelas

        # Verificar se há fundos suficientes na receita especificada
        self.cursor.execute("SELECT valor FROM receitas WHERE nome=?", (nome_receita,))
        receita = self.cursor.fetchone()
        if not receita or receita[0] < despesa_total:
            QMessageBox.warning(self, 'Erro', f'Não há fundos suficientes em {nome_receita} para cobrir a despesa.')
            return

        # Inserir despesa no banco de dados
        self.cursor.execute("INSERT INTO despesas (nome, valor, data_vencimento, nome_receita, parcelas) VALUES (?, ?, ?, ?, ?)", 
                            (nome, valor, data_vencimento, nome_receita, parcelas))
        self.cursor.execute("UPDATE receitas SET valor = valor - ? WHERE nome = ?", (despesa_total, nome_receita))
        self.conn.commit()
        self.atualizar_dados()

        QMessageBox.information(self, 'Sucesso', f'Despesa {nome} adicionada.')
        
    def limpar_campos_receita(self):
        self.receita_nome_input.clear()
        self.receita_valor_input.clear()
        
    def limpar_campos_despesa(self):
        self.despesa_nome_input.clear()
        self.despesa_valor_input.clear()
        self.despesa_data_vencimento.clear()
        self.despesa_nome_receita.clear()
        self.despesa_parcelas_input.clear()

    def atualizar_dados(self):
        try:
            self.tabela_balanco.setRowCount(0)
            self.cursor.execute("SELECT nome, valor FROM receitas")
            for dados_linha in self.cursor.fetchall():
                linha = self.tabela_balanco.rowCount()
                self.tabela_balanco.insertRow(linha)
                for coluna, item in enumerate(dados_linha):
                    self.tabela_balanco.setItem(linha, coluna, QTableWidgetItem(str(item)))
                    
            self.tabela_balanco.setColumnCount(4) # Atualize o número de colunas para incluir editar e excluir
            self.tabela_balanco.setHorizontalHeaderLabels(['Receita', 'Valor', 'Editar', 'Excluir'])
            
            self.cursor.execute("SELECT id, nome, valor FROM receitas")
            for dados_linha in self.cursor.fetchall():
                linha = self.tabela_balanco.rowCount()
                self.tabela_balanco.insertRow(linha)
                for coluna, item in enumerate(dados_linha[1:]): # Pule o primeiro item (id)
                    self.tabela_balanco.setItem(linha, coluna, QTableWidgetItem(str(item)))
                
                editar_button = QPushButton('Editar')
                editar_button.clicked.connect(lambda _, id=dados_linha[0]: self.editar_receita(id))
                
                excluir_button = QPushButton('Excluir')
                excluir_button.clicked.connect(lambda _, id=dados_linha[0]: self.excluir_receita(id))
                
                self.tabela_balanco.setCellWidget(linha, 2, editar_button)
                self.tabela_balanco.setCellWidget(linha, 3, excluir_button)

            self.tabela_despesas.setColumnCount(7) # Atualize o número de colunas para incluir editar e excluir
            self.tabela_despesas.setHorizontalHeaderLabels(['Despesa', 'Valor', 'Data de Vencimento', 'Nome da Receita', 'Parcelas', 'Editar', 'Excluir'])
            
            self.cursor.execute("SELECT id, nome, valor, data_vencimento, nome_receita, parcelas FROM despesas")
            for dados_linha in self.cursor.fetchall():
                linha = self.tabela_despesas.rowCount()
                self.tabela_despesas.insertRow(linha)
                for coluna, item in enumerate(dados_linha[1:]): # Pule o primeiro item (id)
                    self.tabela_despesas.setItem(linha, coluna, QTableWidgetItem(str(item)))
                    
                editar_button = QPushButton('Editar')
                editar_button.clicked.connect(lambda _, id=dados_linha[0]: self.editar_despesa(id))
                
                excluir_button = QPushButton('Excluir')
                excluir_button.clicked.connect(lambda _, id=dados_linha[0]: self.excluir_despesa(id))
                
                self.tabela_despesas.setCellWidget(linha, 5, editar_button)
                self.tabela_despesas.setCellWidget(linha, 6, excluir_button)
                
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao atualizar os dados: {str(e)}')
            
    def editar_receita(self, id):
        try:
            self.cursor.execute("SELECT nome, valor FROM receitas WHERE id=?", (id,))
            receita = self.cursor.fetchone()
            
            if receita:
                self.receita_nome_input.setText(receita[0])
                self.receita_valor_input.setText(str(receita[1]))
                
                self.cursor.execute("DELETE FROM receitas WHERE id=?", (id,))
                self.conn.commit()
                self.atualizar_dados()
            else:
                QMessageBox.warning(self, 'Erro', 'Receita não encontrada')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao editar a receita: {str(e)}')
            
    def excluir_receita(self, id):
        try:
            self.cursor.execute("DELETE FROM receitas WHERE id=?", (id,))
            self.conn.commit()
            self.atualizar_dados()
            QMessageBox.information(self, 'Sucesso', 'Receita excluída com sucesso.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao excluir a receita: {str(e)}')
            
    def editar_despesa(self, id):
        try:
            self.cursor.execute("SELECT nome, valor, data_vencimento, nome_receita, parcelas FROM despesas WHERE id=?", (id,))
            despesa = self.cursor.fetchone()
            
            if despesa:
                self.despesa_nome_input.setText(despesa[0])
                self.despesa_valor_input.setText(float(despesa[1]))
                self.despesa_data_vencimento_input.setText(despesa[2])
                self.despesa_nome_receita_input.setText(despesa[3])
                self.despesa_parcelas_input.setText(despesa[4])
                
                self.cursor.execute("DELETE FROM despesas WHERE id=?", (id,))
                self.conn.commit()
                self.atualizar_dados()
            else:
                QMessageBox.warning(self, 'Erro', 'Despesa não encontrada.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao editar a despesa: {str(e)}')
    
    def excluir_despesa(self, id):
        try:
            self.cursor.execute("DELETE FROM despesas WHERE id=?", (id,))
            self.conn.commit()
            self.atualizar_dados()
            QMessageBox.information(self, 'Sucesso', 'Despesa excluída com sucesso.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao excluir a despesa: {str(e)}')
    
    """# Salvar dados
    def salvar_dados(self):
        try:
            dados = {
                'receitas': self.obter_dados_tabela(self.tabela_balanco),
                'despesas': self.obter_dados_tabela(self.tabela_despesas),
                # outros dados que precise salvar
            }
            with open('dados_financeiros.pkl', 'wb') as f:
                pickle.dump(dados, f)
            QMessageBox.information(self, 'Sucesso', 'Dados salvos com sucesso.')
            
        except Exception as e:
            QMessageBox.critical(self, 'Erro ao salvar dados', f'Ocorreu um erro ao salvar os dados.')
    
    def obter_dados_tabela(self, tabela):
        dados = []
        for linha in range(tabela.rowCount()):
            linha_dados = {}
            for coluna in range(tabela.ColumnCount()):
                item = tabela.item(linha, coluna)
                if item is not None:
                    linha_dados[tabela.horizontalHeaderItem(coluna).text()] = item.text()
            dados.append(linha_dados)
        return dados
    
    # Carregar dados
    def carregar_dados(self):
        try:
            with open('dados_financeiros.pkl', 'rb') as f:
                dados = pickle.load(f)
                self.preencher_tabela(self.tabela_balanco, dados.get('receitas', []))
                self.preencher_tabela(self.tabela_despesa, dados.get('despesas', []))
            QMessageBox.information(self, 'Sucesso', 'Dados carregados com sucesso.')
                # carregar outros dados necessários
        except FileNotFoundError:
            QMessageBox.warning(self, 'Arquivo não encontrado', 'Não foram encontrados dados salvos.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro ao carregar dados', f'Ocorreu um erro ao carregar os dados: {str(e)}')
    
    def preencher_tabela(self, tabela, dados):
        tabela.setRowCount(0)
        for linha, linha_dados in enumerate(dados):
            tabela.insertRow(linha)
            for coluna, valor in enumerate(linha_dados.values()):
                tabela.setItem(linha, coluna, QTableWidget(valor))"""

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Instanciar e exibir o sistema financeiro principal
    sistema_financeiro = FinanceSystem()
    sistema_financeiro.show()

    sys.exit(app.exec_())

    """EXEMPLO DE USO:
    1. Adicionar uma receita:
        - Preencha o campo "Nome da Receita" com "Salário".
        - Preencha o campo "Valor" com "1598.18".
        - Clique no botão "Adicionar Receita".
    
    2. Adicionar uma receita adicional:
        - Preencha o campo "Nome da Receita" com "Bonificação".
        - Preencha o campo "Valor" com "175".
        - Clique no botão "Adicionar Receita".
    
    3. Adicionar uma despesa:
        - Preencha o campo "Nome da Despesa" com "Mãe".
        - Preencha o campo "Valor" com "500".
        - Clique no botão "Selecionar Data" e selecione a data de vencimento.
        - Preencha o campo "Nome da Receita" com "Salário".
        - Preencha o campo "Parcelas" com "1".
        - Clique no botão "Adicionar Despesa".
    
    4. Adicionar outra despesa:
        - Preencha o campo "Nome da Despesa" com "Óculos 3D".
        - Preencha o campo "Valor" com "150".
        - Clique no botão "Selecionar Data" e selecione a data de vencimento.
        - Preencha o campo "Nome da Receita" com "Bonificação".
        - Preencha o campo "Parcelas" com "1".
        - Clique no botão "Adicionar Despesa".
    
    5. Atualizar e visualizar os dados:
        - Clique no botão "Atualizar Dados" para atualizar e visualizar as receitas e despesas."""