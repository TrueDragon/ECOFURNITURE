from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from Forms import CreateUserForm, CreateCustomerForm, CreateFurnitureForm, PaymentForm, ReportForm, OrderForm, DiscountForm
import shelve
from User import User
import Customer
import Furniture
import Pay
import Order
import Report
import os
import Discount
from flask import request

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/retrieveReport')
def retrieveReport():
    return render_template('retrieveReport.html')



@app.route('/createDiscount', methods=['GET', 'POST'])
def create_discount():
    discount_form = DiscountForm(request.form)
    if request.method == 'POST' and discount_form.validate():
        discount_dict = {}
        db = shelve.open('discount.db', 'c')

        try:
            discount_dict = db['Info']
        except:
            print("Error in retrieving Users from discount.db.")

        discount = Discount.Discount(discount_form.code.data, discount_form.amount.data)

        discount_dict[discount.get_id()] = discount
        db['Info'] = discount_dict

        db.close()

        return redirect(url_for('retrieve_discount'))
    return render_template('createDiscount.html', form=discount_form)

@app.route('/retrieveDiscount')
def retrieve_discount():
    discount_dict = {}
    db = shelve.open('discount.db', 'r')
    discount_dict = db['Info']
    db.close()

    discount_list = []
    for key in discount_dict.keys():
        discount = discount_dict.get(key)
        discount_list.append(discount)

    return render_template('retrieveDiscount.html', count=len(discount_list), discount_list=discount_list)

@app.route('/updateDiscount/<int:id>/', methods=['GET', 'POST'])
def update_discount(id):
    update_discount_form = DiscountForm(request.form)
    if request.method == 'POST' and update_discount_form.validate():
        discount_dict = {}
        db = shelve.open('discount.db', 'w')
        discount_dict = db['Info']

        discount = discount_dict.get(id)
        discount.set_code(update_discount_form.code.data)
        discount.set_amount(update_discount_form.amount.data)

        db['Info'] = discount_dict
        db.close()

        return redirect(url_for('retrieve_discount'))

    else:
        discount_dict = {}
        db = shelve.open('discount.db', 'r')
        discount_dict = db['Info']
        db.close()

        discount = discount_dict.get(id)
        update_discount_form.code.data = discount.get_code()
        update_discount_form.amount.data = discount.get_amount()
        return render_template('updateDiscount.html', form=update_discount_form)

@app.route('/deleteDiscount/<int:id>', methods=['POST'])
def delete_discount(id):
    discount_dict = {}
    db = shelve.open('discount.db', 'w')
    discount_dict = db['Info']

    discount_dict.pop(id)

    db['Info'] = discount_dict
    db.close()

    return redirect(url_for('retrieve_discount'))






@app.route('/cart', methods=['GET', 'POST'])
def cart():
    subtotal_value = 100
    shipping_fee = 15
    # Handle POST request when the form is submitted
    if request.method == 'POST':
        discount_code = request.form.get('discount_code').strip()  # Remove leading and trailing whitespaces

        # Retrieve discount from database
        db = shelve.open('discount.db', 'r')
        discount_dict = db.get('Info', {})
        db.close()

        # Check if the discount code exists in the database (case-sensitive)
        if any(discount.get_code() == discount_code for discount in discount_dict.values()):
            for discount in discount_dict.values():
                if discount.get_code() == discount_code:
                    discount_amount = discount.get_amount()
                    subtotal_value -= discount_amount  # Subtract discount amount from subtotal
                    flash(f'Discount of ${discount_amount} applied successfully!')
                    break
        else:
            flash('Invalid discount code. Please try again.')
    return render_template('cart.html', subtotal_value=subtotal_value, shipping_fee=shipping_fee)



@app.route('/ikeacreation', methods=['GET', 'POST'])
def ikeaCreation():
    if request.method == 'POST':
        with shelve.open('userbear.db', writeback=True) as db:
            user_id = str(max(map(int, db.keys()), default=0) + 1)
            db[user_id] = {
                'username': request.form['username'],
                'password': request.form['password'],
                'user_type': request.form['user_type']
            }
        return render_template('login.html')

    return render_template('ikeacreation.html')
@app.route('/createUser')
def createUser():
    return render_template('ikeacreation.html')


@app.route('/retrieveUsers', methods=['GET', 'POST'])
def retrieve_users():
    users_list = []
    with shelve.open('userbear.db') as db:
        users_list = list(db.items())
    return render_template('retrieveUsers.html', users_list=users_list)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    with shelve.open('userbear.db', writeback=True) as db:
        if str(user_id) in db:
            del db[str(user_id)]
    return redirect(url_for('retrieve_users'))







