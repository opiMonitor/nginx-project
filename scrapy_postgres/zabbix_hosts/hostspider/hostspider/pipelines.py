# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from hostspider.models import Host, db_connect, create_table


class SaveQuotesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        # tworzenie sesji połączeniowej pomiędzy psql
        session = self.Session()

        # for one_item in item:
        #     host.host = item["hosts"][one_item]
        #     host.ip = item["ips"][one_item]

        print("Enter for ")
        for x in range(0, len(item['hosts'])):
            print(f"\n\n---- index: {x}")

            # tworzenie instancji obiektu Host() czyli modelu naszej tabeli w bazie danych
            host = Host()

            # nadajemy wartości zmiennym dla naszej instancji klasy Host. nie dajemy .id gdyż to Primary key i nada się sam
            host.host = item["hosts"][x]
            host.ip = item["ips"][x]

            print(f"doing host: {host.host} and ip: {host.ip}")
            # check whether the host exists
            host_exist = session.query(Host).filter_by(host=host.host).first()
            print(f"host_exist: {host_exist}")
            if host_exist is None:  # if the current host do not exists do this:
                try:
                    session.add(host)
                    session.commit()
                    print(f"try: {host.host} and ip: {host.ip}")

                except:
                    session.rollback()
                    print(f"exception: {host.host} and ip: {host.ip}")
                    raise

                finally:
                    print(f"finally: {host.host} and ip: {host.ip}")

        session.close()
        return item
