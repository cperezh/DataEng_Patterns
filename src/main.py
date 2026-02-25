from etl import etl_ing
import db
import argparse



def main(file_name:str):

    etl_ing.run(file_name)

    db.ConexionBD.cerrar()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='main.py',
                    description='ETL runner',
                    epilog='Text at the bottom of help')
    
    parser.add_argument('filename')
    args = parser.parse_args()
    
    main(args.filename)