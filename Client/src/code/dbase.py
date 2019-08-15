
from tinydb import TinyDB, Query
config = 'config.json'
query = Query()
db = TinyDB(config)
#
#
def main():
    #this value is static for now
    val = "user-pc"
    get_db_info(val)
#
#
def get_db_info(val):
    if db.search(query.value == val):
        print ("[!] config exists continuing.")
        return True
    else:
        print("[!] value not present. adding host info to config file....")
        db.insert({'type': 'HostName', 'value': val})


    #else:
    #    print("value not present. adding host info to config file....")
    #    db.insert({'type': 'Location', 'value': 'Middletown, NJ'})
    #    db.insert({'type': 'HostName', 'value': "Office10-pc"})
    #    #db.insert({'type': 'Location', 'value': 'Middletown, NJ'})
    #    db.insert({'type': 'Type', 'value': "Workstation"})
    #    db.insert({'type': 'Address', 'value': "192.168.2.24"})
    #    db.insert({'type': 'OS', 'value': "nt"})
#db.remove(db.value == "testhost")
    #db.purge()
#db.remove(db.type == Location)
#value = Query()

    #db.remove(value.type == 'Location')
#db.search(location.value == 'Middletown, NJ')
#dbs = db.all()
#print(dbs)

if __name__=='__main__':
    main()