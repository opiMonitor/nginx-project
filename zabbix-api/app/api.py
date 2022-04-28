from pprint import pprint
from pyzabbix.api import ZabbixAPI
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json


def connect():

    # Create ZabbixAPI class instance
    zapi = ZabbixAPI(url='http://10.20.50.57/zabbix/', user='tv-monitor', password='monitor1')

    web_links = zapi.do_request('trigger.get',
                                {
                                    'filter': {'hostid': 11195,
                                               'status': 0},
                                    'output': ['description']
                                })
    # convert to list
    web_links_list = []
    for web in web_links['result']:
        web_links_list.append(web['description'])

    # print OK
    print('\033[1;32m [OK] API GET 200!' + '\x1b[0m')

    # API logout
    zapi.user.logout()

    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        print('\nx) Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="postgres",
            dbname="postgres",
            user="postgres",
            password="postgres")

        cur = conn.cursor()
        print('\033[1;32m [OK] Connected!' + '\x1b[0m')

        # check if table exists / create table
        table_name = 'web'
        cur.execute("select * from information_schema.tables where table_name=%s", (table_name,))
        if(bool(cur.rowcount)):
            print(f'table_name "{table_name}" exists. aborting creation.')
        else:
            print(f'table_name "{table_name}" was not existed. creation...')
            try:
                cur.execute(sql.SQL("CREATE TABLE {table} ( \
                            link_id SERIAL PRIMARY KEY, \
                            url VARCHAR(255) NOT NULL \
                            )").format(table=sql.Identifier(table_name)))
                conn.commit()
                print('\033[1;32m [NEW TABLE] table Created!' + '\x1b[0m')
            except (Exception, psycopg2.DatabaseError) as error:
                print('\033[95m check if table exists / create table ERROR:' + '\x1b[0m')
                print(error)

        # add web scenarios to database
        try:
            for link in web_links_list:
                # cur.execute("INSERT INTO {table} (url) VALUES web=%s").format(table=sql.Identifier(table_name)), resulten)
                cur.execute(sql.SQL("""INSERT INTO {table} (url) \
                VALUES (%s);""").format(table=sql.Identifier(table_name)),
                            [link])

            conn.commit()
            print('\033[1;32m [OK] add web scenarios to database Created!' + '\x1b[0m')
        except (Exception, psycopg2.DatabaseError) as error:
            print('\033[95m add web scenarios to database ERROR:' + '\x1b[0m')
            print(error)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print('\033[95m Connecting to the PostgreSQL database ERROR:' + '\x1b[0m')
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('\n xxxxxxx Database connection closed xxxxxxx')


if __name__ == '__main__':
    connect()
