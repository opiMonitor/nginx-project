from pprint import pprint
from pyzabbix.api import ZabbixAPI
import psycopg2

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://10.20.50.57/zabbix/', user='tv-monitor', password='monitor1')

web_links = zapi.do_request('trigger.get',
                            {
                                'filter': {'hostid': 11195,
                                           'status': 0},
                                'output': ['description']
                            })

for resulten in web_links['result']:
    print(resulten['description'])


zapi.user.logout()


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None

    # postgresql://username:password@host:port/database
    # 'postgresql://postgres:postgres@postgres:5432/postgres',

    try:
        print('\nx) Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="postgres",
            dbname="postgres",
            user="postgres",
            password="postgres")

        cur = conn.cursor()
        print('\033[1;32m [OK] Connected!' + '\x1b[0m')

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE web_links (
            link_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """)


if __name__ == '__main__':
    connect()
    print('koniec programu :)')
