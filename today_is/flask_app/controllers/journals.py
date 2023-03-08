from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.journal import Journal


@app.route('/dashboard')
def r_dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id']
        } 
    logged_in_user = User.get_by_id(data)
    journals = Journal.get_all_journals()
    theUser = User.get_all()
    return render_template("dashboard.html", logged_in_user = logged_in_user, journals = journals, users = theUser)

@app.route('/show/<int:journal_id>')
def r_one(journal_id):
    wrapped_user= {
        "id": session["user_id"]
    }
    logged_in_user = User.get_by_id(wrapped_user)
    theJournal = Journal.get_by_id(journal_id)
    theUser = User.get_all()
    return render_template("show.html", logged_in_user=logged_in_user, theJournal = theJournal, users = theUser)

@app.route('/new')
def r_new():
    user = User.get_by_id({'id': session['user_id']})
    return render_template("new.html", logged_in_user = user)

@app.route('/saveJournal', methods=['POST'])
def saveJournal():
    if not Journal.validate_new_journal(request.form):
        return redirect ('/new')
    data = {
        'what_happend': request.form['what_happend'],
        'new_symptom': request.form['new_symptom'],
        'tool_used': request.form['tool_used'],
        'effective': request.form['effective'],
        'user_id': session['user_id']
    }
    Journal.save_journal(data)
    return redirect('/dashboard')

@app.route("/edit/<int:journal_id>")
def edit_journal(journal_id):
    book = Journal.get_by_id(journal_id)
    wrapped_user = {
        "id": session['user_id']
    }
    logged_in_user = User.get_by_id(wrapped_user)
    return render_template('edit.html', logged_in_user = logged_in_user, journals = book)

@app.route("/editJournal/<int:journal_id>", methods=['POST'])
def journalEdit(journal_id):
    if not Journal.validate_new_journal(request.form):
        return redirect(f'/edit/{journal_id}')
    data = {
        'id': journal_id,
        'what_happend': request.form['what_happend'],
        'new_symptom': request.form['new_symptom'],
        'tool_used': request.form['tool_used'],
        'effective': request.form['effective'],
        'user_id': session['user_id']
    }
    Journal.update_journal(data)
    print("boop")
    return redirect("/dashboard")


@app.route("/deleteJournal/<int:journal_id>")
def delete_by_id(journal_id):
    Journal.delete_journal(journal_id)
    return redirect("/dashboard")

