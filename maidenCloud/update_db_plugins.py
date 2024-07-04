import xmlrpc.client
import sys

from os import getenv
from dotenv import load_dotenv

def get_available_databases(db_endpoint_url):
    try:
        common = xmlrpc.client.ServerProxy(db_endpoint_url)
        return common.list()
    except xmlrpc.client.Fault as e:
        raise Exception(f"XML-RPC Fault: {e}")
    except Exception as e:
       raise Exception(f"Error: {e}")

    return []

# Función para obtener el uid del usuario
def authenticate(database, odoo_url, username, password):
    common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
    uid = common.authenticate(database, username, password, {})
    if uid == 0:
        print(f"Error de autenticación en la base de datos {database}")
        sys.exit(0)
    return uid

# Función para actualizar el módulo
def update_module(database, odoo_url, uid, password, module_name):
    models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")
    module_ids = models.execute_kw(database, uid, password, "ir.module.module", "search", [[["name", "=", module_name], ["state", "in", ["installed", "to upgrade"]]]])
    if not module_ids:
        print(f"El módulo {module_name} no se encontró en la base de datos {database}")
        return
    models.execute_kw(database, uid, password, "ir.module.module", "button_upgrade", [module_ids])
    print(f"El módulo {module_name} ha sido actualizado en la base de datos {database}")

def update_dbs():
    url = getenv('MAIDEN_BASE_URL')
    db_endpoint = f'{url}/xmlrpc/2/db'

    # Configura tus bases de datos y credenciales
    username = getenv('ODOO_USER')
    password = getenv('ODOO_PASSWORD')
    module_name = "l10n_co_e_invoicing"

    databases = get_available_databases(db_endpoint)
    failed = []
    # Actualiza el módulo en todas las bases de datos
    for db in databases:
        try:
            db_url = f'https://{db}'
            print(f"Actualizando plugins en {db}")
            uid = authenticate(db, db_url, username, password)
            update_module(db, db_url, uid, password, module_name)
        except:
            failed.append(db)
        

    print("Terminado")
    print(f"Los siguientes dominios no pudieron ser actualizados: {failed}")


if __name__ == '__main__':
    load_dotenv()
    update_dbs()
