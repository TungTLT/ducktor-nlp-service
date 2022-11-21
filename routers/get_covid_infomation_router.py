from get_covid_information.covid_information_client import CovidAPI
from flask import jsonify, abort
from __main__ import app


@app.route('/covid/global/get-today-infected')
def global_get_infect_today():
    result = CovidAPI().get_infected_in_day_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-total-infected')
def global_get_infect_total():
    result = CovidAPI().get_total_infected_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-today-death')
def global_get_death_today():
    result = CovidAPI().get_death_in_day_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-total-death')
def global_get_death_total():
    result = CovidAPI().get_total_death_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-today-recovered')
def global_get_recovered_today():
    result = CovidAPI().get_recover_in_day_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-total-recovered')
def global_get_recovered_total():
    result = CovidAPI().get_total_recover_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-infected')
def vn_get_infected_today():
    result = CovidAPI().get_infected_in_day_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-infected')
def vn_get_infected_total():
    result = CovidAPI().get_total_infected_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-death')
def vn_get_death_today():
    result = CovidAPI().get_death_in_day_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-death')
def vn_get_death_total():
    result = CovidAPI().get_total_death_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-today-recovered')
def vn_get_recovered_today():
    result = CovidAPI().get_recover_in_day_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-total-recovered')
def vn_get_recovered_total():
    result = CovidAPI().get_total_recover_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/global/get-summary')
def global_get_summary():
    result = CovidAPI().get_summary_global()
    if result is None:
        abort(500)
    return jsonify(result), 200


@app.route('/covid/vietnam/get-summary')
def vietnam_get_summary():
    result = CovidAPI().get_summary_vietnam()
    if result is None:
        abort(500)
    return jsonify(result), 200
