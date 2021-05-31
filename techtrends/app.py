import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

import logging

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.logger.setLevel(logging.INFO)

# Variable to keep track of number of connections made to the Database
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    global db_connection_count
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    db_connection_count += 1
    return post

# Define the main route of the web application 
@app.route('/')
def index():
    global db_connection_count
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    db_connection_count += 1
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(f'A Non-Existng article with id: {post_id} is accessed')
        return render_template('404.html'), 404
    else:
        app.logger.info(f'Article: {post[2]} with id: {post_id} is accessed')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('<About Us> page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            global db_connection_count
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            db_connection_count += 1

            app.logger.info(f'A new Article: {title} is created')

            return redirect(url_for('index'))


    return render_template('create.html')

# Endpoint for Application Health Check
@app.route('/healthz')
def health_check():
    response = app.response_class(
            response=json.dumps({"result" : "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    app.logger.info('HealthCheck Endpoint is called - Application state is <HEALTHY>.')
    return response

# Function to get total posts count in the DB
def get_total_posts_count():
    global db_connection_count
    connection = get_db_connection()
    posts_count = connection.execute('SELECT count(*) FROM posts').fetchone()[0]
    connection.close()
    db_connection_count += 1

    return posts_count

# Endpoint for collections Total DB Connections and Total Posts Count metris
@app.route('/metrics')
def metrics():
    posts_count = get_total_posts_count()
    response_data = {"db_connection_count": str(db_connection_count), "post_count": str(posts_count)}
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )

    app.logger.info('Metrics API is called.')

    return response

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')