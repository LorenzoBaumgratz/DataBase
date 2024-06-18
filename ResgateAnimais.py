import psycopg2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#CHECK (`porte` in ('Pequeno','Médio', 'Grande'))
#PRIMARY KEY(`data_resgate`,`cod_animal`,`id_local`),
# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {'USUARIO': (
    """CREATE TABLE USUARIO (
      userId integer PRIMARY KEY NOT NULL,
      name varchar(100) NOT NULL,
      email varchar(100) NOT NULL,
      password varchar(100) NOT NULL
    ) """),
    'SESSAO': (
        """CREATE TABLE SESSAO (
            token varchar(50) PRIMARY KEY NOT NULL,
            userId integer NOT NULL,  
            FOREIGN KEY(userId) REFERENCES USUARIO (userId)
        ) """),
    'CIDADE': (
        """CREATE TABLE CIDADE (
        cityId integer PRIMARY KEY NOT NULL,
        city_name varchar(150) NOT NULL
        ) """),    
    'EVENTO': (
        """CREATE TABLE EVENTO (
        eventoId integer PRIMARY KEY NOT NULL,
        cityId integer NOT NULL,
        nome_evento varchar(150) NOT NULL,
        data_inicio timestamp NOT NULL,
        data_fim timestamp NOT NULL,
        FOREIGN KEY(cityId) REFERENCES CIDADE (cityId)
        ) """),
    'COMENTARIO_EVENTO': (
        """CREATE TABLE COMENTARIO_EVENTO (
        comentario_e_Id integer PRIMARY KEY NOT NULL,
        eventoId integer NOT NULL,
        userId integer NOT NULL,
        rating float NOT NULL,
        descricao varchar(150) NOT NULL,
        data timestamp NOT NULL,
        FOREIGN KEY(eventoId) REFERENCES EVENTO (eventoId),
        FOREIGN KEY(userId) REFERENCES USUARIO (userId)
        ) """),
    'HOTEL': (
        """CREATE TABLE HOTEL (
        hotelId integer PRIMARY KEY NOT NULL,
        hotel_name varchar(150) NOT NULL,
        price float NOT NULL,
        cityId integer NOT NULL,
        FOREIGN KEY(cityId) REFERENCES CIDADE (cityId)
        ) """),
    'COMENTARIO_HOTEL': (
        """CREATE TABLE COMENTARIO_HOTEL (
        comentario_h_Id integer PRIMARY KEY NOT NULL,
        hotelId integer NOT NULL,
        userId integer NOT NULL,
        rating float NOT NULL,
        descricao varchar(150) NOT NULL,
        data timestamp NOT NULL,
        FOREIGN KEY(hotelId) REFERENCES HOTEL (hotelId),
        FOREIGN KEY(userId) REFERENCES USUARIO (userId)
        ) """),    
    'IMAGEM': (
        """CREATE TABLE IMAGEM (
        imgId integer PRIMARY KEY NOT NULL,
        url varchar(150) NOT NULL,
        cityId integer ,
        hotelId integer ,
        FOREIGN KEY(cityId) REFERENCES CIDADE (cityId),
        FOREIGN KEY(hotelId) REFERENCES HOTEL (hotelId)
        ) """),
    'AREA': (
        """CREATE TABLE AREA (
        areaId integer PRIMARY KEY NOT NULL,
        hotelId integer NOT NULL,
        tipo text NOT NULL,
        FOREIGN KEY(hotelId) REFERENCES HOTEL (hotelId)
        ) """),
    'TIPO_PASSAGEM': (
        """CREATE TABLE TIPO_PASSAGEM (
        tipoId integer PRIMARY KEY NOT NULL,
        tipo_nome varchar(150) NOT NULL,
        descricao text NOT NULL,
        CHECK (tipo_nome in ('Executiva','PrimeiraClasse', 'Padrao'))
        ) """),
    'EMPRESA': (
        """CREATE TABLE EMPRESA (
        airlineId integer PRIMARY KEY NOT NULL,
        airline_name varchar(150) NOT NULL
        ) """),
    'PASSAGEM': (
        """CREATE TABLE PASSAGEM (
        passagemId integer PRIMARY KEY NOT NULL,
        cidade_origem integer NOT NULL,
        cidade_destino integer NOT NULL,
        tipoId integer NOT NULL,
        airlineId integer NOT NULL,
        FOREIGN KEY(cidade_origem ) REFERENCES CIDADE (cityId),
        FOREIGN KEY(cidade_destino) REFERENCES CIDADE (cityId),
        FOREIGN KEY(tipoId) REFERENCES TIPO_PASSAGEM (tipoId),
        FOREIGN KEY(airlineId) REFERENCES EMPRESA (airlineId)
        ) """)
}

