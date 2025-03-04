from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Создаем приложение Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruiter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных
db = SQLAlchemy(app)

# Модель кандидата
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    resume_path = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Новый')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))
    source = db.Column(db.String(50), default='Другое')  # Telegram или другой источник
    specializations = db.Column(db.String(200))  # Хранение специализаций через запятую
    telegram_username = db.Column(db.String(100))  # Добавляем поле для username в Telegram

    def set_specializations(self, specs_list):
        if specs_list:
            self.specializations = ','.join(specs_list)
        else:
            self.specializations = ''

    def get_specializations(self):
        return self.specializations.split(',') if self.specializations else []

# Модель вакансии
class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Открыта')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='vacancy', lazy=True)

@app.route('/')
def index():
    return render_template('index.html')

# Маршруты для кандидатов
@app.route('/candidates')
def candidates():
    candidates_list = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates_list)

@app.route('/candidate/add', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        candidate = Candidate(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            status=request.form['status'],
            source=request.form['source']
        )
        candidate.set_specializations(request.form.getlist('specializations'))
        db.session.add(candidate)
        db.session.commit()
        flash('Кандидат успешно добавлен', 'success')
        return redirect(url_for('candidates'))
    return render_template('add_candidate.html')

@app.route('/candidate/<int:id>')
def view_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    return render_template('view_candidate.html', candidate=candidate)

@app.route('/candidate/<int:id>/edit', methods=['GET', 'POST'])
def edit_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    if request.method == 'POST':
        candidate.name = request.form['name']
        candidate.email = request.form['email']
        candidate.phone = request.form['phone']
        candidate.status = request.form['status']
        candidate.set_specializations(request.form.getlist('specializations'))
        db.session.commit()
        flash('Кандидат успешно обновлен', 'success')
        return redirect(url_for('candidates'))
    return render_template('edit_candidate.html', candidate=candidate)

@app.route('/candidate/<int:id>/resume')
def download_resume(id):
    candidate = Candidate.query.get_or_404(id)
    if candidate.resume_path and os.path.exists(candidate.resume_path):
        return send_file(candidate.resume_path, as_attachment=True)
    flash('Резюме не найдено', 'error')
    return redirect(url_for('view_candidate', id=id))

# Маршруты для вакансий
@app.route('/vacancies')
def vacancies():
    vacancies_list = Vacancy.query.all()
    return render_template('vacancies.html', vacancies=vacancies_list)

@app.route('/vacancy/add', methods=['GET', 'POST'])
def add_vacancy():
    if request.method == 'POST':
        vacancy = Vacancy(
            title=request.form['title'],
            description=request.form['description'],
            status=request.form['status']
        )
        db.session.add(vacancy)
        db.session.commit()
        flash('Вакансия успешно добавлена', 'success')
        return redirect(url_for('vacancies'))
    return render_template('add_vacancy.html')

@app.route('/vacancy/<int:id>')
def view_vacancy(id):
    vacancy = Vacancy.query.get_or_404(id)
    return render_template('view_vacancy.html', vacancy=vacancy)

@app.route('/vacancy/<int:id>/edit', methods=['GET', 'POST'])
def edit_vacancy(id):
    vacancy = Vacancy.query.get_or_404(id)
    if request.method == 'POST':
        vacancy.title = request.form['title']
        vacancy.description = request.form['description']
        vacancy.status = request.form['status']
        db.session.commit()
        flash('Вакансия успешно обновлена', 'success')
        return redirect(url_for('vacancies'))
    return render_template('edit_vacancy.html', vacancy=vacancy)

@app.route('/vacancy/<int:id>/candidates')
def candidates_for_vacancy(id):
    vacancy = Vacancy.query.get_or_404(id)
    return render_template('candidates.html', candidates=vacancy.candidates, vacancy=vacancy)

# Создаем базу данных при запуске приложения
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 