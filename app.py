from flask import Flask, render_template#, request, redirect, session
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
c = conn.cursor()

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

@app.route('/')
def index():
  query = "SELECT * FROM products"
  results = (c.execute(query)).fetchall()
  return render_template("index.html", data=results)

def main():
  create_table()
  #get_all()
  if get_one("potato") == None:
    add_item("potato", 3, 0.03)
  #add_item("green beans", 6, 0.05)
  #add_item("peppers", 2, 0.09)

if __name__ == '__main__':
  main()
  app.run()