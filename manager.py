from tabulate import tabulate
from APP import create_app
from APP.extensions import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys

app = create_app()
migrate = Migrate(app, db)

database_manager = Manager(app)
database_manager.add_command('db', MigrateCommand)


def bordered(text, width=50):
    lines = text.center(width).splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    print('\n'.join(res))


def init_db():
    with app.app_context():
        db.create_all()
    bordered("DB Initialized")


def drop_db():
    with app.app_context():
        db.drop_all()
    bordered("DB Dropped")

def reset_db():
    drop_db()
    init_db()
    bordered("DB has Been rested")


def generat_dummy_data():
    reset_db()
    bordered("dummy data Has been Genarated")


commands = {'init_db': init_db, 'drop_db': drop_db, 'reset_db': reset_db, 'dummy': generat_dummy_data, 'db': database_manager.run, 'run': app.run}


all_commands = [["run", "To Run The Server"]]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for command, function in commands.items():
            if sys.argv[1] == command:
                function()
    else:
        print(' ')
        print("Not Valid Command".center(50))
        print(' ')
        print("Please Enter Valid one from Commands Listed Below".center(50))
        print('-' * 50)
        print(' ')
        print(tabulate(all_commands, headers=[
              'Command', 'Description'], showindex="always", tablefmt="github"))
        print(' ')
