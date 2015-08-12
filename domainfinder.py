import time

import whois
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domainmodels import Domains, Base


engine = create_engine('sqlite:///domainDB.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def open_file():
    with open('domains.txt', 'rb') as f:
        for line in f:
            line = line.lower()
            line = line.rstrip()  # this seems to work
            time.sleep(0.5)
            whoisfnc(line)

def donothing():
    pass

def userinput():
    userin = raw_input("Enter domain: ")
    userin = userin.replace('www.', '')
    whoisfnc(userin)

def whoisfnc(domainsel):
    print 'Checking: '+ domainsel + '.....'
    domaindict = whois.whois(domainsel)
    country = (domaindict['country'])
    city = (domaindict['city'])
    updated_date = (domaindict['updated_date'])
    expiration_date = (domaindict['expiration_date'])
    registrar = (domaindict['registrar'])

    # check if the domain exists
    exists = session.query(Domains).filter_by(domain=domainsel)
    exists_count = exists.count()

    if domaindict.updated_date is None:
        print "Not a registered domain: " + domainsel
        print "\n"
        donothing()

    elif exists_count > 0:
        print "Domain " + domainsel + " already exists"
        print "\n"
    else:
        insertdb = Domains(domain=domainsel,
                               country=country,
                               city=city,
                               updated_date=updated_date,
                               expiration_date=expiration_date,
                               registrar=registrar)
        session.add(insertdb)
        session.commit()
        print "Made entry for: " + domainsel
        print "\n"

if __name__ == '__main__':
    open_file()
    #userinput()

