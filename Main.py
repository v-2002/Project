from bs4 import BeautifulSoup
import xlwt
import time
from flask import Flask, render_template
from selenium import webdriver
import csv
import MySQLdb

app = Flask(__name__)

workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet("Information", cell_overwrite_ok=True)
sheet.write(0, 0, 'Name')
sheet.write(0, 1, 'Position')
sheet.write(0, 2, 'Cmpy_Name')
sheet.write(0, 3, 'Link')
line = 0

url = "https://www.naukri.com/hr-recruiters-consultants"

driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
driver.get(url)

time.sleep(10)
result = driver.page_source
spider = BeautifulSoup(result, 'html.parser')

divTag = spider.find_all("div", {"class": "vcard"})
for item in divTag:
    link = item.find("a").get('href')
    name = item.find("span", class_="fl ellipsis").get_text()
    position = item.find("span",class_="ellipsis clr").get_text()
    company = item.find("small", class_="ellipsis").get_text()

    sheet.write(line, 0, name)
    sheet.write(line, 1, position)
    sheet.write(line, 2, company)
    sheet.write(line, 3, link)
    line +=1

workbook.save("Scraped_data.csv")


try:
    connects = MySQLdb.connect(host='localhost',
                           user='root',
                           password='vikas',
                           db='mydb')
    cur = connects.cursor()
    cur.execute(
        'CREATE TABLE Scrapping_Data(Name varchar(20), Position varchar(25), Cmpy_Name varchar(15), Location varchar(10),Active varchar(10);')
    csv_file = open("Scraped_data.csv")
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        cur.execute('INSERT INTO Scrapping_Data(Names, \
                                 Position, Cmpy_Name, Location, Active )' \
                       'VALUES("%s", "%s", "%s","%s", "%s" )',
                       row)
    connects.commit()
    cur.close()
except:
    print("")

finally:
    #cur.close()
    print("Done!!")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/show_data')
def show_data():
    #return render_template('data_scrapped.html')
    try:
        connect = MySQLdb.connect(host='localhost',
                                  user='root',
                                  password='vikas',
                                  db='mydb')
        cur = connect.cursor()
        cur.execute("SELECT * FROM Scrapping_Data")
        info = cur.fetchall()
        return render_template('data_scrapped.html', data=info)

    finally:
        print("Nothing")


if __name__ == '__main__':
    app.run(debug=True)
