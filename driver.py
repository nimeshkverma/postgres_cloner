import os
import subprocess
import config
import datetime
from basic_imports import *


def execute_bash_command(command, password):
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


def table_dump():
    """
        Function to take dump of the tables given in Config
    """
    try:
        bash_command = 'pg_dump -U {user_name} -p {port} --data-only '.format(
            user_name=config.SOURCE['user'], port=config.SOURCE['port'])
        for table_name in config.TABLE_LIST:
            bash_command += '--table=' + str(table_name) + ' '
        bash_command += config.SOURCE['db'] + ' > ' + \
            config.DUMP_DIR + config.TABLE_DUMP_FILE

        LOGGER.info("PG Dump for Given Table Started at: {now}".format(
            now=datetime.datetime.now()))
        execute_bash_command(bash_command, config.SOURCE['password'])
        LOGGER.info("PG Dump for Given Table Completed at: {now}".format(
            now=datetime.datetime.now()))
    except Exception as e:
        msg = "table_dump: Table dump failed due to Error:{err}".format(
            command=command, err=str(e))
        raise msg


def table_restore():
    """
        Function to restore tables from dump
    """
    try:
        bash_command = 'psql -U {user_name} -p {port} {db} < {dump_file}'.format(user_name=config.OUTCOME['user'],
                                                                                 port=config.OUTCOME[
            'port'],
            db=config.OUTCOME[
            'db'],
            dump_file=config.DUMP_DIR+config.TABLE_DUMP_FILE)
        LOGGER.info("Restoration of the given table started at: {now}".format(
            now=datetime.datetime.now()))
        execute_bash_command(bash_command, config.OUTCOME['password'])
        LOGGER.info("Restoration of the given table completed at: {now}".format(
            now=datetime.datetime.now()))
    except Exception as e:
        msg = "table_restore: Table restore failed due to Error:{err}".format(
            command=command, err=str(e))
        raise msg


def main():
    """
        Driver Function for DB_Split
    """
    try:
        table_dump()
        table_restore()
    except Exception as e:
        LOGGER.error(str(e))

if __name__ == '__main__':
    main()
