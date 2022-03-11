from flask import Flask, render_template, request, redirect, send_file
from scrap import scrap

app = Flask('__name__')


@app.route('/')
def main():
    return render_template('main.html')


@app.errorhandler(500)
def page_not_founded(error):
    return render_template('error.html')


@app.route('/', methods=['GET', 'POST'])
def execute_scraping():
    if request.method == 'POST':
        keyword = request.form['keyword']
        start_page = int(request.form['start-page'])
        end_page = int(request.form['end-page'])
        columns = request.form.getlist('column')

        file_name = scrap(keyword, start_page, end_page, columns)

        return send_file(file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
