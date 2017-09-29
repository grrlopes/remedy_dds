# -*- coding: utf-8 -*-
#!/usr/bin/env python

DOCUMENTATION = '''
---
module: anadds_proc
short_description: Descoberta de serviço na base BMC Remedy
'''

EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: POC DDS BMC Remedy - Descoberta de servico
      anadds_proc:
        ChangeID: CHG00*****
        Status: WorkInProgress
      register: result
    - debug: var=result
'''
import os
import base64
import yaml
from pyremedy import ARS, ARSError
from ansible.module_utils.basic import AnsibleModule
__author__ = 'Equipe Automação Indracompany'

class Anadds_proc:
    '''
    Class construtora que com os objetos
    de credenciais, conexões e query
    '''
    def __init__(self):
        self.rede = None
        self.porta = None
        self.login = None
        self.senha = None
        self.cred = None
        self.conexao = None
        self.resultado = None
        self.query = None

    def _conf(self):
        if os.path.isfile(os.getcwd()+'/workspace_produban/pyremedy_modulo/library/config.yaml'):
            self.cred = yaml.load(open(os.getcwd()+'/workspace_produban/pyremedy_modulo/library/config.yaml', 'r'))
            for nivel in self.cred:
                for valor in self.cred[nivel]:
                    if valor == 'login':
                        self.login = self.cred[nivel][valor]
                    elif valor == 'senha':
                        self.senha = self.cred[nivel][valor]
                    elif valor == 'rede':
                        self.rede = self.cred[nivel][valor]
                    elif valor == 'porta':
                        self.porta = self.cred[nivel][valor]
                    '''
                    elif valor == 'query':
                        self.query = self.cred[nivel][valor]
                    '''
        else:
            return "Config.yaml não encontrado ou erro de syntax"

    def filtros(self):
        '''
            Efetua retrieve do valores esperados.
        '''
        lista = ['Change ID+', 'Summary', 'Status', 'Department', 'Region', \
        'Description', 'Requester Login Name+', 'Requester ID+', 'Requester Name+']
        self.resultado = self.conexao.query(
            schema='CHG:Change',
            qualifier=self.query,
            fields=lista,
            offset=0,
            limit=1
        )
        '''
        for base_chave, base_valor in self.resultado:
            for chave, valor in base_valor.items():
                print '{}:{}'.format(chave, valor)
        '''

    def cnxbmc(self):
        '''
        Methodo que encapsula a conexão com a base remedy, efetuado autenticação
        em caso de sucesso ou não.
        '''
        try:
            self.conexao = ARS(server=base64.b64decode(self.rede), port=self.porta, \
             user=base64.b64decode(self.login), password=base64.b64decode(self.senha))
            self.filtros()
        except ARSError:
            for message_number, message_text, appended_text in self.conexao.errors:
                if appended_text:
                    print(
                        '\nMessage {}: {} ({})'.format(message_number, message_text, appended_text)
                        +'\nVerique conexao ou query'
                    )
                else:
                    print(
                        'Message {}: {}'.format(message_number, message_text)
                        +'\nVerique configuracao de conexao'
                    )
        finally:
            if self.conexao is not None:
                self.conexao.terminate()
            print "\nExecução finalizada\n"

    def playana(self):
        """
        Frame AnsibleModule que manipula o status, filtros e
        valores com base nos parametros do playbook.
        """
        self._conf()
        fields = {
            "ChangeID": {"required": True, "type": "str"},
            "Status": {"required": True, "type": "str"}
        }
        module = AnsibleModule(
            argument_spec=fields
        )

        if module.check_mode:
            module.exit_json(changed=False)
        if module.params['Status'] == 'WorkInProgress' and module.params['ChangeID'] is not None:
            self._conf()
            self.query = """ 'Status*' != "Scheduled" AND
            'Change ID+' = \""""+module.params['ChangeID']+"""\" """
            self.cnxbmc()
            module.exit_json(changed=False, msg=self.resultado)
        else:
            msg = "Não encontrado"
            module.fail_json(msg=msg)

class Executa(Anadds_proc):
    '''
    Inicialiaza o projeto: Chama a methodo playana
    contento o manipulador do AnsibleModule
    '''
    def __init__(self):
        Anadds_proc.__init__(self)
        self.playana()

class Principal:
    if __name__ == "__main__":
        Executa()
