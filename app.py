from flask import Flask, render_template

app = Flask(__name__)

user = {
    'username': 'Xevion',
    'logged_in': False
}


@app.route('/')
def index():  # put application's code here
    return render_template('layouts/index.html', user=user)


@app.route('/about')
def about():
    return render_template('pages/about.html', user=user)

@app.route('/users')
def browse():
    return render_template('pages/browse.html', user=user)

@app.route('/feed')
def feed():
    return render_template('pages/feed.html', user=user)

@app.route('/messages')
def messages():
    return render_template('pages/messages.html', user=user)

@app.route('/search')
def search():
    return render_template('pages/search.html', user=user)

@app.route('/user/<username>')
def user(username: str):
    return render_template('pages/about.html', user=user)

@app.route('/blogs')
def blogs():
    return render_template('pages/blogs.html', user=user)

@app.route('/groups')
def groups():
    return render_template('pages/groups.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
