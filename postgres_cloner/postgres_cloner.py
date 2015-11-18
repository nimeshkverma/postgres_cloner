import os
import subprocess
import datetime
import json
from basic_imports import *

class CustomError(Exception):
    def __init__(self, arg):
        self.msg = arg


class PostgresCloner:

    def __init__(self, config_path):
        """
            Constructor
            :param config_path: Path to the config(json) file
            :type  config_path: string
        """
        self.configfile_path = config_path
        TABLE_LIST = []
        SOURCE = {}
        OUTCOME = {}
        DUMP_DIR = ""
        TABLE_DUMP_FILE = ""

        try:
            jsonfile = open(config_path)
        except IOError:
            print "Please specify a file of the following format : "
            return
        required_keys = ["TABLE_LIST", "SOURCE", "OUTCOME", "DUMP_DIR", "TABLE_DUMP_FILE"]
        with open(config_path) as jsonfile:
            data = json.load(jsonfile)
            if set(data.keys()) != set(required_keys):
                msg = "Invalid file! Please specify a file of the following format : {}"
                exit()

            TABLE_LIST = data['TABLE_LIST']
            SOURCE = data['SOURCE']
            OUTCOME = data['OUTCOME']
            DUMP_DIR = data['DUMP_DIR']
            TABLE_DUMP_FILE = data['TABLE_DUMP_FILE']

        print TABLE_LIST
        print SOURCE
        print OUTCOME
        print DUMP_DIR
        print TABLE_DUMP_FILE
        self.clone()




    def execute_bash_command(self, command, password):
        """
            Function to Execute Bash commant using subprocess module
            :param command: Shell command to be executed
            :type  command: string

            :param password: Postgres password
            :type  password: string
        """
        try:
            os.putenv('PGPASSWORD', password)
            subprocess.call(command, shell=True)
        except Exception as e:
            msg = "execute_bash_command: Execution of the command: '{command}' failed due to Error:{err}".format(
                command=command, err=str(e))
            raise msg


    def table_dump(self):
        """
            Function to take dump of the tables given in Config
        """
        try:
            bash_command = 'pg_dump -U {user_name} -p {port} --data-only '.format(
                user_name=SOURCE['user'], port=SOURCE['port'])
            for table_name in TABLE_LIST:
                bash_command += '--table=' + str(table_name) + ' '
            bash_command += SOURCE['db'] + ' > ' + \
                DUMP_DIR + TABLE_DUMP_FILE

            LOGGER.info("PG Dump for Given Table Started at: {now}".format(
                now=datetime.datetime.now()))
            execute_bash_command(bash_command, SOURCE['password'])
            LOGGER.info("PG Dump for Given Table Completed at: {now}".format(
                now=datetime.datetime.now()))
        except Exception as e:
            msg = "table_dump: Table dump failed due to Error:{err}".format(
                err=str(e))
            raise msg


    def table_restore(self):
        """
            Function to restore tables from dump
        """
        try:
            bash_command = 'psql -U {user_name} -p {port} {db} < {dump_file}'.format(user_name=OUTCOME['user'],
                                                                                     port=OUTCOME[
                'port'],
                db=OUTCOME[
                'db'],
                dump_file=DUMP_DIR+TABLE_DUMP_FILE)
            LOGGER.info("Restoration of the given table started at: {now}".format(
                now=datetime.datetime.now()))
            execute_bash_command(bash_command, OUTCOME['password'])
            LOGGER.info("Restoration of the given table completed at: {now}".format(
                now=datetime.datetime.now()))
        except Exception as e:
            msg = "table_restore: Table restore failed due to Error:{err}".format(
                err=str(e))
            raise msg


    def clone(self):
        """
            Driver Function for DB_Split
        """
        try:
            self.table_dump()
            self.table_restore()
        except Exception as e:
            LOGGER.error(str(e))



if __name__ == "__main__":
    ps = PostgresCloner("config.json")

