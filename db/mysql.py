import drconf.db as db
import drconf.dr as dr
import MySQLdb

def connect():
	dr.log.debug("[MYSQL]begin to connect mysql DB")
	return MySQLdb.connect(db.DBSERVER , db.DBUSER , db.DBPASS , db.DBNAME, charset=dr.ENCODING);


def query(sql):
	dr.log.debug("[MYSQL]ready to query sql:" + sql)
	db = connect()
	cur = db.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	db.close()

	return results
