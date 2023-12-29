from flask import Blueprint, render_template, redirect, url_for, request
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
    """
        Populate the select option with the tables that are available
    """
    tableForm = TableAssignmentForm()
    tables = Table.query.order_by(Table.number).all() # Get all the tables
    open_orders = Order.query.filter(Order.finished == False) # Getting all the orders that are not finished
    busy_table_ids = [order.table_id for order in open_orders] # Getting the table ids of the unfinished orders

    open_tables = [table for table in tables if table.id not in busy_table_ids] # Getting only the open tables
    tableForm.tables.choices = [(table.id,f"Table {table.number}")  for table in open_tables] # updating the choices  for tables

    """
        Populate the select option with servers details
    """
    servers = Employee.query.all()
    tableForm.servers.choices = [ (server.id, f"Server {server.name}") for server in servers]

    """
        Display your orders
    """
    your_orders = Order.query.filter(Order.finished == False).filter(Order.employee_id==current_user.id).all()
    """
        Calculate the total price of the open orders
    """
    for order in your_orders:
        total_price = 0
        for order_detail in order.order_details:
            item_price = order_detail.menu_items.price
            total_price += item_price
        order.price = total_price

    """
        Display the list of menu items
    """
    menu_item_form = MenuItemAssignmentForm()
    # menu_item_types = MenuItemType.query.all()
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name)
    menu_item_form.menu_items.choices = [(item.id,item) for item in menu_items]

    if tableForm.validate_on_submit():
        table = tableForm.tables.data
        server = tableForm.servers.data
        return redirect(url_for('orders.assign_table',table=table, server=server))
    return render_template("orders.html", tableForm = tableForm, menu_item_form= menu_item_form, your_orders = your_orders)


@bp.route("/assigntable/<table>/<server>")
@login_required
def assign_table(table,server):
    from app import db
    # Creating a new order with the table and server id
    newOrder = Order(employee_id = server, table_id = table, finished = False)
    db.session.add(newOrder)
    db.session.commit()
    return redirect(url_for('orders.index'))


@bp.route("/closetable/<order_id>", methods=["POST"])
@login_required
def close_table(order_id):
    from app import db
    # Closing the order by chnaging the finished status in the order table
    current_order = Order.query.filter(Order.id == order_id).first()
    current_order.finished = True
    db.session.commit()
    return redirect(url_for('orders.index'))

@bp.route("/addorder/<order_id>", methods=["POST"])
@login_required
def add_to_order(order_id):
    from app import db
    selected_items = request.form.getlist('checkbox')
    order = Order.query.get(order_id)
    for item_id in selected_items:
        item = MenuItem.query.get(item_id)
        orderDetail = OrderDetail(order_id=order_id,menu_item_id=item_id, menu_items=item,orders=order)
        db.session.add(orderDetail)
    db.session.commit()
    return redirect(url_for('orders.index'))

"""
3 endpoints:
1. Assign Table
2. Close Table
3. Add to Order
"""
