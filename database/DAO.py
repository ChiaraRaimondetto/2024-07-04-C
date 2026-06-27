from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                from state s ,sighting s2 
                where s.id= UPPER(s2.state) and year(s2.`datetime`) =%s
                group by s.id
                order by s.id asc"""
            cursor.execute(query,(anno,))

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(anno,forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
             
                    select s2.*
                    from sighting s2 
                    where  year(s2.`datetime`) =%s and s2.shape =%s
                             """
            cursor.execute(query,(anno,forma))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct YEAR(s.`datetime`) as y
                    from sighting s 
                    order by s.`datetime` desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShape(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ 
                select distinct s2.shape as shape
                from sighting s2
                where year(s2.`datetime`) =%s
                order by s2.shape asc"""
            cursor.execute(query,(anno,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result
    @staticmethod
    def getAllEdges(anno,forma, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ 
                select t1.id as id1,t2.id as id2,(t2.longitude -t1.longitude ) as peso
                from (
                select s2.*
                from sighting s2 
                where  year(s2.`datetime`) =%s and s2.shape =%s) t1, 
                (
                select s2.*
                from sighting s2 
                where  year(s2.`datetime`) =%s and s2.shape =%s ) t2
                where  t1.state =t2.state and t1.longitude < t2.longitude
                """
            cursor.execute(query,(anno,forma,anno,forma))

            for row in cursor:
                result.append(Arco(idMap[row["id1"]],idMap[row["id2"]],row["peso"]))
            cursor.close()
            cnx.close()
        return result