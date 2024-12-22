from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['STATIC_FOLDER'] = 'static'

class AddExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired()])
    expense_date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    criteria = SelectField('Select Criteria:', choices=[
        ('past_month', 'Past Month'),
        ('past_year', 'Past Year'),
        ('past_week', 'Past Week'),
        ('by_category', 'By Category')
    ])
    submit = SubmitField('Add Expense')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddExpenseForm()
    plot_url = None

    if form.validate_on_submit():
        amount = form.amount.data
        category = form.category.data
        expense_date = form.expense_date.data
        criteria = form.criteria.data

        conn = sqlite3.connect('expense_tracker.db')
        cursor = conn.cursor()

        # Insert the new expense
        cursor.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)',
                       (1, amount, category, expense_date))
        conn.commit()

        flash('Expense added successfully!', 'success')

        # Retrieve and plot expenses based on criteria
        if criteria == 'past_month':
            start_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = date.today().strftime('%Y-%m-%d')
        elif criteria == 'past_year':
            start_date = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')
            end_date = date.today().strftime('%Y-%m-%d')
        elif criteria == 'past_week':
            start_date = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = date.today().strftime('%Y-%m-%d')
        elif criteria == 'by_category':
            # Modify the query to group by category
            cursor.execute('SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category', (1,))
            expenses = cursor.fetchall()
            categories = [exp[0] for exp in expenses]
            amounts = [exp[1] for exp in expenses]

            plt.figure(figsize=(8, 4))
            plt.bar(categories, amounts)
            plt.xlabel('Categories')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category')

            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('index.html', form=form, plot_url=plot_url)

        conn.close()

        # Default criteria (Past Month)
        if not plot_url:
            start_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = date.today().strftime('%Y-%m-%d')

        cursor.execute('SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? GROUP BY category',
                       (1, start_date, end_date))
        expenses = cursor.fetchall()
        categories = [exp[0] for exp in expenses]
        amounts = [exp[1] for exp in expenses]

        plt.figure(figsize=(8, 4))
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Amount Spent')
        plt.title('Expenses by Category')

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', form=form, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
