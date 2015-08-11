import whois
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

def donothing():
    pass

def userinput():
    userin = raw_input("Enter domain: ")
    userin = userin.replace('www.', '')
    whoisfnc(userin)

def whoisfnc(domainsel):
    domaindict = whois.whois(domainsel)
    domainvar = (domainsel)
    country = (domaindict['country'])
    city = (domaindict['city'])
    updated_date = (domaindict['updated_date'])
    expiration_date = (domaindict['expiration_date'])
    registrar = (domaindict['registrar'])
    exists = session.query(Domains).filter_by(domain=domainvar)
    exists_count = exists.count()
    if domaindict.updated_date is None:
        print "Not a registered domain"
        donothing()
    # Build an array of entries
    # ISSUE = its using the for loop for the amount of times it runs over the same domainentry / existing

    elif exists_count > 0:
        print "Domain " + domainvar + " already exists"
    else:
        print "Adding " + domainvar
        insertdb = Domains(domain=domainvar,
                               country=country,
                               city=city,
                               updated_date=updated_date,
                               expiration_date=expiration_date,
                               registrar=registrar)
        session.add(insertdb)
        session.commit()
        print "Made entry for: " + domainvar

if __name__ == '__main__':
    userinput()

