DDS - Descoberta de serviços
============

Objetivo
-------

Efetuar consultas estilo cmdb na base Bmc remedy.

Requisitos
----------

1. Python 2.7+
2. PIP
3. ARAPI 8
    - https://rrr.se/download/arapi/api811linux.tar.gz
4. Pyremedy
    - https://github.com/fgimian/pyremedy/archive/0.2.1.tar.gz
5. Ansible 2.2+

Instalação
----------

Efetuar o download dentro da pasta **/tmp**.

1. PIP
    - yum -y install python-pip

2. Dependências lib Remedy.
    - mkdir /opt/remedy
    - tar -xvfz api811linux.tar.gz  -C /opt/remedy --strip 1
    ```
    echo '# Remedy ARS support' > /etc/ld.so.conf.d/remedy.conf
    echo /opt/remedy/lib >> /etc/ld.so.conf.d/remedy.conf
    echo /opt/remedy/bin >> /etc/ld.so.conf.d/remedy.conf
    sudo ldconfig
    ```
3. Pyremedy
    - tar -xzvf pyremedy-0.2.1.tar.gz
    ```
    cd /tmp/pyremedy-0.2.1
    python setup.py install
    ```

4. Exemplo de utilização do playbook
- anadds_proc: Nome do modulo
- changeID: Nº do chamado
- Status: Andamento do chamado

```
- hosts: localhost
- name: Poc DDS BMC Remedy - Descoberta de servico
  anadds_proc:
  tasks:
    - name: Poc DDS BMC Remedy
      anadds_proc:
        ChangeID: CHG00******
        Status: WorkInProgress
      register: result
    - debug: var=result
```

5. Arquivo de configuração config.yaml
- OBS: **Esse arquivo é simplesmente temporário, a nível de desenvolvimento.**
- Arquivo devera fica no mesmo nível do modulo
- Arquivo **temp** contendo as credencias e endereço do servidor.
```
--- 
credencial:
  login: ""
  senha: ""
servidor:
  rede: ""
  porta: 2020
```