# http://opentechschool.github.io/python-flask/
# https://flask-pymongo.readthedocs.io/en/latest/
# http://codehandbook.org/creating-a-web-app-using-angularjs-python-mongodb/
# https://api.mongodb.com/python/current/faq.html?highlight=flask
# https://www.tutorialspoint.com/flask/flask_quick_guide.htm

from flask import Flask, render_template

from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import ast

client = MongoClient()
app = Flask(__name__)
db = client['library']


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test')
def test():
	return json.dumps({'tomato':'hello'})

@app.route('/add_book/<string:title>/<string:authors>/<string:isbn>/<string:pagecount>')
def add_book(title, authors, isbn, pagecount):
	print("IN add_book")
	author_list = authors.split(',')
	jResults = json.dumps({'title':title, 'author':author_list,'ISBN':isbn, 'pgcount':str(pagecount)})
	coll = db['books']
	result = db.books.insert_one({'title':title, 'author':author_list,'ISBN':isbn, 'pgcount':str(pagecount)})
	return json.dumps({'Insert_output':str(result.inserted_id)})

@app.route('/commit_edit_book/<string:isbn>/<string:title>/<string:authors>/<string:pagecount>')
def commit_edit_book(isbn, title, authors, pagecount):
	author_list = authors.split(',')
	result = db.books.update_one({'ISBN':isbn}, { '$set': {'title': title, 'author':author_list, 'pgcount':str(pagecount)}})
	if title == 'x1234abc':
		db.books.update({'ISBN': isbn}, {'$unset': {'title':1}})
	if authors == 'x1234abc':
		db.books.update({'ISBN': isbn}, {'$unset': {'author':1}})
	if pagecount == 'x1234abc':
		db.books.update({'ISBN': isbn}, {'$unset': {'pgcount':1}})
	return json.dumps({'Updated_count': result.modified_count})

@app.route('/commit_edit_borrower/<string:username>/<string:name>/<string:phone>')
def commit_edit_borrower(username, name, phone):
	result = db.borrowers.update_one({'username': username}, {'$set' : {'name': name, 'phone': phone}})
	return json.dumps({'Updated_count': result.modified_count})

@app.route('/check_isbn/<string:isbn>')
def check_isbn(isbn):
	result = db.books.find({'ISBN':str(isbn)}).count()
	print(result)
	if(result == 0):
		return json.dumps({'result':'true'})
	else:
		return json.dumps({'result':'false'})

@app.route('/check_username/<string:username>')
def check_username(username):
	result = db.borrowers.find({'username':str(username)}).count()
	print(result)
	if(result == 0):
		return json.dumps({'result':'true'})
	else:
		return json.dumps({'result':'false'})

@app.route('/delete_book/<string:isbn>')
def delete_book(isbn):
	result = db.books.delete_one({'ISBN':isbn})
	if (result.deleted_count != 1):
		return json.dumps({'result':'Failed to delete book'})
	else :
		return json.dumps({'result':'Deleted book'})

@app.route('/delete_borrower/<string:username>')
def delete_borrower(username):
	result = db.borrowers.delete_one({'username':username})
	if (result.deleted_count != 1):
		return json.dumps({'result':'Failed to delete book'})
	else :
		return json.dumps({'result':'Deleted book'})

@app.route('/get_edit_book/<string:isbn>')
def get_edit_book(isbn):
	result = db.books.find_one({'ISBN': isbn})
	tempAuthor = "DNE"
	tempTitle = "DNE"
	tempPg = "DNE"
	if 'author' in result:
		tempAuthor = list(result['author'])
	if 'title' in result:
		tempTitle = result['title']
	if 'pgcount' in result:
		tempPg = result['pgcount']
	result_list = [tempTitle, tempAuthor, tempPg]
	return json.dumps({'result':result_list})

@app.route('/get_edit_borrower/<string:username>')
def get_edit_borrower(username):
	result = db.borrowers.find_one({'username': username})
	result_list = [result['name'], result['phone']]
	return json.dumps({'result':result_list})

@app.route('/get_book_isbn')
def get_book_isbn():
	coll = db.books.find({'checkedout': {'$exists' : False}})
	list_isbn = [];
	for c in coll:
		list_isbn.append(c['ISBN'])
	return json.dumps({'result': list_isbn})

@app.route('/get_books_checked_out')
def get_books_checked_out():
	coll = db.books.find({'checkedout': {'$exists': True}})
	list_coll = [];
	for c in coll:
		list_coll.append([c['checkedout'], c['ISBN']])
	return json.dumps({'result': list_coll})

@app.route('/get_users_count')
def user_track():
	coll = db.borrowers.find({'checkedout': {'$gt': -1}})
	list_coll = []
	for c in coll:
		list_coll.append([str(c['checkedout']), c['username']])
	return json.dumps({'result': list_coll})


@app.route('/search_book/<string:search_type>/<string:search>')
def search_book(search_type, search):
	output = db.books.find({str(search_type):{'$regex': search}}, {'_id':0})
	output_list = list(output);

	return json.dumps({'final': str(output_list)})


@app.route('/search_borrower/<string:search_type>/<string:search>')
def search_borrower(search_type, search):
	output  = db.borrowers.find({str(search_type):{'$regex': search}}, {'_id':0})
	return json.dumps({'final': str(list(output))})

@app.route('/sort_book/<string:attribute>')
def sort_book(attribute):
	output = db.books.find({}, {'_id':0}).sort(attribute,-1)
	return json.dumps({'final':str(list(output))})

@app.route('/add_borrower/<string:name>/<string:username>/<string:phone>')
def add_borrower(name, username, phone):
	result = db.borrowers.insert_one({'name':name, 'username':username, 'phone':phone, 'checkedout': 0})
	return json.dumps({'Insert_output':str(result.inserted_id)})

@app.route('/get_borrowers_username')
def get_borrowers_username():
	coll = db.borrowers.find({'checkedout': {'$eq': 0}})
	list_checkedout = [];
	for c in coll:
		list_checkedout.append(c['username'])
	return json.dumps({'result':list_checkedout})

@app.route('/get_all_borrowers_usernames')
def get_all_borrowers_usernames():
	coll = db.borrowers.find()
	list_bor = [];
	for c in coll:
		list_bor.append(c['username'])
	return json.dumps({'result':list_bor})

@app.route('/borrower_checkout/<string:username>/<string:isbn>')
def borrower_checkout(username, isbn):
	result = db.borrowers.update_one({'username':username}, {'$inc': {'checkedout': 1}})
	result2 = db.books.update_one({'ISBN': isbn}, {'$set': {'checkedout': username}})
	return json.dumps({'Checking_out': [result.modified_count, result2.modified_count]})

@app.route('/borrower_return/<string:isbn>/<string:username>')
def borrower_return(isbn,username):
	result = db.borrowers.update_one({'username':username}, {'$inc': {'checkedout': -1}})
	result2 = db.books.update_one({'ISBN': isbn}, {'$unset': {'checkedout': username}})
	return json.dumps({'Checking_out': [result.modified_count, result2.modified_count]})


if __name__ == '__main__':
	app.run()
