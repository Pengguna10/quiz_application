import os
from flask import Flask, session, request, redirect, url_for, render_template
from db_scripts import get_question_after, get_quises


def start_quis(quiz_id):
    '''creates the desired values in the session dictionary'''
    session['quiz'] = quiz_id
    session['last_question'] = 0


def end_quiz():
    session.clear()


def quiz_form():
    '''the function gets a list of quizzes from the database and formulates a form with a drop-down list'''
    q_list = get_quises()
    return render_template('first.html', q_list=q_list)


def index():
    '''First page: if it came with a GET request, then choose a quiz,
    if POST, then remember the quiz ID and send it to the questions'''
    if request.method == 'GET':
        # the quiz is not selected, reset the quiz id and show the selection form
        start_quis(-1)
        return quiz_form()
    else:
        # received additional data in the request! Use them:
        quest_id = request.form.get('quiz') # selected quiz number
        start_quis(quest_id)
        return redirect(url_for('test'))


def test():
    '''returns the question page'''
    # what if a user without choosing a quiz went straight to the address '/test'?
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # there is still an old version of the function:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]
            # if we've taught the database to return Row or dict, then we shouldn't write result[0] and instead write result['id']
            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'


def result():
    end_quiz()
    return "that's all folks!"


folder = os.getcwd() # remembering the current working folder
# Creating a web application object:
app = Flask(__name__, template_folder=folder, static_folder=folder) # the first parameter is the module name
                            # the parameter named static_folder defines the name of the folder containing the static files
                            # the parameter named template_folder defines the name of the folder containing the templates


app.add_url_rule('/', 'index', index, methods=['post', 'get'])   # creates a rule for the URL '/'
app.add_url_rule('/test', 'test', test) # creates a rule for the URL '/test'
app.add_url_rule('/result', 'result', result) # creates a rule for the URL '/test'
# Setting the encryption key:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'


if __name__ == "__main__":
    # Starting the web server:
    app.run()



