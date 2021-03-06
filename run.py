from datausa import app

from flask.ext.script import Manager, Command, Option

class GunicornServer(Command):

    description = 'Run the app within Gunicorn'
    #if you're running this on a VM, set host='0.0.0.0' and make sure to forward port 8000 so the host can access the VM's port 8000
    #on a cloud server, or behind nginx, set host='127.0.0.1'
    def __init__(self, host='127.0.0.1', port=8000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def __call__(self, app, host, port, workers):

        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)),'workers': workers}), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers 
                    }

                def load(self):
                    return app

            FlaskApplication().run()

if __name__ == '__main__':
    app.debug = True
    manager = Manager(app)
    manager.add_command("gunicorn", GunicornServer())
    manager.run()