# Valores para serem inseridos no Banco de Dados
inserts = {'USUARIO': ("""
        INSERT INTO USUARIO (userId, name, email, password) VALUES 
        (1,'Lorenzo', 'lorenzo@example.com', 'password123'),
        (2,'Maria', 'maria@example.com', 'password456'),
        (3,'João', 'joao@example.com', 'password789'),
        (4, 'Ana Paula', 'ana.paula@example.com', 'senha123'),
        (5, 'Carlos Alberto', 'carlos.alberto@example.com', 'senha456'),
        (6, 'Mariana Souza', 'mariana.souza@example.com', 'senha789'),
        (7, 'Pedro Henrique', 'pedro.henrique@example.com', 'senha101'),
        (8, 'Julia Santos', 'julia.santos@example.com', 'senha202')                                    
    """),
    'CIDADE': (
        """
        INSERT INTO CIDADE (cityId,city_name) VALUES 
        (1,'São Paulo'),
        (2,'Rio de Janeiro'),
        (3,'Belo Horizonte'),
        (4, 'Curitiba'),
        (5, 'Porto Alegre'),
        (6, 'Salvador'),
        (7, 'Brasília'),
        (8, 'Recife')
    """),
    'EVENTO': (
        """
        INSERT INTO EVENTO (eventoId, cityId, nome_evento, data_inicio, data_fim) VALUES 
        (1,1, 'Festival de Música', '2024-06-15 18:00:00', '2024-06-16 23:59:59'),
        (2,2, 'Feira de Tecnologia', '2024-07-20 09:00:00', '2024-07-22 18:00:00'),
        (3,3, 'Congresso de Ciências', '2024-08-10 10:00:00', '2024-08-12 17:00:00'),
        (4, 4, 'Maratona de Curitiba', '2024-09-10 07:00:00', '2024-09-10 12:00:00'),
        (5, 5, 'Festival de Cinema de Porto Alegre', '2024-10-05 18:00:00', '2024-10-10 23:59:59'),
        (6, 6, 'Carnaval de Salvador', '2024-02-25 15:00:00', '2024-02-29 23:59:59'),
        (7, 7, 'Festa Nacional de Brasília', '2024-11-15 09:00:00', '2024-11-20 23:59:59'),
        (8, 8, 'Festival de Música de Recife', '2024-12-10 18:00:00', '2024-12-15 23:59:59')
    """),
    'HOTEL': (
        """
        INSERT INTO HOTEL (hotelId,hotel_name, price, cityId) VALUES 
        (1,'Hotel São Paulo', 300.00, 1),
        (2,'Hotel Rio', 250.00, 2),
        (3,'Hotel BH', 200.00, 3),
        (4, 'Hotel Curitiba', 350.00, 4),
        (5, 'Hotel Porto Alegre', 280.00, 5),
        (6, 'Hotel Salvador', 300.00, 6),
        (7, 'Hotel Brasília', 320.00, 7),
        (8, 'Hotel Recife', 290.00, 8)
    """),
    'IMAGEM': (
        """
        INSERT INTO IMAGEM (imgId,url, cityId, hotelId) VALUES 
        (1,'http://example.com/img1.jpg', 1, NULL),
        (2, 'http://example.com/img2.jpg', NULL, 2),
        (3, 'http://example.com/img3.jpg', 3, NULL)
    """),
    'AREA': (
        """
        INSERT INTO AREA (areaId, hotelId, tipo) VALUES 
        (1,1, 'Piscina'),
        (2,2, 'Academia'),
        (3,3, 'Restaurante')
    """),
    'TIPO_PASSAGEM': (
        """
        INSERT INTO TIPO_PASSAGEM (tipoId,tipo_nome, descricao) VALUES 
        (1,'Executiva', 'Assento confortável com mais espaço e serviços premium'),
        (2, 'PrimeiraClasse', 'Serviço de luxo com todas as comodidades'),
        (3, 'Padrao', 'Assento padrão com serviços básicos')
    """),
    'EMPRESA': (
        """
        INSERT INTO EMPRESA (airlineId, airline_name) VALUES 
        (1,'Airline A'),
        (2,'Airline B'),
        (3,'Airline C'),
        (4, 'Airline D'),
        (5, 'Airline E'),
        (6, 'Airline F')
    """),
    'PASSAGEM': (
        """
        INSERT INTO PASSAGEM (passagemId,cidade_origem , cidade_destino, tipoId, airlineId) VALUES 
        (1,1, 2, 1, 1),
        (2,2, 3, 2, 2),
        (3,3, 1, 3, 3),
        (4, 1, 4, 1, 1),
        (5, 2, 5, 2, 2),
        (6, 3, 6, 3, 3),
        (7, 4, 7, 1, 1),
        (8, 5, 8, 2, 2)
    """),
    'COMENTARIO_EVENTO': (
        """
        INSERT INTO COMENTARIO_EVENTO (comentario_e_Id, eventoId, userId, rating, descricao, data) VALUES 
        (1,1, 1, 4.5, 'Evento maravilhoso!', '2024-06-16 12:00:00'),
        (2,2, 2, 3.8, 'Muito interessante, mas poderia ter mais stands.', '2024-07-21 14:00:00'),
        (3,3, 3, 4.2, 'Ótimas palestras!', '2024-08-11 16:00:00'),
        (4, 4, 4, 5.0, 'Evento muito bem organizado e animado!', '2024-09-10 13:00:00'),
        (5, 5, 5, 4.0, 'Ótimos filmes e organização impecável.', '2024-10-11 12:00:00'),
        (6, 6, 6, 4.5, 'Carnaval incrível, muita alegria e segurança.', '2024-03-01 10:00:00'),
        (7, 7, 7, 4.8, 'Evento maravilhoso com muitas atrações.', '2024-11-21 15:00:00'),
        (8, 8, 8, 4.7, 'Festival de música com bandas incríveis.', '2024-12-16 12:00:00'),
        (9, 4, 5, 4.5, 'Curitiba sempre oferece bons eventos!', '2024-09-10 14:00:00'),
        (10, 5, 6, 4.2, 'Muito interessante, mas poderia ter mais stands.', '2024-10-12 11:00:00')
    """),
    'COMENTARIO_HOTEL': (
        """
        INSERT INTO COMENTARIO_HOTEL (comentario_h_Id, hotelId, userId, rating, descricao, data) VALUES 
        (1,1, 1, 4.0, 'Ótimo hotel com excelente serviço.', '2024-06-17 10:00:00'),
        (2,2, 2, 3.5, 'Bom hotel, mas poderia ser mais limpo.', '2024-07-23 12:30:00'),
        (3,3, 3, 5.0, 'Experiência incrível! Recomendo.', '2024-08-13 14:00:00'),
        (4, 4, 4, 4.7, 'Excelente hotel com ótima localização.', '2024-09-11 09:00:00'),
        (5, 5, 5, 4.2, 'Bom hotel, mas o café da manhã poderia ser melhor.', '2024-10-12 08:00:00'),
        (6, 6, 6, 4.8, 'Ótima estadia durante o carnaval.', '2024-03-02 11:00:00'),
        (7, 7, 7, 4.6, 'Hotel com excelente serviço e conforto.', '2024-11-22 10:00:00'),
        (8, 8, 8, 4.5, 'Bom hotel, mas um pouco caro.', '2024-12-17 09:00:00'),
        (9, 4, 5, 4.3, 'Localização perfeita e quartos confortáveis.', '2024-09-12 08:30:00'),
        (10, 5, 6, 4.0, 'Bom custo-benefício.', '2024-10-13 10:00:00')
    """)
}

