import whois
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domainmodels import Domains, Base

engine = create_engine('sqlite:///domainDB.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def userinput():
    userin = raw_input("Enter domain: ")
    userin = userin.replace('www.','')
    whoisfnc(userin)

def whoisfnc(domainsel):
    dict = whois.whois(domainsel)
    domain = (domainsel)
    country = (dict['country'])
    city = (dict['city'])
    updated_date = (dict['updated_date'])
    expiration_date = (dict['expiration_date'])
    registrar = (dict['registrar'])

    # put it in the database
    insertdb = Domains(domain=domain,country=country,city=city,updated_date=updated_date,expiration_date=expiration_date)
    session.add(insertdb)
    session.commit()
'''
    print "Country:\t {country}".format(**dict)
    print "City:\t\t {city}".format(**dict)
    print "Updated last:\t {updated_date}".format(**dict)
    print "Expiration date:\t {expiration_date}".format(**dict)
    print "Registrar:\t {registrar}".format(**dict)

    # get nameservers
    ns_list = dict['name_servers']
    for ns in ns_list:
        print "Name Server:\t %s" % ns

    # get emails
    email_list = dict['emails']
    for email in email_list:
        print "Contact Email:\t %s" % email
'''
if __name__ == '__main__':
    userinput()

# notes

# cat /usr/share/dict/words > words.txt
