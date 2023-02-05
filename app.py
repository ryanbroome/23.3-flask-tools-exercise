from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

#//DELETE BEFORE SUBMIT
#todo WORKING THROUGH SOLUTION
#
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretpassword"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

survey = satisfaction_survey

@app.route("/")
def show_survey_start():
    """ Select a Survey"""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """ Save response and redirect to next question"""
    
    
    choice = request.form['answer']


    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        #user has answered all questions, thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)
    #// raise
    if(responses is None):
        #user trying to access question page early
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        #they have answered all questions, thank them
        return redirect("/complete")

    if(len(responses) != qid):
        #accessing qusetions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)



@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")






























# ATTEMPT 1 
# RESPONSES = []

# @app.route("/")
# def root():
#     return render_template('base.html')

# @app.route("/home")
# def base_page():
#     """
#     returns base page template, pulls title and instructions out of Survey obj passes to template
#     """
#     title = satisfaction_survey.title
#     instructions = satisfaction_survey.instructions
#     return render_template("home.html", title=title, instructions=instructions)

# @app.route("/questions/<int:id>", methods=["POST", "GET"])
# def show_form(id):
#     """selects question from survey and displays choices for that question"""
#     selected_question = satisfaction_survey.questions[id].question
#     selected_question_choices = satisfaction_survey.questions[id].choices
    
#     flash(f"Your question has been answered")
#     return render_template("questions.html", id=id, selected_question=selected_question, satisfaction_survey=satisfaction_survey, selected_question_choices=selected_question_choices)


# @app.route("/answers", methods=["POST", "GET"])
# def save_answers():
#     """ save answers to RESPONSES"""
#     question_count = len(satisfaction_survey.questions)
    
#     choice = request.form.get("choice")
#     RESPONSES.append(choice)
#     id = int(request.form["id"])
#     if id < (len(satisfaction_survey.questions) -1 ):
#         return redirect(f"/questions/{id +1}")
#     else: return redirect("/thanks")

# @app.route("/thanks")
# def show_thanks():
#     """ shows thanks message"""
#     survey_title = satisfaction_survey.title
#     responses = RESPONSES
#     return render_template("thanks.html", survey_title=survey_title, responses=responses)

# # ! Questions from app exercise
# # ? Line 34 "for some reason I kept getting a "method not allowed" error, what would cause the "method not allowed" error in this instance?"
# # ? Line 39  i used .get method incase a radio button isn't selected, will pass "None" as choice value, is this right?
# # ? Line Step 6 could not complete step 6, protecting questions. not sure what is meant by or how to do that. 
# # ? Line 42 id is sent as a hidden input on the form to get the index of the current question