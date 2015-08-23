import whois
import time
import os.path
import sys
import csv
from ConfigParser import SafeConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domainmodels import Domains, Base


# Database bits (create_engine needs porting into config.ini)

engine = create_engine('sqlite:///domainDB.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def main_menu():
    print (30 * '-')
    print ("   M A I N - M E N U")
    print (30 * '-')
    print ("1. Scan dictionary file to DB")
    print ("2. Dump CSV")
    print ("3. Perform Look Up (include TLD!")
    print (30 * '-')

    # selection = int(raw_input('Enter your choice [1-3] : '))
    selection = raw_input("Enter your choice [1-3] : ")
    while selection not in ("1", "2", "3"):
        print "Please choose a valid option"
        selection = raw_input()
    if selection == "1":
        configure_app()
    elif selection == "2":
        dump_csv()
    elif selection == "3":
        userinput()


# Get config file and check for dictionary file
def configure_app():
    parser = SafeConfigParser()
    parser.read('config.ini')
    dictionaryFile = parser.get('config', 'dictionaryFile')
    tlds = parser.get('config', 'tlds')
    if not os.path.exists(dictionaryFile):
        print dictionaryFile + " not found!"
        sys.exit()
    else:
        iterate_domains(dictionaryFile, tlds)


def iterate_domains(dictfile, tld):
    tld = tld.split(',')
    with open(dictfile, 'rb') as f:
        for line in f:
            line = line.lower()
            line = line.rstrip()
            for tlds in tld:
                if not line:
                    print "end of the line"
                    break
                else:
                    fullurl=line+tlds
                    time.sleep(0.5)
                    print fullurl
                    whoisfnc(fullurl)


def whoisfnc(domainselected):
    print 'Checking: '+ domainselected + '.....\n'
    currentdomain = whois.whois(domainselected)
    country = (currentdomain['country'])
    city = (currentdomain['city'])
    updated_date = (currentdomain['updated_date'])
    expiration_date = (currentdomain['expiration_date'])
    registrar = (currentdomain['registrar'])

    # check if the domain exists
    exists = session.query(Domains).filter_by(domain=domainselected)
    exists_count = exists.count()

    if currentdomain.updated_date is None:
        print "Adding to database: " + domainselected + "\n"
        placeholder = "NULL"
        insertdb = Domains(domain=domainselected,
                           country=placeholder,
                           city=placeholder,
                           updated_date=placeholder,
                           expiration_date=placeholder,
                           registrar="Unregistered")
        session.add(insertdb)
        session.commit()

    elif exists_count > 0:
        print "Domain " + domainselected + " already exists"
        print "\n"
    else:
        insertdb = Domains(domain=domainselected,
                           country=country,
                           city=city,
                           updated_date=updated_date,
                           expiration_date=expiration_date,
                           registrar=registrar)
        session.add(insertdb)
        session.commit()
        print "Made entry for: " + domainselected + "\n"

def userinput():
    user_input = raw_input("Enter domain: ")
    # Strip out www prefix
    user_input = user_input.replace('www.', '')
    whoisfnc(user_input)


def dump_csv():
    selection = str(raw_input('Enter save name for csv '))
    selection = selection +'.csv'
    # add .csv
    outfile = open(selection, 'wb')
    outcsv = csv.writer(outfile)
    records = session.query(Domains).all()
    [outcsv.writerow([getattr(curr, column.name) for column in Domains.__mapper__.columns]) for curr in records]
    outfile.close()

if __name__ == '__main__':
    main_menu()