# Valores para deletar as tabelas
drop = {
    'COMENTARIO_HOTEL': (
    "drop table COMENTARIO_HOTEL"),
    'COMENTARIO_EVENTO': (
        "drop table COMENTARIO_EVENTO"),
    'PASSAGEM': (
        "drop table PASSAGEM"),
    'EMPRESA': (
        "drop table EMPRESA"),
    'TIPO_PASSAGEM': (
        "drop table TIPO_PASSAGEM"),
    'AREA': (
        "drop table AREA"),
    'IMAGEM': (
        "drop table IMAGEM"),
    'HOTEL': (
        "drop table HOTEL"),
    'EVENTO': (
        "drop table EVENTO"),
    'SESSAO': (
        "drop table SESSAO"),
    'CIDADE': (
        "drop table CIDADE"),
    'USUARIO': (
        "drop table USUARIO")
}

# Valores para teste de update
update = {
    'USUARIO': (
        """UPDATE USUARIO
        SET name = 'Lorenzo Silva',
        email = 'lorenzo.silva@example.com'
        WHERE userId = 1"""
    ),
    'SESSAO': (
        """UPDATE SESSAO
        SET token = 'new_token_value'
        WHERE userId = 1"""
    ),
    'CIDADE': (
        """UPDATE CIDADE
        SET city_name = 'São Paulo Atualizado'
        WHERE cityId = 1"""
    ),
    'EVENTO': (
        """UPDATE EVENTO
        SET nome_evento = 'Festival de Música Atualizado',
        data_fim = '2024-06-17 23:59:59'
        WHERE eventoId = 1"""
    ),
    'COMENTARIO_EVENTO': (
        """UPDATE COMENTARIO_EVENTO
        SET rating = 4.8,
        descricao = 'Evento maravilhoso! Atualizado.'
        WHERE comentario_e_Id = 1"""
    ),
    'HOTEL': (
        """UPDATE HOTEL
        SET price = 350.00
        WHERE hotelId = 1"""
    ),
    'IMAGEM': (
        """UPDATE IMAGEM
        SET url = 'http://example.com/updated_img1.jpg'
        WHERE imgId = 1"""
    ),
    'AREA': (
        """UPDATE AREA
        SET tipo = 'Piscina Atualizada'
        WHERE areaId = 1"""
    ),
    'TIPO_PASSAGEM': (
        """UPDATE TIPO_PASSAGEM
        SET descricao = 'Assento confortável atualizado com mais espaço e serviços premium'
        WHERE tipoId = 1"""
    ),
    'EMPRESA': (
        """UPDATE EMPRESA
        SET airline_name = 'Airline A Atualizada'
        WHERE airlineId = 1"""
    ),
    'PASSAGEM': (
        """UPDATE PASSAGEM
        SET tipoId = 2
        WHERE passagemId = 1"""
    ),
    'COMENTARIO_HOTEL': (
        """UPDATE COMENTARIO_HOTEL
        SET rating = 4.5,
        descricao = 'Ótimo hotel com excelente serviço. Atualizado.'
        WHERE comentario_h_Id = 1"""
    )
}

