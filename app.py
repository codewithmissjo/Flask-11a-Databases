from flask import Flask, render_template#, request, redirect, session
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
c = conn.cursor()

searchInfo = ""

def create_table():
  query = """CREATE TABLE IF NOT EXISTS
  products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity INTEGER,
    price DOUBLE
  )"""
  c.execute(query)

def add_item(name, quant, price):
  query = "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)"
  c.execute(query, (name, quant, price))
  conn.commit()

def get_one(name):
  query = "SELECT * FROM products WHERE name = ?"
  results = c.execute(query, (name, )).fetchone()
  return results

def get_all():
  query = "SELECT * FROM products"
  results = c.execute(query)
  print(results.fetchall())

def delete_item(name):
  query = "DELETE FROM products WHERE name = ?"
  c.execute(query, (name, ))
  conn.commit()

@app.route('/')
def index():
  query = "SELECT * FROM products"
  results = (c.execute(query)).fetchall()
  return render_template("index.html", data=results, searchResults=searchInfo)

@app.route('/search', methods=['POST'])
def search():
  global searchInfo
  name = request.form.get('pr-name')
  found = get_one(name)
  if found != None:
    searchInfo = found
  else:
    searchInfo = "Item not found"
  return redirect('/')

@app.route('/add', methods=["post"])
def add():
  # get form values
  # name
  name = request.form.get('add-name')
  # quantity
  quantity = request.form.get('add-quan')
  # price
  price = request.form.get('add-price')

  # add to database
  add_item(name, quantity, price)
  return redirect('/')

def main():
  create_table()
  if get_one("potato") == None:
    add_item("potato", 3, 0.03)
  if get_one("green beans") == None:
    add_item("green beans", 6, 0.05)
  if get_one("peppers") == None:
    add_item("peppers", 2, 0.09)

if __name__ == '__main__':
  main()
  app.run()
