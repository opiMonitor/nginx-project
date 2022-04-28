from pprint import pprint
from pyzabbix.api import ZabbixAPI
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@postgres:5432/postgres')
Base = declarative_base()


class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __repr__(self):
        return "<Url(id='{}', url='{}')>".format(self.id, self.url)


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

    try:
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        s = Session()
        rows = s.query(Url).count()

        for link in web_links_list:
            data_url = Url(url=link)
            host_exist = s.query(Url).filter_by(url=data_url.url).first()
            if host_exist is None:  # if the current host do not exists do this:
                try:
                    s.add(data_url)
                    s.commit()
                    print(
                        f"\033[1;32m [OK] NEW URL ADDED: ' + '\x1b[0m: id({data_url.id}), url: {data_url.url}")

                except:
                    s.rollback()
                    print(f"exception: {data_url.id} and url: {data_url.url}")
                    raise

                finally:
                    print(f"finally: {data_url.id} and url: {data_url.url}")

        rows2 = s.query(Url).count()
        print(f" ADDED: {rows2-rows} ROWS")
        s.close()

    except (Exception) as error:
        print('\033[95m add web scenarios to database ERROR:' + '\x1b[0m')
        print(error)

    finally:
        s.close()


if __name__ == '__main__':
    connect()
