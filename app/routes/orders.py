from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.forms import TableAssignmentForm, MenuItemAssignmentForm
from app.models import Table, Order, Employee, OrderDetail, MenuItem, MenuItemType

bp = Blueprint("orders",__name__,url_prefix="")

@bp.route("/", methods=["GET","POST"])
@login_required
def index():
    """
    Table assignment form
    """
    tableForm = TableAssignmentForm()
    tables = Table.query.order_by(Table.number).all() # Get all the tables
    open_orders = Order.query.filter(Order.finished == False) # Getting all the orders that are not finished
    busy_table_ids = [order.table_id for order in open_orders] # Getting of the gtable id of the unfinished orders

    open_tables = [table for table in tables if table.id not in busy_table_ids] # Getting only the open tables
    tableForm.tables.choices = [(table.id,f"Table {table.number}")  for table in open_tables] # updating the choices  for tables

    servers = Employee.query.all()
    tableForm.servers.choices = [ (server.id, f"Server {server.name}") for server in servers]

    """
    Display your orders
    """
    your_orders = Order.query.filter(Order.finished == False).filter(Order.employee_id==current_user.id)

    """
    Display the list of menu items
    """
    menu_item_form = MenuItemAssignmentForm()
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name)
    menu_item_form.choices = [(item.id,'') for item in MenuItem.query.all()]
    print(menu_item_form.choices)

    if tableForm.validate_on_submit():
        table = tableForm.tables.data
        server = tableForm.servers.data
        return redirect(url_for('orders.assign_table',table=table, server=server))
    return render_template("orders.html", tableForm = tableForm, your_orders = your_orders, menu_item_form= menu_item_form, menu_items=menu_items)


@bp.route("/assigntable/<table>/<server>")
@login_required
def assign_table(table,server):
    from app import db
    print(table,server)
    newOrder = Order(employee_id = server, table_id = table, finished = False)
    db.session.add(newOrder)
    db.session.commit()
    return redirect(url_for('orders.index'))


@bp.route("/closetable/<order_id>")
@login_required
def close_table(order_id):
    from app import db
    print(order_id)
    current_order = Order.query.filter(Order.id == order_id).first()
    current_order.finished = True
    db.session.commit()
    return redirect(url_for('orders.index'))

@bp.route("/addorder/<order_id>/<item_ids>")
@login_required
def add_to_order(order_id,item_ids):
    from app import db
    items = item_ids.split(",")
    for item in items:
        print(item)
        order = OrderDetail(order_id = order_id, menu_item_id=item)
        db.session.add(order)
    db.session.commit()
    return redirect(url_for('orders.index'))

"""
3 endpoints:
1. Assign Table
2. Close Table
3. Add to Order
"""
