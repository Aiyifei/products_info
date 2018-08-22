from pymongo import MongoClient
from flask import Flask, request, Response
from bson.json_util import dumps


app = Flask(__name__)

mongo_url = 'localhost:27017'
client = MongoClient(mongo_url)
# client.crawler.authenticate(name='z', password='')
db = client.test


@app.route('/product_info/')
def product_info():
    p_type = request.args.get('p_type')
    p_name = request.args.get('p_name')

    result = []
    query_expr = {}

    # 类型和关键词为必填参数
    if not p_type or not p_name:
        ret_var = {
            'code': 1,
            'msg': 'p_type和p_name为必填参数!',
            'data': []
        }
        return Response(dumps(ret_var, ensure_ascii=False), mimetype='application/json')
    query_expr['p_type'] = p_type
    query_expr['p_name'] = p_name

    rows = db.products_info.find(query_expr)
    for row in rows:
        result.append(row)

    ret_var = {
        'code': 0,
        'msg': 'OK',
        'data': result
    }

    return Response(dumps(ret_var, ensure_ascii=False), mimetype='application/json')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
