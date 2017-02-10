import sys
import pony.orm as pny
import Crypto.PublicKey.RSA as RSA


database = pny.Database()
database.bind(
        'mysql',
        host='localhost',
        user='biomio_admin',
        passwd='gate',
        db='biomio_db'
    )


@pny.db_session
def geberate_token(providerID):
    key = RSA.generate(1024)
    private_pem = key.exportKey()
    public_pem = key.publickey().exportKey()

    result = database.execute("""SELECT p.id FROM ProviderJWTKeys p WHERE p.ProviderId = {};""".format(providerID))
    result = result.fetchone()
    if result:
        database.execute(
            """
                UPDATE ProviderJWTKeys p
                SET
                  p.private_key="{private_pem}",
                  p.public_key="{public_pem}"
                WHERE p.ProviderId = {providerID};
            """.format(private_pem=private_pem, public_pem=public_pem, providerID=providerID)
        )
        database.commit()
        return True
    else:
        result = database.execute("""SELECT p.id FROM Providers p WHERE p.id = {};""".format(providerID))
        result = result.fetchone()
        if result:
            database.execute(
                """
                    INSERT INTO ProviderJWTKeys (private_key, public_key, providerID)
                    VALUES ("{private_pem}", "{public_pem}", {providerID});
                """.format(private_pem=private_pem, public_pem=public_pem, providerID=providerID)
            )
            database.commit()
            return True
    return False


if __name__ == "__main__":
    print geberate_token(sys.argv[1])
