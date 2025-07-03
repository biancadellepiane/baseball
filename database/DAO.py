from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select distinct t.`year` as year
                    from teams t 
                    where t.`year` > 1979"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsofYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """ select *
                    from teams t 
                    where t.`year` = %s"""

        cursor.execute(query, (year,)) #prendo non solo la query ma anche l'inserimento dell'year

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeam(year, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select t.teamCode , t.ID , sum(s.salary) as TotSalary
                from teams t, salaries s, appearances a 
                where s.`year` = t.`year` and t.`year` = a.`year` 
                and a.`year` = %s
                and t.ID = a.teamID 
                and s.playerID = a.playerID 
                group by t.teamCode"""


        result = {}
        cursor.execute(query, (year,))

        for row in cursor:
            #dizionario [squadra] = [valore salario]
            result[idMap[row["ID"]]] = row["TotSalary"]

        cursor.close()
        conn.close()
        return result






