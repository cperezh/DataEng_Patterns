from etl import etl_ing
import db.connection as db



if __name__ == "__main__":

    etl_ing.run()

    db.ConexionBD.cerrar()