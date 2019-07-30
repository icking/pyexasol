"""
Example 24
Script output server

Exasol should be able to open connection to the host where current script is running
"""

import pyexasol
import _config as config
import os

import pprint
printer = pprint.PrettyPrinter(indent=4, width=140)

is_travis = 'TRAVIS' in os.environ

C = pyexasol.connect(dsn=config.dsn, user=config.user, password=config.password, schema=config.schema,
                     query_timeout=5,
                     # Custom parameters are required to make this example work in Travis context
                     # 172.17.0.1 is an IP address of docker host in Linux
                     udf_output_bind_address=('', 8580) if is_travis else None,
                     udf_output_connect_address=('172.17.0.1', 8580) if is_travis else None
                     )

stmt, log_files = C.execute_udf_output("""
    SELECT echo_java(user_id)
    FROM users
    GROUP BY CEIL(RANDOM() * 4)
""")

printer.pprint(stmt.fetchall())
printer.pprint(log_files)

print(log_files[0].read_text())
