from flask import Blueprint, request, redirect, session, render_template, send_file
from models.db import get_db
from datetime import datetime
import csv
import io

trade_bp = Blueprint('trade', __name__)

def protect():
    if 'username' not in session:
        return redirect('/login')

@trade_bp.route('/', methods=['GET', 'POST'])
def index():
    check = protect()
    if check: return check

    db = get_db()
    collection = db['trades']
    capitals = db['capitals']
    username = session['username']

    if request.method == 'POST':
        equity = float(request.form['equity'])
        lot = float(request.form['lot'])
        open_price = float(request.form['open_price'])
        sl = float(request.form['sl'])
        tp = float(request.form['tp'])
        result = request.form['result']
        note = request.form['note']

        pip_value = 100 * lot

        if note == 'Buy':
            pnl = (tp - open_price) * pip_value if result == 'TP' else (sl - open_price) * pip_value
        else:
            pnl = (open_price - tp) * pip_value if result == 'TP' else (sl - open_price) * pip_value * -1

        equity_after = equity + pnl

        collection.insert_one({
            'username': username,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'equity': equity,
            'lot': lot,
            'open_price': open_price,
            'sl': sl,
            'tp': tp,
            'result': result,
            'note': note,
            'equity_after': equity_after
        })
        return redirect('/')

    trades = list(collection.find({'username': username}).sort("date", -1))
    modal = sum(x['amount'] for x in capitals.find({'username': username}))
    tp = sum(1 for x in trades if x['result'] == 'TP')
    sl = sum(1 for x in trades if x['result'] == 'SL')
    total = len(trades)
    winrate = round(tp / total * 100, 2) if total else 0
    growth = trades[0]['equity_after'] - modal if trades else 0

    stats = dict(tp=tp, sl=sl, total=total, winrate=winrate, growth=growth)
    return render_template('journal.html', trades=trades, stats=stats, modal=modal)

@trade_bp.route('/export')
def export():
    check = protect()
    if check: return check

    db = get_db()
    collection = db['trades']
    username = session['username']
    trades = list(collection.find({'username': username}).sort("date", -1))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Tanggal', 'Equity', 'Lot', 'Open', 'SL', 'TP', 'Hasil', 'Note', 'Equity After'])
    for t in trades:
        writer.writerow([t['date'], t['equity'], t['lot'], t['open_price'], t['sl'], t['tp'], t['result'], t['note'], t['equity_after']])

    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()), mimetype='text/csv', as_attachment=True, download_name='jurnal_trading.csv')
