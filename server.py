from mysql.connector import MySQLConnection, Error


def set_connection():
	main_connector = MySQLConnection(host="localhost",
									 database="service_center",
									 user="root",
									 password="1234");
	ERROR_HANDLER = main_connector.is_connected()
	if ERROR_HANDLER == False:
		set_connection()
	return main_connector


def add_user(connector, login, password, FIO, passport, user_type, telephone=0):
	cursor = connector.cursor()
	try:
		cursor.execute(
			'insert into authentification values(default, "{login}", "{password}", {user_type})'.format(login=login,
																										password=password,
																										user_type=user_type))

		auth_id = cursor.lastrowid

		if user_type == "1":
			cursor.execute('insert into client values(default, {auth_id}, "{passport}", "{telephone}", "{fio}")'.format(
				auth_id=auth_id,
				passport=passport,
				telephone=telephone,
				fio=FIO))

		else:
			cursor.execute(
				'insert into employee values(default, {auth_id}, "{passport}", "{fio}")'.format(auth_id=auth_id,
																								passport=passport,
																								fio=FIO))
		connector.commit()

	except Exception as error:
		print(error)
		cursor.execute('delete from client where client_id={}'.format(cursor.lastrowid))
		cursor.execute('delete from authentification where auth_data_id={}'.format(auth_id))
		connector.commit()
		cursor.close()
		return -1

	user_id = cursor.lastrowid
	cursor.close()
	return user_id


def add_device(connector, client_id, device_type, device_model, device_password, device_problem, device_vendor):
	cursor = connector.cursor()
	try:
		cursor.execute('select client_id from client where client_id="{}"'.format(client_id))
		if cursor.fetchone() is not None:
			cursor.execute(
				'insert into device values(default, "{client_id}", "{device_type}", "{device_model}", "{device_password}", "{device_problem}", "{device_vendor}", "priemnyi otdel")'.format(
					client_id=client_id,
					device_type=device_type,
					device_model=device_model,
					device_password=device_password,
					device_problem=device_problem,
					device_vendor=device_vendor))
		else:
			return -1

		connector.commit()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	new_device_id = cursor.lastrowid
	cursor.close()
	return new_device_id


def add_order(connector, client_id, device_type, device_model, device_password, device_problem, device_vendor,
			  commentary):
	# type: (object, object, object, object, object, object, object, object) -> object
	device_id = add_device(connector, client_id, device_type, device_model, device_password, device_problem,
						   device_vendor)
	cursor = connector.cursor()
	try:
		if device_id != -1:
			cursor.execute(
				'insert into orders values(default, "{device_id}", curdate(), default, default, default, "{comment}")'.format(
					device_id=device_id,
					comment=commentary))
		else:
			return -1

		connector.commit()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	new_order_id = cursor.lastrowid
	cursor.close()
	return new_order_id

def update_order_total_price(connector, order_id, new_price):
	cursor = connector.cursor()
	cursor.execute('update orders set total_price={} where order_id={}'.format(new_price, order_id))
	connector.commit()
	cursor.close()
	return cursor.lastrowid

def set_order_ending_date(connector, order_id):
	cursor = connector.cursor()
	cursor.execute('update orders set ending_date=curdate() where order_id={}'.format(order_id))
	connector.commit()
	cursor.close()
	return cursor.lastrowid

def return_service_names_list(connector):
	cursor = connector.cursor()
	cursor.execute('select service_name from service_list')
	row = cursor.fetchone()
	service_names_list = []
	while row is not None:
		service_names_list.append(row[0])
		row = cursor.fetchone()
	return service_names_list


def get_service_by_name(connector, service_name):
	cursor = connector.cursor()
	try:
		cursor.execute('select service_id from service_list where service_name = "{}"'.format(service_name))
		service_id = cursor.fetchone()[0]

	except Exception as error:
		cursor.close()
		print(error)
		return -1

	cursor.close()
	return service_id


def return_employees_list(connector):
	cursor = connector.cursor()
	cursor.execute('select fio, employee_id from employee')
	row = cursor.fetchone()
	employees_names_and_ids_list = []
	while row is not None:
		employees_names_and_ids_list.append(row)
		row = cursor.fetchone()
	return employees_names_and_ids_list


def add_used_service(connector, order_id, service_name, employee_id, commentary):
	cursor = connector.cursor()
	try:
		service_id = get_service_by_name(connector, service_name)
		if service_id != -1:
			cursor.execute(
				'insert into used_services values(default, "{order_id}", "{service_id}", "{employee_id}", "{comment}")'.format(
					order_id=order_id,
					service_id=service_id,
					employee_id=employee_id,
					comment=commentary))
			connector.commit()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	new_used_service = cursor.lastrowid
	cursor.close()
	return new_used_service


def add_used_component(connector, order_id, name, price, supplier, bill):
	cursor = connector.cursor()
	try:
		cursor.execute(
			'insert into used_components_list values(default, "{order_id}", "{name}", "{price}", "{supplier}", "{bill}")'.format(
				order_id=order_id,
				name=name,
				price=price,
				supplier=supplier,
				bill=bill))
		connector.commit()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	new_component_id = cursor.lastrowid
	cursor.close()
	return new_component_id


