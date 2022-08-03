from flask_script import Manager
from App.app import create_app
from flask_migrate import MigrateCommand

app = create_app()
manager = Manager(app)  # 创建实例

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
