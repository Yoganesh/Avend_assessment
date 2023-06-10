import requests
import schedule
import time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine("mysql://avend:secret@172.17.0.1:3306/avend_db")


Base = declarative_base()


class Scrap(Base):
    __tablename__ = 'scrap_data'
    id = Column(Integer, primary_key=True)
    dealDate = Column(String(10))
    securityCode = Column(String(10))
    securityName = Column(String(20))
    clientName = Column(String(50))
    dealType = Column(String(1))
    quantity = Column(String(10))
    price = Column(String(10))


Base.metadata.create_all(engine)


def bse_india_scrap(url):
    print("##### Job Running #####")
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
    r = requests.get(url, headers=header)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.findAll("tr", {"class": "tdcolumn"})
    session = Session(bind=engine, expire_on_commit=False)

    for link in data:
        table_data = link.findAll("td", {"class": "tdcolumn"})
        sam = [x.text for x in table_data]
        secName = link.find("td", {"class": "TTRow_left"}).text
        print(sam)
        scrapdb = Scrap(dealDate=sam[0], securityCode=sam[1], securityName=secName, clientName=sam[2], dealType=sam[3], quantity=sam[4], price=sam[5])

        session.add(scrapdb)
        session.commit()

        id_1 = scrapdb.id

        print(f"created scrapped data with id {id_1}")

    session.close()


# For Automatic

schedule.every().day.at("09:00").do(bse_india_scrap, 'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx')

while True:
    schedule.run_pending()

# For Manual

# bse_india_scrap("https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx")
