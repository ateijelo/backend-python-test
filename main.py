"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py migratedb
"""

from __future__ import print_function

from docopt import docopt
import subprocess
import sys
import os

from alayatodo import app


def _run_sql(filename):
    try:
        with open(filename) as f:
            subprocess.check_output(
                ["sqlite3", app.config['DATABASE']],
                stdin=f,
                stderr=subprocess.STDOUT,
            )
    except subprocess.CalledProcessError, ex:
        print(ex.output)
        sys.exit(1)


def _run_migrations(migrations_dir):
    for mig in sorted(os.listdir(migrations_dir)):
        if not mig.lower().endswith('.sql'):
            continue

        db_version = int(subprocess.check_output([
            "sqlite3","-noheader","-csv",
            app.config['DATABASE'],
            "PRAGMA user_version"
        ]).strip())
        try:
            mig_version = int(mig.split("-", 1)[0])
        except ValueError:
            print("Migrations must be named <INTEGER>-brief-description.sql", file=sys.stderr)
            os.exit(1)

        if db_version > mig_version:
            continue

        print("Running migration {}... ".format(mig), end="")
        _run_sql(os.path.join(migrations_dir, mig))
        # Update database version
        subprocess.check_call([
            "sqlite3",
            app.config['DATABASE'],
            "PRAGMA user_version = {}".format(mig_version)
        ])
        print("done.")


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("AlayaTodo: Database initialized.")
    elif args['migratedb']:
        _run_migrations('resources/migrations')
    else:
        app.run(use_reloader=True)