def register_user(username, password):
    with shelve.open('userbear.db', writeback=True) as db:
        if any(user_info['username'] == username for user_info in db.values()):
            error = 'Username already taken. Please choose another one.'
            return render_template('register.html', error=error)
        user_id = str(max(map(int, db.keys()), default=0) + 1)
        db[user_id] = {
            'username': username,
            'password': password,
            'user_type': 'user'
        }

def authenticate_user(username, password):
    with shelve.open('userbear.db') as db:
        for user_info in db.values():
            if user_info['username'] == username and user_info.get('password') == password:
                return user_info
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with shelve.open('userbear.db') as db:
            user_info = authenticate_user(username, password)
            if user_info:

                if user_info['user_type'] == 'admin':
                    session['admin'] = True
                    return redirect(url_for('home'))
                else:
                    session['username'] = username
                    return redirect(url_for('products'))
            else:
                error = 'Invalid username or password'
                return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        register_result = register_user(username, password)

        if isinstance(register_result, str):
            return register_result

        return redirect(url_for('login'))

    return render_template('register.html', error=None)

@app.route('/passchange', methods=['GET', 'POST'])
def passchange():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        with shelve.open('userbear.db', writeback=True) as db:
            user_info = next((info for info in db.values() if info['username'] == username), None)
            if user_info and user_info.get('password') == current_password:
                if new_password == confirm_password:
                    user_info['password'] = new_password
                    session['username'] = username
                    return redirect(url_for('products'))
                else:
                    error = 'New password and confirm password do not match'
            else:
                error = 'Incorrect current password'
            return render_template('account.html', error=error)

    return render_template('account.html')

@app.route('/')
def default():
    return render_template('products.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/living_room')
def living_room():
    query = request.args.get('query', '')
    reset = request.args.get('reset')

    if reset:
        query = ''

    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        if query.lower() in furniture.get_furniture_name().lower():
            furniture_list.append(furniture)

    return render_template('living_room.html', count=len(furniture_list), furniture_list=furniture_list, query=query)


@app.route('/bedroom')
def bedroom():
    query = request.args.get('query', '')
    reset = request.args.get('reset')

    if reset:
        query = ''

    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        if query.lower() in furniture.get_furniture_name().lower():
            furniture_list.append(furniture)

    return render_template('bedroom.html', count=len(furniture_list), furniture_list=furniture_list, query=query)

@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('products'))

@app.route('/signoutadmin')
def signoutadmin():
    session.pop('admin', None)
    return redirect(url_for('products'))

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')

@app.route('/dining_room')
def dining_room():
    query = request.args.get('query', '')
    reset = request.args.get('reset')

    if reset:
        query = ''

    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        if query.lower() in furniture.get_furniture_name().lower():
            furniture_list.append(furniture)

    return render_template('dining_room.html', count=len(furniture_list), furniture_list=furniture_list, query=query)


@app.route('/office')
def office():
    query = request.args.get('query', '')
    reset = request.args.get('reset')

    if reset:
        query = ''

    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        if query.lower() in furniture.get_furniture_name().lower():
            furniture_list.append(furniture)

    return render_template('office.html', count=len(furniture_list), furniture_list=furniture_list, query=query)


@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")
        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.membership.data,
                                     create_customer_form.remarks.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data, create_customer_form.address.data)
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)

@app.route('/createFurniture', methods=['GET', 'POST'])
def create_furniture():
    create_furniture_form = CreateFurnitureForm(request.form)
    if request.method == 'POST' and create_furniture_form.validate():
        furniture_dict = {}
        db = shelve.open('furniture.db', 'c')

        try:
            furniture_dict = db['Furniture']
        except:
            print("Error in retrieving Users from user.db.")

        furniture = Furniture.Furniture(create_furniture_form.furniture_type.data,
                                        create_furniture_form.furniture_name.data,
                                        create_furniture_form.furniture_quantity.data,
                                        create_furniture_form.furniture_category.data,
                                        create_furniture_form.furniture_status.data,
                                        create_furniture_form.furniture_price.data,
                                        create_furniture_form.furniture_remarks.data)
        furniture_dict[furniture.get_furniture_id()] = furniture
        db['Furniture'] = furniture_dict

        db.close()

        return redirect(url_for('retrieve_furniture'))
    return render_template('createFurniture.html', form=create_furniture_form)

@app.route('/createpayment', methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm(request.form)
    if request.method == 'POST' and payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'c')
        try:
            payment_dict = db['Info']
        except:
            print("Error in retrieving Users from user.db.")

        payment = Pay.Payment(payment_form.first_name.data, payment_form.last_name.data, payment_form.card_no.data,
                              payment_form.exp.data, payment_form.cvv.data)

        payment_dict[payment.get_cust_id()] = payment
        db['Info'] = payment_dict

        db.close()

        return redirect(url_for('retrieve_payment'))
    return render_template('createpayment.html', form=payment_form)


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)



