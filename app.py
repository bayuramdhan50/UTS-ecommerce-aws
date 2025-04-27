from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Student Information
STUDENT_NAME = "Bayu Ramdhan Ardiyanto"
STUDENT_NRP = "152022082"

# Function to get database connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='ecommerce-db.cjeg4okq6zjc.ap-southeast-1.rds.amazonaws.com',
            user='admin',
            password='Password123!',
            database='ecommerce'
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, price, image_url FROM products")
            products = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('index.html', 
                                  products=products, 
                                  student_name=STUDENT_NAME, 
                                  student_nrp=STUDENT_NRP)
        except Exception as e:
            logger.error(f"Database query error: {e}")
            connection.close()
            return render_template('error.html', error=str(e))
    else:
        return render_template('error.html', error="Failed to connect to database")

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image_url = request.form['image_url']
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO products (name, price, image_url) VALUES (%s, %s, %s)",
                    (name, price, image_url)
                )
                connection.commit()
                cursor.close()
                connection.close()
                flash('Product added successfully!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                logger.error(f"Error adding product: {e}")
                connection.close()
                flash(f'Error adding product: {str(e)}', 'error')
                return redirect(url_for('add_product'))
        else:
            flash('Database connection error', 'error')
            return redirect(url_for('add_product'))
    
    return render_template('add_product.html', 
                          student_name=STUDENT_NAME, 
                          student_nrp=STUDENT_NRP)

@app.route('/about')
def about():
    return render_template('about.html', 
                          student_name=STUDENT_NAME, 
                          student_nrp=STUDENT_NRP)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)