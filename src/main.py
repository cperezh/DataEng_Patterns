from etl import etl_ing
import db



def main():

    etl_ing.run()

    db.ConexionBD.cerrar()


if __name__ == "__main__":

    main()