@app.route('/retrieveFurniture')
def retrieve_furniture():
    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        furniture_list.append(furniture)

    return render_template('retrieveFurniture.html', count=len(furniture_list), furniture_list=furniture_list)


@app.route('/retrievePayment')
def retrieve_payment():
    payment_dict = {}
    db = shelve.open('payment.db', 'r')
    payment_dict = db['Info']
    db.close()

    payment_list = []
    for key in payment_dict.keys():
        payment = payment_dict.get(key)
        payment_list.append(payment)

    return render_template('retrievePayment.html', count=len(payment_list), payment_list=payment_list)
'''
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)
'''
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.remarks.data = customer.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)

@app.route('/updateFurniture/<int:id>/', methods=['GET', 'POST'])
def update_furniture(id):
    update_furniture_form = CreateFurnitureForm(request.form)
    if request.method == 'POST' and update_furniture_form.validate():
        furniture_dict = {}
        db = shelve.open('furniture.db', 'w')
        furniture_dict = db['Furniture']

        furniture = furniture_dict.get(id)
        furniture.set_furniture_type(update_furniture_form.furniture_type.data)
        furniture.set_furniture_name(update_furniture_form.furniture_name.data)
        furniture.set_furniture_quantity(
            update_furniture_form.furniture_quantity.data)
        furniture.set_furniture_category(
            update_furniture_form.furniture_category.data)
        furniture.set_furniture_status(
            update_furniture_form.furniture_status.data)
        furniture.set_furniture_price(
            update_furniture_form.furniture_price.data)
        furniture.set_furniture_remarks(
            update_furniture_form.furniture_remarks.data)

        db['Furniture'] = furniture_dict
        db.close()

        return redirect(url_for('retrieve_furniture'))

    else:
        furniture_dict = {}
        db = shelve.open('furniture.db', 'r')
        furniture_dict = db['Furniture']
        db.close()

        furniture = furniture_dict.get(id)
        update_furniture_form.furniture_type.data = furniture.get_furniture_type()
        update_furniture_form.furniture_name.data = furniture.get_furniture_name()
        update_furniture_form.furniture_quantity.data = furniture.get_furniture_quantity()
        update_furniture_form.furniture_category.data = furniture.get_furniture_category()
        update_furniture_form.furniture_status.data = furniture.get_furniture_status()
        update_furniture_form.furniture_price.data = furniture.get_furniture_price()
        update_furniture_form.furniture_remarks.data = furniture.get_furniture_remarks()

        return render_template('updateFurniture.html', form=update_furniture_form)

@app.route('/updatePayment/<int:id>/', methods=['GET', 'POST'])
def update_payment(id):
    update_payment_form = PaymentForm(request.form)
    if request.method == 'POST' and update_payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'w')
        payment_dict = db['Info']

        payment = payment_dict.get(id)
        payment.set_first_name(update_payment_form.first_name.data)
        payment.set_last_name(update_payment_form.last_name.data)
        payment.set_card_no(update_payment_form.card_no.data)
        payment.set_exp(update_payment_form.exp.data)
        payment.set_cvv(update_payment_form.cvv.data)

        db['Info'] = payment_dict
        db.close()

        return redirect(url_for('retrieve_payment'))
    else:
        payment_dict = {}
        db = shelve.open('payment.db', 'r')
        payment_dict = db['Info']
        db.close()

        payment = payment_dict.get(id)
        update_payment_form.first_name.data = payment.get_first_name()
        update_payment_form.last_name.data = payment.get_last_name()
        update_payment_form.card_no.data = payment.get_card_no()
        update_payment_form.exp.data = payment.get_exp()
        update_payment_form.cvv.data = payment.get_cvv()
        return render_template('updatePayment.html', form=update_payment_form)



@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))

@app.route('/deleteFurniture/<int:id>', methods=['POST'])
def delete_furniture(id):
    furniture_dict = {}
    db = shelve.open('furniture.db', 'w')
    furniture_dict = db['Furniture']

    furniture_dict.pop(id)

    db['Furniture'] = furniture_dict
    db.close()

    return redirect(url_for('retrieve_furniture'))

@app.route('/deletePayment/<int:id>', methods=['POST'])
def delete_payment(id):
    payment_dict = {}
    db = shelve.open('payment.db', 'w')
    payment_dict = db['Info']

    payment_dict.pop(id)

    db['Info'] = payment_dict
    db.close()

    return redirect(url_for('retrieve_payment'))