# Valores para teste de delete
delete = {
    'COMENTARIO_HOTEL': (
        """DELETE FROM COMENTARIO_HOTEL
        WHERE comentario_h_Id = 1"""
    ),
    'COMENTARIO_EVENTO': (
        """DELETE FROM COMENTARIO_EVENTO
        WHERE comentario_e_Id = 1"""
    ),
    'PASSAGEM': (
        """DELETE FROM PASSAGEM
        WHERE passagemId = 1 OR passagemId=3 OR passagemId=4 OR passagemId=7"""
    ),
    'EMPRESA': (
        """DELETE FROM EMPRESA
        WHERE airlineId = 1 """
    ),
    'TIPO_PASSAGEM': (
        """DELETE FROM TIPO_PASSAGEM
        WHERE tipoId = 1 """
    ),
    'AREA': (
        """DELETE FROM AREA
        WHERE areaId = 1 """
    ),
    'IMAGEM': (
        """DELETE FROM IMAGEM
        WHERE imgId = 1 """
    ),
    'HOTEL': (
        """DELETE FROM HOTEL
        WHERE hotelId = 1"""
    ),
    'EVENTO': (
        """DELETE FROM EVENTO
        WHERE eventoId = 1"""
    ),
    'SESSAO': (
        """DELETE FROM SESSAO
        WHERE token = 'token1'"""
    ),
    'CIDADE': (
        """DELETE FROM CIDADE
        WHERE cityId = 1 """
    ),
    'USUARIO': (
        """DELETE FROM USUARIO
        WHERE userId = 1"""
    )
}


