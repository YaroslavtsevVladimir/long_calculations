import multiprocessing
import sqlite3
import time
import uuid

from flask import Flask, request, Response


app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    return connection


@app.route('/calculate/', methods=['GET'])
def get_number():
    calculation_id = uuid.uuid4().hex
    number = request.args.get('x')

    if not isinstance(number, float):
        number = float(number)

    get_result_process = multiprocessing.Process(target=save_calculated_result, args=(calculation_id, number))
    get_result_process.start()

    return Response(f'Your id: {calculation_id}\n', status=201)


@app.route('/result/', methods=['GET'])
def get_result():
    connection = get_db_connection()
    calculation_id = request.args.get('id')

    if calculation_id is None:
        return 'Please set the "id" parameter to the request.\n'

    result = connection.execute(
        'SELECT result FROM results WHERE id = ?',
        (calculation_id, )
    ).fetchone()
    connection.close()

    if result is None:
        return 'Your request is being processed, please wait\n'

    return Response(f'Calculation result: {result[0]}\n', status=200)


def save_calculated_result(calculation_id, number):
    time.sleep(20)
    connection = get_db_connection()
    connection.execute(
        'INSERT INTO results (id, result) VALUES (?, ?)',
        (calculation_id, 2 * number)
    )
    connection.commit()
    connection.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