def check_user(connector, login, password):
	cursor = connector.cursor()
	try:
		cursor.execute(
			'select auth_data_id, user_type from authentification where login="{}" and password="{}"'.format(login,
																											 password))
		user_id, user_type = cursor.fetchone()
		print(user_id, user_type)
		id_type = ""
		table_type = ""
		if user_type == "1":
			id_type = "client_id"
			table_type = "client"
		else:
			id_type = "employee_id"
			table_type = "employee"
		print(id_type,table_type)
		cursor.execute('select {} from {} where auth_data_id="{auth_data_id}"'.format(id_type,
																					  table_type,
																					  auth_data_id=user_id))
		user_id = cursor.fetchone()[0]

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	cursor.close()
	return user_id, user_type


def return_client_devices(connector, client_id):
	cursor = connector.cursor()
	list_of_devices = []
	try:
		cursor.execute('select * from device where client_id = {client_id}'.format(client_id=client_id))
		row = cursor.fetchone()
		while row is not None:
			list_of_devices.append(row)
			row = cursor.fetchone()
	except Exception as error:
		print(error)
		cursor.close()
		return -1
	cursor.close()
	return list_of_devices


def return_detailed_device_info(connector, device_id):
	cursor = connector.cursor()
	major_info = []
	services_list = []
	components_list = []
	try:
		cursor.execute(
			'select * from orders where device_id = {device_id}'.format(
				device_id=device_id))
		row = cursor.fetchone()
		major_info = [elem for elem in row]

		cursor.execute('select * from used_services where order_id = {order_id}'.format(
			order_id=major_info[0]))
		tmp = []
		row = cursor.fetchone()
		while row is not None:
			tmp.append(row)
			row = cursor.fetchone()

		for elem in tmp:
			cursor.execute('select * from service_list where service_id="{}"'.format(elem[2]))
			tmp_service = cursor.fetchone()
			cursor.execute('select * from employee where employee_id= "{}"'.format(elem[3]))
			tmp_employee = cursor.fetchone()
			services_list.append((tmp_service[1], tmp_employee[3], tmp_service[2], tmp_service[3]))

		cursor.execute(
			"select * from used_components_list where order_id={}".format(major_info[0]))
		row = cursor.fetchone()

		while row is not None:
			components_list.append(row)
			row = cursor.fetchone()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	cursor.close()
	return (major_info, services_list, components_list)


def return_orders(connector, filter):
	cursor = connector.cursor()
	orders = []
	try:
		if filter != "":
			cursor.execute('select device_id from device where status_id="{}"'.format(filter))
			tmp = cursor.fetchall()
			for elem in tmp:
				cursor.execute('select * from orders where device_id={}'.format(elem[0]))
				orders.append((cursor.fetchone()))
		else:
			cursor.execute('select * from orders')
			orders = cursor.fetchall()

	except Error as error:
		print(error)
		cursor.close()
		return -1

	return orders


def get_device_by_id(connector, device_id):
	cursor = connector.cursor()
	try:
		cursor.execute('select * from device where device_id = {}'.format(device_id))

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	return cursor.fetchone()


def return_client_info(connector, client_id):
	cursor = connector.cursor()
	try:
		cursor.execute('select * from client where client_id = "{}"'.format(client_id))

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	return cursor.fetchone()


def change_client_telephone(connector, client_id, new_telephone):
	cursor = connector.cursor()
	try:
		cursor.execute(
			'update client set telephone_number = "{telephone}" where client_id = {client_id}'.format(telephone=new_telephone,
																							   client_id=client_id))

		connector.commit()

	except Exception as error:
		print(error)
		cursor.close()
		return -1

	cursor.close()
	return 1


def change_device_status(connector, device_id, new_status):
	cursor = connector.cursor()
	try:
		cursor.execute(
			'update device set status_id = "{status}" where device_id = {id}'.format(status=new_status, id=device_id))

		connector.commit()
	except Exception as error:
		print(error)
		cursor.close()
		return -1

	return 1


def change_order_comment(connector, order_id, comment):
	cursor = connector.cursor()
	try:
		cursor.execute('update orders set comment = "{}" where order_id = {}'.format(comment, order_id))

		connector.commit()
	except Exception as error:
		print(error)
		cursor.close()
		return -1

	return 1


def generate_value(i):
	res = str(i)
	for _ in range(10 - len(str(i))):
		res += "0"
	return res


if __name__ == '__main__':
	connector = set_connection()
	login = "user_{number}".format(number=1)
	password = "{number}".format(number=1)
	fullname = "default name {number}".format(number=1)
	passport = "{number}".format(number=generate_value(1))
	telephone = "+7{number}".format(number=generate_value(1))
	user_info = check_user(connector, login, password)
	print(user_info)
	if user_info == -1:
		user_info = add_user(connector, login, password, fullname, passport, 1, telephone)
	order_id = add_order(connector, user_info[0], "телефон", "LG104396", "12345678", "проблемы с микрофоном, не работают кнопки громкости", "LG", "-")
	add_used_component(connector, order_id, "Экран", "10000", "магазин", "102234")
	list_of_d = return_client_devices(connector, user_info[0])
	for device in list_of_d:
		print(return_detailed_device_info(connector, device[0]))
	connector.close()
