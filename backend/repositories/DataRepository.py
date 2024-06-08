from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def create_historiek(deviceid, gebruikerid, actiedatum, waarde, commentaar):
        sql = "INSERT INTO historiek (DeviceID, GebruikerID, Actiedatum, Waarde, Commentaar) VALUES \
        (%s,%s,%s,%s,%s)"
        params = [deviceid, gebruikerid, actiedatum, waarde, commentaar]
        return Database.execute_sql(sql, params)

    def get_id_sensor(beschrijving):
        sql = "SELECT DeviceID FROM device where beschrijving = %s;"
        params = [beschrijving]
        return Database.get_one_row(sql,params)
    
    def get_latest_waterlevel():
        sql = "SELECT Waarde FROM historiek \
                WHERE DeviceID = 2 \
                ORDER BY Actiedatum DESC \
                LIMIT 1"
        return Database.get_one_row(sql)
    
    def get_latest_proteinweight():
        sql = "SELECT Waarde FROM historiek \
                WHERE DeviceID = 3 \
                ORDER BY Actiedatum DESC \
                LIMIT 1"
        return Database.get_one_row(sql)

    def get_latest_creatineweight():
        sql = "SELECT Waarde FROM historiek \
                WHERE DeviceID = 4 \
                ORDER BY Actiedatum DESC \
                LIMIT 1"
        return Database.get_one_row(sql)
    
    def read_historiek():
        sql = "SELECT * FROM historiek"
        return Database.get_rows(sql)
    
    def create_gebruiker(gebruikersnaam, wachtwoord, email, aanmaakdatum):
        sql = "INSERT INTO gebruiker (Gebruikersnaam, Wachtwoord, Email, Aanmaakdatum) VALUES \
        (%s,%s,%s,%s)"
        params = [gebruikersnaam, wachtwoord, email,aanmaakdatum]
        return Database.execute_sql(sql, params)
    
    def get_user_by_email(email):
        sql="SELECT * FROM gebruiker where Email = %s"
        params = [email]
        return Database.get_one_row(sql, params)


