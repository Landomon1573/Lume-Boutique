import mysql.connector

# Conexão com o Banco de Dados
def conectar():
    try:
        return mysql.connector.connect(
    host="localhost",
    user="SEU_USUARIO",
    password="SUA_SENHA",
    database="lume_boutique"
)
    except mysql.connector.Error as err:
        print(f"\n[ERRO DE CONEXÃO] Não foi possível conectar ao banco de dados: {err}")
        return None

# Cadastro de Cliente/Usuário
def cadastrar_usuario():
    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor()

    print("\n=== CADASTRO DE USUÁRIO ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    try:
        sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, senha, "cliente")
        cursor.execute(sql, valores)
        conexao.commit()
        print("\nUsuário cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print(f"\nErro ao cadastrar: {err}")
    finally:
        cursor.close()
        conexao.close()

# Autenticação de Usuário (Login)
def login():
    conexao = conectar()
    if not conexao: return None
    cursor = conexao.cursor(dictionary=True)

    print("\n=== LOGIN ===")
    email = input("Email: ")
    senha = input("Senha: ")

    sql = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
    cursor.execute(sql, (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        print(f"\nBem vinda(o), {usuario['nome']}!")
    else:
        print("\n[ERRO] Email ou senha inválidos!")
        usuario = None

    cursor.close()
    conexao.close()
    return usuario

# Exibição de Categorias
def listar_categorias():
    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()

    print("\n=== CATEGORIAS ===")
    for categoria in categorias:
        print(f"{categoria[0]} - {categoria[1]}")

    cursor.close()
    conexao.close()

# Cadastro de Novo Produto
def cadastrar_produto():
    listar_categorias()
    try:
        categoria_id = int(input("\nDigite o ID da categoria desejada: "))
        nome = input("Nome do produto: ")
        descricao = input("Descrição: ")
        preco = float(input("Preço: "))
        estoque = int(input("Quantidade em estoque: "))
    except ValueError:
        print("\n[ERRO] Entrada inválida! Preço e Estoque devem ser números.")
        return

    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor()

    try:
        sql = "INSERT INTO produtos (nome, categoria_id, descricao, preco, estoque) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, categoria_id, descricao, preco, estoque)
        cursor.execute(sql, valores)
        conexao.commit()
        print("\nProduto cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print(f"\nErro ao salvar produto: {err}")
    finally:
        cursor.close()
        conexao.close()

# Listagem do Catálogo de Produtos
def listar_produtos(pausa_no_final=False):
    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor()

    sql = """SELECT produtos.id, produtos.nome, categorias.nome, produtos.preco, produtos.estoque
             FROM produtos
             INNER JOIN categorias ON produtos.categoria_id = categorias.id"""
    cursor.execute(sql)
    produtos = cursor.fetchall()

    print("\n=== PRODUTOS DISPONÍVEIS ===")
    if not produtos:
        print("Nenhum produto cadastrado.")
    else:
        for p in produtos:
            status = verificar_estoque(p[4])
            print(f"ID: {p[0]} | {p[1]} ({p[2]}) - R${p[3]:.2f} | Estoque: {p[4]} [{status}]")

    cursor.close()
    conexao.close()
    
    if pausa_no_final:
        input("\nPressione Enter para voltar ao menu...")

# Exclusão de Produto do Sistema
def excluir_produto():
    try:
        id_produto = int(input("ID do produto a ser excluído: "))
    except ValueError:
        print("\n[ERRO] ID inválido.")
        return

    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor()

    sql = "DELETE FROM produtos WHERE id = %s"
    cursor.execute(sql, (id_produto,))
    conexao.commit()
    print("\nProduto removido de sistema!")
    
    cursor.close()
    conexao.close()

# Edição de Dados do Produto
def editar_produto():
    listar_produtos()
    
    try:
        id_produto = int(input("\nDigite o ID do produto que deseja editar: "))
    except ValueError:
        print("[ERRO] ID inválido! Digite apenas números.")
        input("\nPressione Enter para voltar...")
        return

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
    produto = cursor.fetchone()

    if not produto:
        print("[ERRO] Produto não encontrado!")
        cursor.close()
        conexao.close()
        input("\nPressione Enter para voltar...")
        return

    print(f"\n--- EDITANDO: {produto['nome']} ---")
    print("(Pressione ENTER sem digitar nada para MANTER o valor atual)")

    novo_nome = input(f"Nome atual [{produto['nome']}]: ")
    if novo_nome.strip() == "":
        novo_nome = produto['nome']

    nova_descricao = input(f"Descrição atual [{produto['descricao']}]: ")
    if nova_descricao.strip() == "":
        nova_descricao = produto['descricao']

    novo_preco_input = input(f"Preço atual [R${produto['preco']:.2f}]: ")
    if novo_preco_input.strip() == "":
        novo_preco = float(produto['preco'])
    else:
        try:
            novo_preco = float(novo_preco_input)
        except ValueError:
            print("[ERRO] Preço inválido! Mantendo o valor anterior.")
            novo_preco = float(produto['preco'])

    novo_estoque_input = input(f"Estoque atual [{produto['estoque']}]: ")
    if novo_estoque_input.strip() == "":
        novo_estoque = int(produto['estoque'])
    else:
        try:
            novo_estoque = int(novo_estoque_input)
        except ValueError:
            print("[ERRO] Quantidade inválida! Mantendo o valor anterior.")
            novo_estoque = int(produto['estoque'])

    sql = """UPDATE produtos 
             SET nome = %s, descricao = %s, preco = %s, estoque = %s 
             WHERE id = %s"""
    valores = (novo_nome, nova_descricao, novo_preco, novo_estoque, id_produto)

    cursor.execute(sql, valores)
    conexao.commit()
    
    print("\n✅ Produto atualizado com sucesso!")
    
    cursor.close()
    conexao.close()
    input("\nPressione Enter para voltar ao menu...")

# Verificação do Status de Estoque
def verificar_estoque(estoque):
    if estoque <= 0:
        return "Produto sem estoque!"
    elif estoque <= 5:
        return "Estoque baixo!"
    else:
        return "Produto disponível!"

carrinho = []

# Adição de Item ao Carrinho
def adicionar_carrinho():
    listar_produtos(pausa_no_final=False)

    print("\n-----------------------------")
    try:
        id_produto = int(input("Digite o ID do produto que deseja: "))
        quantidade = int(input("Quantidade: "))
        if quantidade <= 0:
            print("[ERRO] A quantidade deve ser maior que zero.")
            return
    except ValueError:
        print("\n[ERRO] Você deve digitar apenas números inteiros!")
        return

    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not produto:
        print("\n[ERRO] Produto não encontrado.")
        return
        
    if produto['estoque'] < quantidade:
        print(f"\n[ERRO] Estoque insuficiente! Disponível apenas: {produto['estoque']}")
        return

    for item in carrinho:
        if item["id"] == id_produto:
            if (item["quantidade"] + quantidade) > produto['estoque']:
                print(f"\n[ERRO] A soma excede o estoque disponível ({produto['estoque']}).")
                return
            item["quantidade"] += quantidade
            print(f"\nQuantidade de '{produto['nome']}' atualizada no carrinho!")
            return

    item = {
        "id": produto["id"],
        "nome": produto["nome"],
        "preco": float(produto["preco"]),
        "quantidade": quantidade
    }
    carrinho.append(item)
    print(f"\n'{produto['nome']}' adicionado ao carrinho!")

# Exibição do Carrinho de Compras
def visualizar_carrinho(pausa_no_final=True):
    if not carrinho:
        print("\nSeu carrinho está vazio.")
        if pausa_no_final: input("\nPressione Enter para voltar...")
        return False
    
    total = 0
    print("\n=== SEU CARRINHO ===")
    for item in carrinho:
        subtotal = item["preco"] * item["quantidade"]
        print(f"ID: {item['id']} | {item['nome']} - {item['quantidade']}x - R${subtotal:.2f}")
        total += subtotal
    print(f"-----------------------------")
    print(f"TOTAL DO CARRINHO: R${total:.2f}")
    
    if pausa_no_final:
        input("\nPressione Enter para voltar ao menu...")
    return True

# Remoção de Item do Carrinho
def remover_do_carrinho():
    carrinho_com_itens = visualizar_carrinho(pausa_no_final=False)
    if not carrinho_com_itens:
        return
    
    try:
        id_remover = int(input("\nDigite o ID do produto que deseja remover: "))
    except ValueError:
        print("\n[ERRO] Entrada inválida! Por favor, digite um número válido.")
        return

    for item in carrinho:
        if item["id"] == id_remover:
            carrinho.remove(item)
            print(f"\nProduto '{item['nome']}' removido com sucesso!")
            return 
            
    print("\n[ERRO] Produto não encontrado no seu carrinho.")

# Checkout e Finalização de Compra
def finalizar_pedido(usuario_logado):
    if usuario_logado is None:
        print("\n[ERRO] Faça login primeiro para finalizar a compra!")
        input("\nPressione Enter para continuar...")
        return
    if not carrinho:
        print("\n[ERRO] Seu carrinho está vazio!")
        input("\nPressione Enter para continuar...")
        return
    
    conexao = conectar()
    if not conexao: return
    cursor = conexao.cursor(dictionary=True)

    print("\n=== DADOS DE ENTREGA ===")
    rua = input("Rua/Av: ")
    cep = input("CEP (Apenas 8 números): ")
    complemento = input("Complemento: ")

    try:
        for item in carrinho:
            cursor.execute("SELECT estoque FROM produtos WHERE id = %s", (item["id"],))
            prod_banco = cursor.fetchone()
            if prod_banco["estoque"] < item["quantidade"]:
                print(f"\n[CRÍTICO] O produto '{item['nome']}' acabou de esgotar no estoque. Pedido cancelado.")
                return

        total = sum(item["preco"] * item["quantidade"] for item in carrinho) 

        sql_pedido = "INSERT INTO pedidos (usuario_id, total, rua, cep, complemento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_pedido, (usuario_logado["id"], total, rua, cep, complemento))
        pedido_id = cursor.lastrowid    

        for item in carrinho:
            subtotal = item["preco"] * item["quantidade"]

            sql_item = "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, subtotal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_item, (pedido_id, item["id"], item["quantidade"], subtotal))

            sql_estoque = "UPDATE produtos SET estoque = estoque - %s WHERE id = %s"
            cursor.execute(sql_estoque, (item["quantidade"], item["id"]))

        conexao.commit()
        print(f"\n🎉 Pedido #{pedido_id} finalizado com sucesso! Total: R${total:.2f}")
        carrinho.clear()
        
    except mysql.connector.Error as err:
        print(f"\n[ERRO] Falha ao processar pedido no banco: {err}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()
        input("\nPressione Enter para voltar ao menu...")

# Menu do Painel Administrativo
def painel_admin(usuario_logado):
    if usuario_logado is None:
        print("Faça login!")
        input("\nPressione Enter para voltar...")
        return

    if usuario_logado["tipo"] != "admin":
        print("Acesso negado!")
        input("\nPressione Enter para voltar...")
        return
        
    while True:
        print("\n=== PAINEL ADMIN ===")
        print("1 - Cadastrar Produto")
        print("2 - Listar Produtos")
        print("3 - Excluir Produto")
        print("4 - Editar Produto")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            excluir_produto()
        elif opcao == "4":
            editar_produto()
        elif opcao == "0":
            break 
        else:
            print("Opção inválida!")

usuario_logado = None

# Loop do Menu Principal do Sistema
while True:
    status_login = f"Logado como: {usuario_logado['nome']} ({usuario_logado['tipo']})" if usuario_logado else "Não logado"
    
    print(f"\n==== LUME BOUTIQUE ==== [{status_login}]")
    print("1 - Cadastrar usuário")
    print("2 - Fazer login")
    print("3 - Listar produtos")
    print("4 - Adicionar ao carrinho")
    print("5 - Visualizar carrinho")
    print("6 - Remover do carrinho")
    print("7 - Finalizar pedido")
    print("8 - Painel administrador")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        usuario_logado = login()
    elif opcao == "3":
        listar_produtos(pausa_no_final=True)
    elif opcao == "4":
        adicionar_carrinho()
    elif opcao == "5":
        visualizar_carrinho(pausa_no_final=True)
    elif opcao == "6":
        remover_do_carrinho()
    elif opcao == "7":
        finalizar_pedido(usuario_logado)
    elif opcao == "8":
        painel_admin(usuario_logado)
    elif opcao == "0":
        print("\nSistema Lume Boutique encerrado. Até logo!")
        break
    else:
        print("\nOpção inválida! Tente novamente.")