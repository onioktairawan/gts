from flask import Blueprint, request, redirect, session, render_template
from models.db import get_db
from datetime import datetime

capital_bp = Blueprint('capital', __name__)

@capital_bp.route('/add_modal', methods=['GET', 'POST'])
def add_modal():
    if 'username' not in session:
        return redirect('/login')

    db = get_db()
    capitals = db['capitals']

    if request.method == 'POST':
        amount = float(request.form['amount'])
        capitals.insert_one({
            'username': session['username'],
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return redirect('/')

    return render_template('add_modal.html')
