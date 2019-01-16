from datetime import datetime, timedelta, timezone
from flask import render_template, request, jsonify, session, redirect
from os import path, environ

from ..insight import application
from ..services import authentication_service
from ..services.events_service import search
from ..services import calendar_service
from ..services.chart_service import draw_chart, build_file_name, add_path_to_file
from ..utilities.util import format_date, convert_date


@application.before_request
def before_request():
    if 'credentials' not in session and request.endpoint != 'authentication_handler':
        return authentication_service.create_auth_request()


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    """
    A method handling GET and POST requests to the index page
    :return: the template for the index page
    """

    calendar_list = calendar_service.get_calendars()

    if request.method == 'GET':
        return render_template('index.html', calendars=calendar_list, request=request)

    elif request.method == 'POST':
        query = request.form.get('query')
        calendar = request.form.get('calendar')
        sort = request.form.get('sort_by')
        results, days, hours, minutes = search(calendar, query, sort)
        return render_template('index.html', calendars=calendar_list, results=results, days=days, hours=hours,
                               minutes=minutes, query=query, current_cal=calendar, current_sort=sort, request=request)


@application.route('/analysis', methods=['GET', 'POST'])
def analysis():
    """
    A method handling GET and POST requests to the Analysis page
    :return: the template for the Analysis page
    """

    first_date = None
    second_date = None
    file_name = None

    if request.method == 'GET':
        now = datetime.now(timezone.utc)
        first_date = datetime(now.year, now.month, now.day)
        second_date = first_date + timedelta(1)

        # the future date must be the first parameter
        file_name = build_file_name(first_date, second_date)

        if not path.isfile(add_path_to_file(file_name)):
            draw_chart(second_date.astimezone().isoformat(), first_date.astimezone().isoformat(), file_name)

    elif request.method == 'POST':
        req = request.get_json()
        sanitized_other = req['other_date'].replace("th", "").replace("2nd", "2").replace("st", "").replace("\n", " ")
        other_date = datetime.strptime(sanitized_other, '%A %B %d %Y').astimezone()
        date_val = convert_date(req['date_val']).astimezone()
        first_date = date_val if req['el_id'] == '1' else other_date
        # add on an extra day so our date range is inclusive (as in GET request)
        second_date = (date_val if req['el_id'] == '2' else other_date) + timedelta(1)

        if second_date <= first_date:
            # this is an invalid request so do not return a file name
            return jsonify({})

        # the future date must be the first parameter
        file_name = build_file_name(first_date, second_date)

        if not path.isfile(add_path_to_file(file_name)):
            draw_chart(second_date.isoformat(), first_date.isoformat(), file_name)
        file_name = file_name[4:]

        return jsonify({'fileName': file_name})

    first_date = format_date(first_date)
    second_date = format_date(second_date)

    file_name = file_name[4:]

    return render_template('analysis.html', request=request, fileName=file_name,
                           first=first_date, second=second_date)


@application.route('/form', methods=['GET'])
def form():
    """
    Handles GET requests to the form feedback page.
    """
    return render_template('form.html', request=request)


@application.route('/authenticate', methods=['GET'])
def authentication_handler():
    """
    Handles redirects where Google has authenticated the user
    :return: a redirect to the environment's root URL
    """
    # set credentials in session to the newly authorised user
    session['credentials'] = authentication_service.authorize_user(request)

    return redirect(environ.get('ROOT_URL'))


# ERROR HANDLERS


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')