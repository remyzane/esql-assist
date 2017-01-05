from bottle import Bottle, request
from esql.utility.configure import Environment

# create wsgi app
app = application = Bottle()

# create esql environment
env = Environment()


from esql import parser, processor
from esql.processor import execute

parser.init(env.config['parser'])
processor.init()


@app.route('/es', method=('GET', 'POST'))
def es_sql():
    """ Execute Sql in ES
    """
    request_data = request.forms if request.method == 'POST' else request.query
    sql = request_data.get('sql')
    return execute(sql)

# print(execute('create table table_name.info (a string, b integer);'))
