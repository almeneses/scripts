#!/usr/bin/python

import os, sys, subprocess, argparse, csv
from typing import Dict
from shutil import which

def get_args():
  parser = argparse.ArgumentParser(
    prog = 'maidenAddUsers',
    usage = '%(prog)s [options]',
    description = 'Crea archivos de configuración para subdominios de Maidensoft 2'
  )
  parser.add_argument('-c', '--csv',
    help = 'Ubicación del archivo CSV con datos de los usuarios a crear (EJ: /home/usuario/datos.csv',
    type = str,
    required = True
  )

  parser.add_argument('-t', '--template',
    help = 'Ubicación de la plantilla (o base) de configuración (EJ: /etc/nginx/sites-available/xxx)',
    type = str,
    required = True
  )

  parser.add_argument('-o', '--output',
    help = 'Carpeta de destino de los archivos de configuración (EJ: /home/usuario) (Default: /etc/nginx/sites-available)',
    default = '/etc/nginx/sites-available/',
    type = str
  )

  parser.add_argument('-l', '--symlink',
    help = 'Carpeta de destino de enlace simbólico para el archivo de configuración creado ' +
      '(EJ: /etc/nginx/sites-enabled) (Default: /etc/nginx/sites-enabled',
    default = '/etc/nginx/sites-enabled/',
    type = str
  )

  parser.add_argument('-s', '--separator',
    help = 'Caracter separador del archivo CSV (EJ: , ;)',
    default = ',',
    type = str
  )

  return parser.parse_args()

def verify_args(command_args) -> None:
  if not is_file(command_args.csv):
    raise ValueError('La ruta especificada para "--csv" no existe')

  if not is_file(command_args.template):
    raise ValueError('La ruta especificada para "--tempĺate" no existe')

  if not is_directory(command_args.output):
    raise ValueError('La ruta especificada para "--output" no existe o no es una carpeta')


def write_config_file_from_template(
  templateFilePath:str,
  outputFilePath:str,
  replaceValues:dict
  ) -> int:
  newText = ''
  written = 0
  with open(templateFilePath) as file:
    newText = file.read()
    for key in replaceValues:
      newText = newText.replace(f'[{key}]', str(replaceValues[key]))

  with open(outputFilePath, 'w') as file:
    written = file.write(newText)

  return written;

def read_row_data_from_file(filePath, separator) -> Dict[str, str]:
  with open(filePath, 'r') as file:
    csvContent = csv.DictReader(file, delimiter = separator)
    next(csvContent)
    for row in csvContent:
      yield row

def create_symbolic_link(src:str, dest:str) -> None:
  os.symlink(os.path.abspath(src), os.path.abspath(dest))

def is_file(filePath) -> bool:
  return os.path.isfile(filePath)

def is_directory(dirPath) -> bool:
  return os.path.isdir(dirPath)

def create_mst_subdomain(
    dataFilePath:str,
    templateFilePath:str,
    symbolicLinkPath:str,
    outputFilePath:str = './',
    separator:str = ';'
  ) -> None:
  replaceDict = {}
  newConfigFileContent = ''
  fileContentWritten = 0
  userData = read_row_data_from_file(dataFilePath, separator)
  for data in userData:
    replaceDict['subdominio'] = data['subdominio']
    outputPath = os.path.join(outputFilePath, data['subdominio'])
    symlink = os.path.join(symbolicLinkPath, data['subdominio'])


    fileContentWritten = write_config_file_from_template(templateFilePath, outputPath, replaceDict)

    if(fileContentWritten > 0):
      create_symbolic_link(outputPath, symlink)
      print(f'Archivo de config. creado: {outputPath}')
    else:
      print(f'Archivo NO creado: {outputPath}')

def execute_certbot():
  if(which('certbot') is None):
    subprocess.run(['certbot', '--nginx'])
  else:
    raise ValueError('Certbot no está instalado o no está en el PATH\nNose ha podido ejecutar Certbot')

def restart_nginx():
  subprocess.run(['service', 'nginx', 'restart'])

def main() -> None:
  args = get_args()

  try:
    verify_args(args)

    print('\nCreando archivos de configuración para los subdominios...')
    create_mst_subdomain(
      dataFilePath = args.csv,
      templateFilePath = args.template,
      symbolicLinkPath = args.symlink,
      outputFilePath = args.output,
      separator = args.separator
    )

    print('\n -- Autenticando nuevos subdominios con Certbot...')
    execute_certbot()

    print('\n -- Reiniciando Nginx...')
    restart_nginx()

    print('\nHecho!')

  except Exception as error:
    raise SystemExit(error)

if __name__ == '__main__':
  main()
