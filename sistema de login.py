import sqlite3

# Conectar ao banco
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
)
""")
conn.commit()

# Criar admin padrão
cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO usuarios (username, password, is_admin) VALUES (?, ?, ?)",
                   ("admin", "1234", 1))
    conn.commit()

# =========================
# FUNÇÕES
# =========================

def registrar_usuario():
    print("\n=== CADASTRO ===")
    username = input("Escolha um usuário: ")
    password = input("Escolha uma senha: ")

    if not username or not password:
        print("⚠️ Preencha todos os campos!")
        return

    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        print("⚠️ Usuário já existe!")
        return

    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()

    print("✅ Conta criada com sucesso!")

def login():
    username = input("Usuário: ")
    password = input("Senha: ")

    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?",
                   (username, password))
    user = cursor.fetchone()

    if user:
        print("✅ Login realizado!")

        if user[3] == 1:
            menu_admin()
        else:
            print("👤 Usuário comum logado.")
    else:
        print("❌ Login inválido.")

def cadastrar_usuario():
    username = input("Novo usuário: ")
    password = input("Senha: ")

    if not username or not password:
        print("⚠️ Preencha todos os campos!")
        return

    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        print("⚠️ Usuário já existe!")
        return

    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()

    print("✅ Usuário cadastrado!")

def remover_usuario():
    username = input("Usuário para remover: ")

    if username == "admin":
        print("⚠️ Não é possível remover o admin!")
        return

    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()

    print("🗑️ Usuário removido!")

def listar_usuarios():
    cursor.execute("SELECT username, is_admin FROM usuarios")
    usuarios = cursor.fetchall()

    print("\n📋 Usuários:")
    for u in usuarios:
        tipo = "ADMIN" if u[1] == 1 else "COMUM"
        print(f"- {u[0]} ({tipo})")

def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1 - Cadastrar usuário")
        print("2 - Remover usuário")
        print("3 - Listar usuários")
        print("4 - Sair")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_usuario()
        elif op == "2":
            remover_usuario()
        elif op == "3":
            listar_usuarios()
        elif op == "4":
            break
        else:
            print("⚠️ Opção inválida!")

# =========================
# MENU PRINCIPAL
# =========================

while True:
    print("\n=== SISTEMA ===")
    print("1 - Login")
    print("2 - Cadastrar")
    print("3 - Sair")

    op = input("Escolha: ")

    if op == "1":
        login()
    elif op == "2":
        registrar_usuario()
    elif op == "3":
        print("Encerrando sistema...")
        break
    else:
        print("⚠️ Opção inválida!")

conn.close()