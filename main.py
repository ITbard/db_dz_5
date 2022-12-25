import psycopg2


def createdb(conn):
    with conn.cursor() as cur:
        # cur.execute('''
        # Drop table Phone;
        # Drop table User_data;
        # ''')
        cur.execute('''
            create table if not exists User_data(
                id serial primary key,
                name varchar(60) not null,
                surname varchar(60) not null,
                email varchar(60) not null unique
            );
            ''')
        cur.execute('''
            create table if not exists Phone(
                id serial primary key,
                user_id integer not null references User_data(id),
                phone_number varchar(60) unique
            );
            ''')
        conn.commit
        return print('База данных создана')


def add_client(conn, first_name, last_name, email_, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
            insert into User_data (name, surname, email) values(%s, %s, %s) returning id;
            ''', (first_name, last_name, email_))
        id_ = cur.fetchone()
        for id_x in id_:
            id_x
        # id_x
        cur.execute('''
            insert into Phone (phone_number, user_id) values(%s, %s) returning user_id, phone_number;
            ''', (phones, id_x))
        cur.fetchall()
        conn.commit
        return print('Клиент добавлен')


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
            insert into Phone (phone_number, user_id) values(%s, %s) returning user_id, phone_number;
            ''', (phone, client_id))
        cur.fetchall()
        return print('Номер телефона добавлен')


def change_client(conn, client_id, first_name=None, last_name=None, email_=None, phones_id=None, phones=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('''
                update user_data set name=%s where id=%s;
                ''', (first_name, client_id))
            cur.execute('''
                select * from user_data;
                ''')
        if last_name != None:
            cur.execute('''
                update user_data set surname=%s where id=%s;
                ''', (last_name, client_id))
            cur.execute('''
                select * from user_data;
                ''')
        if email_ != None:
            cur.execute('''
                update user_data set email=%s where id=%s;
                ''', (email_, client_id))
            cur.execute('''
                select * from user_data;
                ''')
        if phones != None:
            cur.execute('''
                update phone set phone_number=%s where id=%s;
                ''', (phones, phones_id))
            cur.execute('''
                select * from user_data;
                ''')
        conn.commit
        return print('Данные изменены')


def delete_phone(conn, client_id, phone_):
    with conn.cursor() as cur:
        cur.execute('''
        delete from phone
        where user_id=%s and phone_number=%s;
        ''', (client_id, phone_))
        conn.commit
        return print('Телефон удален')


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        delete from phone
        where user_id=%s;
        ''', (client_id,))
        conn.commit
    with conn.cursor() as cur:
        cur.execute('''
        delete from user_data
        where id=%s;
        ''', (client_id,))
        conn.commit
        return ('Клиент удален')


def find_client_(conn, first_name=None, last_name=None, email_=None, phone_=None):
    with conn.cursor() as cur:
        if first_name != None and last_name != None or email_ != None:
            cur.execute('''
            select id, name, surname, email from user_data
            where name=%s and surname=%s
            or email=%s;
            ''', (first_name, last_name, email_))
            data_user = (cur.fetchone())
            cur.execute('''
            select phone_number from phone
            where user_id=%s;
            ''', (data_user[0],))
            phone_x = cur.fetchall()
            print(data_user, phone_x)
        elif phone_ != None:
            cur.execute('''
            select user_id from phone
            where phone_number=%s;
            ''', (phone_,))
            user_id_x = cur.fetchone()
            # print(user_id_x[0])
            cur.execute('''
            select id, name, surname, email from user_data
            where id=%s;
            ''', (user_id_x[0],))
            user_found = cur.fetchone()
            print(user_found, phone_)
            return None


def select_phone(conn):
    with conn.cursor() as cur:
        cur.execute('''
        select * from phone;
        ''')
        return cur.fetchall()


def select_user_data(conn):
    with conn.cursor() as cur:
        cur.execute('''
        select * from user_data;
        ''')
        return cur.fetchall()


with psycopg2.connect(database='clients_db', user='postgres', password='') as conn:
    # createdb(conn) # 1 DROP TABLE закомментирован

    # add_client(conn, 'Jack', 'Wolf', '1@net', '1001111') # 2 Почта - unique
    # add_client(conn, 'Vans', 'Black', '2@net', '2002222')
    # add_client(conn, 'Kate', 'Orange', '3@net', '3003333')
    #
    # add_phone(conn, 1, '1002222') # 3 Номер - unique

    # change_client(conn, 1, 'Jacky', 'asdf', '1231e', 6, '563463453') # 4

    # delete_phone(conn, 1, '1001111') # 5

    # delete_client(conn, 1) # 6

    # find_client_(conn, email_='3@net') # 7 если ввести не существующие данные, то будет ошибка
    #
    # print(select_phone(conn)) # вывести список телефонов
    # print(select_user_data(conn)) # вывести список клиентов(Имя, Фамилия, почта)

    conn.close

