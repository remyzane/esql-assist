from bottle import Bottle, request
from esql.utility.configure import Environment

# create wsgi app
app = application = Bottle()

# create esql environment
env = Environment()


from esql import parser
from esql.processor import init as processor_init, Processor

parser.init(env.config['parser'])
processor_init()


@app.route('/es', method=('GET', 'POST'))
def execute():
    """ Execute Sql in ES
    """
    request_data = request.forms if request.method == 'POST' else request.query
    sql = request_data.get('sql')
    return Processor.execute(sql)

# print(execute('create table table_name.info (a string, b integer);'))