# Funções
def connect_TrabalhoNota10():
    cnx = psycopg2.connect(host='localhost', database='bd', user='postgres', password='macacoLH04')
    cnx.autocommit
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Deletando {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuido: ")
        codigo_f = input("Digite a variavel primaria: ")
        codigo = input("Digite o codigo numerico: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
        cursor.execute(sql)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    SELECT evento.eventoId, evento.nome_evento, evento.city_name, evento.total_comentarios
    FROM (
        SELECT 
            e.eventoId,
            e.nome_evento,
            c.city_name,
            COUNT(ce.comentario_e_Id) AS total_comentarios
        FROM 
            EVENTO e
        JOIN 
            COMENTARIO_EVENTO ce ON e.eventoId = ce.eventoId
        JOIN 
            CIDADE c ON e.cityId = c.cityId
        WHERE e.data_inicio >= '2024-01-01' -- Filtra eventos começando a partir de 2024
        GROUP BY 
            e.eventoId, e.nome_evento, c.city_name
    ) AS evento
    """
    print("Primeira Consulta: Número de Comentários por Evento"
          "Esta consulta visa sumarizar o número de comentários feitos em cada evento, "
          "exibindo o ID do evento, o nome do evento, o nome da cidade e o total de comentários.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    return myresult


def consulta2(connect):
    select_query = """
    SELECT avaliacao.city_name, avaliacao.hotel_name, avaliacao.media_avaliacao
    FROM (
        SELECT 
            c.city_name,
            h.hotel_name,
            AVG(ch.rating) AS media_avaliacao
        FROM 
            HOTEL h
        JOIN 
            CIDADE c ON h.cityId = c.cityId
        JOIN 
            COMENTARIO_HOTEL ch ON h.hotelId = ch.hotelId
        WHERE h.price > 200.00 -- Filtra hotéis com preço maior que 200
        GROUP BY 
            c.city_name, h.hotel_name
    ) AS avaliacao
    """
    print("\nSegunda Consulta: Média de Avaliação dos Hotéis por Cidade "
          "Esta consulta tem como objetivo calcular a média de avaliação dos hotéis em cada cidade, "
          "exibindo o nome da cidade, o nome do hotel e a média de avaliação.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    return myresult

def consulta3(connect):
    select_query = """
    SELECT eventos_usuarios.city_name, eventos_usuarios.total_eventos, eventos_usuarios.total_usuarios
    FROM (
        SELECT 
            c.city_name,
            COUNT(DISTINCT e.eventoId) AS total_eventos,
            COUNT(DISTINCT ce.userId) AS total_usuarios
        FROM 
            CIDADE c
        JOIN 
            EVENTO e ON c.cityId = e.cityId
        JOIN 
            COMENTARIO_EVENTO ce ON e.eventoId = ce.eventoId
        WHERE e.data_inicio >= '2024-01-01' -- Filtra eventos começando a partir de 2024
        GROUP BY 
            c.city_name
    ) AS eventos_usuarios
    """
    print("\nTerceira Consulta: Total de Eventos por Cidade e Usuários Envolvidos."
          "Esta consulta tem como objetivo calcular o número total de eventos realizados em cada cidade e "
          "contar o número de usuários que comentaram em eventos dessas cidades, "
          "exibindo o nome da cidade, o número total de eventos e o número de usuários distintos que comentaram.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    return myresult

def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão ao Postgres foi encerrada")


def plot_graph1(data):
    if not data:
        print("No data to plot.")
        return
    
    event_names = [row[2] for row in data]
    total_comments = [row[3] for row in data]
    plt.figure(figsize=(10, 6))
    plt.bar(event_names, total_comments, color='skyblue')
    plt.xlabel('Event Name')
    plt.ylabel('Total Comments')
    plt.title('Number of Comments per Event')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_graph2(data):
    
    city_names = [row[0] for row in data]
    hotel_names = [row[1] for row in data]
    avg_ratings = [row[2] for row in data]

    
    plt.figure(figsize=(10, 6))
    plt.bar(hotel_names, avg_ratings, color='green')
    plt.xlabel('Hotel Name')
    plt.ylabel('Average Rating')
    plt.title('Average Rating of Hotels by City')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_graph3(data):
    
    city_names = [row[0] for row in data]
    total_events = [row[1] for row in data]
    total_users = [row[2] for row in data]

    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('City Name')
    ax1.set_ylabel('Total Events', color=color)
    ax1.bar(city_names, total_events, color=color, alpha=0.6, label='Total Events')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Total Users', color=color)
    ax2.plot(city_names, total_users, color=color, marker='o', linestyle='-', linewidth=2, label='Total Users')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # ajustar para layout claro
    plt.title('Total Events and Users by City')
    plt.show()

def crud_TrabalhoNota10(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)

    

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)

    data1 = consulta1(connect)
    if data1:
        plot_graph1(data1)
    data2 = consulta2(connect)
    if data2:
        plot_graph2(data2)
    data3 = consulta3(connect)
    if data3:
        plot_graph3(data3)



# Main
try:
    # Estabelece Conexão com o DB
    con = connect_TrabalhoNota10()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD TrabalhoNota10
        2.  TEST - Create all tables
        3.  TEST - Insert all values
        4.  TEST - Update
        5.  TEST - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        10. Show Table
        11. Update Value
        12. CLEAR ALL TrabalhoNota10
        0.  Disconnect DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 12:
            print("Erro tente novamente")
            choice = int(input())

        if choice == 0:
                break

        if choice == 1:
            crud_TrabalhoNota10(con)

        if choice == 2:
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:

            data1 = consulta1(con)
            if data1:
                plot_graph1(data1)

        if choice == 7:

            data2 = consulta2(con)
            if data2:
                plot_graph2(data2)

        if choice == 8:

            data3 = consulta3(con)
            if data3:
                plot_graph3(data3)

        if choice == 9:
            break

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

except (psycopg2.DatabaseError, Exception) as error:
            print(error)
