from bottle import Bottle, request
from esql.utility.configure import Environment

# create wsgi app
app = application = Bottle()

# create esql environment
env = Environment()


from parser import init, Processor

init(env.config['parser']['optimize'], env.config['parser']['debug'])


@app.route('/es', method=('GET', 'POST'))
def execute():
    """ Execute Sql in ES
    """
    request_data = request.forms if request.method == 'POST' else request.query
    sql = request_data.get('sql')
    return Processor.execute(sql)

# print(execute('create table table_name.info (a string, b integer);'))
