#!/home/ksoze/anaconda3/bin/python3.7

import os
import sys
import json
from time import time
import datetime as dt
try:
    from tqdm import tqdm
except:
    print('Pacote "tqdm" não instalado. Instale o pacote por meio do seguinte comando: pip install tqdm')
    sys.exit()

# Por quantos dias um arquivo JSON correspondente a uma pasta não deve ser atualizado?
DIAS = 7

class duplicados():
    def __init__(self, pasta):
        self.DIR = pasta
        self.LISTA = list(os.popen(f'find {self.DIR} -type f').readlines())
        self.DIC = {}
        self.DUPL = []
        
        # define arquivo JSON com nome do diretório atual
        self.NAME = os.path.basename(self.DIR) + '.json'
        self.FILE = os.path.join(self.DIR, self.NAME)
        self.lista()

    def exist_json(self):   
        ''' checa se existe o archivo JSON com nome do diretório atual '''
        
        if os.path.exists(self.FILE):
            with open(self.FILE, 'r', newline='\n') as arquivo:
                try:
                    self.DIC = json.load(arquivo)
                    self.LAST = float(self.DIC['timestamp'])
                    self.DIC.pop('timestamp', None)

                    for item in self.DIC:
                        if len(self.DIC[item]) > 1:
                            self.DUPL.append(item)
                except:
                    print('ERROR arquivo provavelmente não tem uma timestamp na última linha\nOu então o arquivo JSON não está bem formado')
            return float(self.LAST)
        else:
            self.LAST = False
            return self.LAST
                    
    def md5(self, file, dicio):
        try:
            md5_hash = os.popen(f'md5sum \"{file}\"').read().split()[0]
            if md5_hash not in dicio:
                dicio[md5_hash] = []
            else:
                self.DUPL.append(md5_hash)
            dicio[md5_hash].append(file)
        except Exception as error:
            print('ERRO gerando md5sum do arquivo:\n', file, error)

    def gravar(self):
        if len(self.DUPL) == 1:
            print('1 arquivo duplicado')
        elif len(self.DUPL) > 1:
            print(f'{len(self.DUPL)} arquivos duplicados')
            
        with open(self.FILE, 'w') as f:
            json.dump(self.DIC, f, indent=3, ensure_ascii=False)
            print(f'Arquivo GERADO {self.FILE}\n')
        
    def lista(self):
        ''' Gera o dicionário e o arquivo JSON caso ele não exista '''

        if not self.exist_json():
            print('Gerando o JSON...')
            for item in tqdm(self.LISTA):
                file = item.strip()
                self.md5(file, self.DIC)

            self.DIC['timestamp'] = str(time())
            self.gravar()
        else:
            self.update()            

    def update(self):
        ''' Atualiza o arquivo JSON no caso dele já existir no diretório '''

        if DIAS != 0  or (dt.datetime.now() - dt.datetime.fromtimestamp(self.LAST)).days <= DIAS:
            print('Arquivo JSON recente')
        else:
            print('Atualizando JSON...')
            CONJUNTO = []
            ct = 0
            # Gera uma lista com todos os nomes de livros, guardados como valores de um dicionário
            # cujas chaves são o md5sum de cada arquivo (ou arquivos)
            for file in self.DIC.values():
                if len(file) > 1:
                    while ct < len(file):
                        CONJUNTO.append(file[ct])
                        ct += 1 
                else:
                    CONJUNTO.append(file[0]) 

            for item in tqdm(self.LISTA):
                file = item.strip()
                if file in CONJUNTO:
                    continue
                else:
                    # Retirar o '\n' do path do arquivo
                    print('Novo arquivo: ', file)
                    self.md5(file, self.DIC)

            self.DIC['timestamp'] = str(time())
            self.gravar()

    @property
    def mostrar(self):
        '''  Mostra os arquivos duplicados '''
        print(json.dumps(self.DIC, indent=3, ensure_ascii=False))        

    def duplicados(self):
        if len(self.DUPL) == 0:
            print('Nenhum arquivo duplicado')
        else:
            sep = '\n\033[0m'
            for num, item in enumerate(self.DUPL, 1):
                prim = self.DIC[item][0]
                print('\033[1;32;40m {} \033[0m'.format(num), '\033[1;31;40m ({}) \033[0m'.format(len(self.DIC[item])))
                print('\033[0;33;40m{}\033[0m'.format(sep.join(self.DIC[item])))

    # ------------------------ comparar dois objetos ---------------
        
    def dupl_pastas(self, obj=False, return_lists=False):
        if self.DIR in obj.DIR or obj.DIR in self.DIR:
            print('Atenção! Uma das pastas está contida dentro da outra')

        diff, comm = [], []
        if not obj.DIC:
            print('É preciso indicar um outro objeto da mesma CLASSE com que comparar')
            return 
        else:
            for hash_file in self.DIC:
                if hash_file not in obj.DIC:
                    diff.append(self.DIC[hash_file])
                else:
                    comm.append(obj.DIC[hash_file])

        self.map_dupl = {}
        for item in comm:
            self.map_dupl[item] = []
            self.map_dupl[item].append(self.DIC[item])
            self.map_dupl[item].append(obj[item])
        
        print(f' {len(comm)} arquivos comuns\n {len(diff)} arquivos diferentes')
        if return_lists:
            return diff, comm
