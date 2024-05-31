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
    
    def read_historiek():
        sql = "SELECT * FROM historiek"
        return Database.get_rows(sql)
    
    def create_gebruiker(gebruikersnaam, wachtwoord, email, voornaam, achternaam, geboortedatum, rol, accountstatus, aanmaakdatum, laatstingelogd):
        sql = "INSERT INTO gebruiker (GebruikerID, Gebruikersnaam, Wachtwoord, Email, Voornaam, Achternaam, Geboortedatum, Rol, AccountStatus, Aanmaakdatum, LaatstIngelogd) VALUES \
        (%s,%s,%s,%s,%s)"
        params = [gebruikersnaam, wachtwoord, email, voornaam, achternaam, geboortedatum, rol, accountstatus, aanmaakdatum, laatstingelogd]
        return Database.execute_sql(sql, params)


