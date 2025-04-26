from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# koneksi ke database RDS
connection = pymysql.connect(
    host='ecommerce-db.cjeg4okq6zjc.ap-southeast-1.rds.amazonaws.com',
    user='admin',
    password='Password123!',
    database='ecommerce'
)

@app.route('/')
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT name, price, image_url FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
