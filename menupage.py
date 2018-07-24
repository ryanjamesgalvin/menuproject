from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    restaurant = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurant = restaurant)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name = request.form['name'])
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    edit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        edit.name = request.form['name']
        session.add(edit)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurant = edit)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    delete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(delete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, restaurant = delete)


@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)
    
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id, restaurant = restaurant_id)
        
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editItem.name = request.form['name']
        editItem.price = request.form['price']
        editItem.description = request.form['description']
        session.add(editItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editItem)
    

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', i=itemToDelete)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
    connect_args={'check_same_thread':False}