@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    create_order_form = OrderForm(request.form)
    if request.method == 'POST' and create_order_form.validate():
        orders_dict = {}
        db = shelve.open('order.db', 'c')

        try:
            orders_dict = db['Orders']
        except:
            print("Error in retriving Orders from order.db")

        order = Order.Order(create_order_form.customer_id.data,
                            create_order_form.item_id.data, create_order_form.item_quantity.data)
        orders_dict[order.get_customer_id()] = order
        db['Orders'] = orders_dict

        db.close()
        return redirect(url_for('retrieve_orders'))
    return render_template('createOrder.html', form=create_order_form)

@app.route('/retrieveOrders')
def retrieve_orders():
    orders_dict = {}
    db = shelve.open('order.db', 'r')
    orders_dict = db['Orders']
    db.close()

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    return render_template('retrieveOrders.html', count=len(orders_list), orders_list=orders_list)

@app.route('/updateOrder/<id>', methods=['GET', 'POST'])
def update_order(id):
    update_order_form = OrderForm(request.form)
    if request.method == 'POST' and update_order_form.validate():
        orders_dict = {}
        db = shelve.open('order.db', 'w')
        orders_dict = db['Orders']

        order = orders_dict.get(id)
        order.set_customer_id(update_order_form.customer_id.data)
        order.set_item_id(update_order_form.item_id.data)
        order.set_item_quantity(update_order_form.item_quantity.data)

        db['Orders'] = orders_dict
        db.close()

        return redirect(url_for('retrieve_orders'))
    else:
        orders_dict = {}
        db = shelve.open('order.db', 'r')
        orders_dict = db['Orders']
        db.close()

        order = orders_dict.get(id)
        update_order_form.customer_id.data = order.get_customer_id()
        update_order_form.item_id.data = order.get_item_id()
        update_order_form.item_quantity.data = order.get_item_quantity()

        return render_template('updateOrder.html', form=update_order_form)

@app.route('/deleteOrder/<id>', methods=['POST'])
def delete_order(id):
    order_dict = {}
    db = shelve.open('order.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('retrieve_orders'))

@app.route('/createReport', methods=['GET', 'POST'])
def create_report():
    form = ReportForm(request.form)
    if request.method == 'POST' and form.validate():
        report_dict = {}
        db = shelve.open('report.db', 'c')

        try:
            report_dict = db['Report']
        except:
            print("Error in submiting report")

        report = Report.Report(
            form.report_id.data, form.customer_id.data, form.employee_id.data, form.item_id.data, form.quantity.data,
            form.total_price.data, form.report_date.data, form.report_type.data, form.remarks.data)
        report_dict[report.get_report_id()] = report
        db['Report'] = report_dict

        db.close()
        return redirect(url_for('retrieve_reports'))
    return render_template('createReport.html', form=form)

@app.route('/retrieveReports')
def retrieve_reports():
    report_dict = {}
    db = shelve.open('report.db', 'r')
    report_dict = db['Report']
    db.close()

    report_list = []
    for key in report_dict:
        report = report_dict.get(key)
        report_list.append(report)

    return render_template('retrieveReports.html', count=len(report_list), report_list=report_list)

@app.route('/updateReport/<id>', methods=['GET', 'POST'])
def update_report(id):
    form = ReportForm(request.form)
    if request.method == 'POST' and form.validate():
        report_dict = {}
        db = shelve.open('report.db', 'w')
        report_dict = db['Report']

        report = report_dict.get(id)
        report.set_report_id(form.report_id.data)
        report.set_customer_id(form.customer_id.data)
        report.set_employee_id(form.employee_id.data)
        report.set_item_id(form.item_id.data)
        report.set_quantity(form.quantity.data)
        report.set_total_price(form.total_price.data)
        report.set_report_date(form.report_date.data)
        report.set_report_type(form.report_type.data)
        report.set_remarks(form.remarks.data)

        db['Report'] = report_dict
        db.close()

        return redirect(url_for('retrieve_reports'))
    else:
        report_dict = {}
        db = shelve.open('report.db', 'r')
        report_dict = db['Report']
        db.close()

        report = report_dict.get(id)
        form.report_id.data = report.get_report_id()
        form.customer_id.data = report.get_customer_id()
        form.employee_id.data = report.get_employee_id()
        form.item_id.data = report.get_item_id()
        form.quantity.data = report.get_quantity()
        form.total_price.data = report.get_total_price()
        form.report_date.data = report.get_report_date()
        form.report_type.data = report.get_report_type()
        form.remarks.data = report.get_remarks()

        return render_template('updateReport.html', form=form)

@app.route('/deleteReport/<id>', methods=['POST'])
def delete_report(id):
    report_dict = {}
    db = shelve.open('report.db', 'w')
    report_dict = db['Report']

    report_dict.pop(id)

    db['Report'] = report_dict
    db.close()

    return redirect(url_for('retrieve_reports'))

if __name__ == '__main__':
    app.run(debug=True)