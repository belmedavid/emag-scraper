import connection
from psycopg2 import sql


# queries for backend
@connection.connection_handler
def get_all_product_name(cursor, table):
    cursor.execute(sql.SQL("SELECT product_name FROM {};").format(sql.Identifier(table)))
    product_names = cursor.fetchall()
    return product_names


@connection.connection_handler
def get_all_checker_name(cursor):
    cursor.execute("SELECT name FROM checker;")
    checker_names = cursor.fetchall()
    return checker_names


@connection.connection_handler
def add_product_to_checker(cursor, name):
    cursor.execute("INSERT INTO checker values (%(name)s);", {'name': name})


@connection.connection_handler
def remove_product_from_checker(cursor, name):
    cursor.execute("DELETE FROM checker WHERE name = %(name)s;", {'name': name})


@connection.connection_handler
def get_quantity_by_name(cursor, table, name):
    cursor.execute(
        sql.SQL("SELECT quantity FROM {} WHERE product_name = {};").format(sql.Identifier(table), sql.Literal(name)))
    quantity = cursor.fetchone()
    return quantity


@connection.connection_handler
def add_product_to_products(cursor, table, row):
    cursor.execute(sql.SQL("INSERT INTO {} values ({})").format(sql.Identifier(table),
                                                                sql.SQL(', ').join(map(sql.Literal, row))))


@connection.connection_handler
def update_product_quantity_by_name(cursor, table, name, price, latest_buy, update):
    cursor.execute(sql.SQL("""UPDATE {} 
                                  SET quantity = {}, latest_buy = {}, price = {}
                                  WHERE product_name = {};""").format(sql.Identifier(table),
                                                                      sql.Literal(update['quantity']),
                                                                      sql.Literal(latest_buy),
                                                                      sql.Literal(price),
                                                                      sql.Literal(name)))
    return None


# queries for frontend

@connection.connection_handler
def get_all_products(cursor, table):
    cursor.execute(sql.SQL("SELECT * from {};").format(sql.Identifier(table)))
    products = cursor.fetchall()
    return products


def get_order_by(order_by):
    base_order = 'latest_buy'
    if order_by != None:
        base_order = order_by
    return base_order


def get_order_direction(order_direction_string):
    order_direction = True
    if order_direction_string == 'desc':
        order_direction = False
    return order_direction


@connection.connection_handler
def get_ordered_products(cursor, table, order_by, order_direction):
    direction = 'asc' if order_direction else 'desc'
    cursor.execute(
        sql.SQL("SELECT * from {} ORDER BY {}" + direction).format(sql.Identifier(table), sql.Identifier(order_by),
                                                                   sql.Literal(order_direction)))
    ordered_products = cursor.fetchall()
    return ordered_products


@connection.connection_handler
def get_searched_product_names(cursor, table, search):
    cursor.execute(sql.SQL("SELECT * FROM {} WHERE LOWER(product_name) LIKE LOWER({});").format(sql.Identifier(table),
                                                                                         sql.Literal(search)))
    searched_products = cursor.fetchall()
    return searched_products


@connection.connection_handler
def get_table_names(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
    table_names = cursor.fetchall()
    return table_names


def get_table_name(table_name):
    base_table = '2018-11'
    if table_name != None:
        base_table = table_name
    return base_table
