from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import server
screen_res = (1920, 1080)
statuses_dict = {'priemnyi otdel':'Приемный отдел',
				 'iz priemki v remont':'Приемка -> Ремонт',
				 'diagnostika':'Диагностика',
				 'remont':'Ремонт',
				 'iz remonta v priemky':'Ремонт -> Приемка',
				 'gotovo k vydache klienty':'Готово к выдаче клиенту',
				 'remont zavershen':'Ремонт завершен'}

class AuthWindow:
	def __init__(self):
		self.parent = Tk()
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13)
		self.width = 290
		self.height = 190
		self.mainFrame = Frame(self.parent)
		self.additionalFrame = Frame(self.parent)
		self.connector = server.set_connection()
		self.initUI()
		self.parent.mainloop()

	def data_handler(self, user_data):
		for elem in user_data:
			if elem == "":
				messagebox.showerror("Ошибка авторизации", "Такого пользователя не существует")
				return
		info = server.check_user(self.connector,
								 user_data[0],
								 user_data[1])
		if info != -1:
			self.parent.destroy()
			MainWindow(self.connector,
					   info[0],
					   info[1])
		else:
			messagebox.showerror("Ошибка", "Такого пользователя не существует")

	def initUI(self):
		self.parent.title("Авторизация")
		self.parent.geometry("{}x{}+{}+{}".format(self.width,
												  self.height,
												  int(screen_res[0]/2 - self.height/2),
												  int(screen_res[1]/2 - self.width/2)))

		login_label = Label(self.mainFrame,text="Логин", font=self.text_font)
		login_entry = Entry(self.mainFrame)
		password_label = Label(self.mainFrame,text="Пароль", font=self.text_font)
		password_entry = Entry(self.mainFrame)
		confirm_button = Button(self.additionalFrame,
								text="Войти в систему",
								background="lightgrey",
								foreground="black",
								font=self.buttons_font)
		register_button = Button(self.additionalFrame,
								 text="Регистрация",
								 background="lightgrey",
								 foreground="black",
								 font=self.buttons_font)

		self.mainFrame.rowconfigure(0, pad=10)
		self.mainFrame.rowconfigure(1, pad=10)
		self.mainFrame.columnconfigure(0, pad=15)
		self.mainFrame.columnconfigure(1, pad=15)

		login_label.grid(row=0, column=0)
		login_entry.grid(row=0, column=1)
		password_label.grid(row=1, column=0)
		password_entry.grid(row=1, column=1)
		register_button.pack(pady=5, side=BOTTOM)
		confirm_button.pack(pady=5, side=BOTTOM)

		confirm_button.bind("<Button-1>",
							lambda data:self.data_handler((login_entry.get(), password_entry.get())))
		register_button.bind("<Button-1>",
							lambda data:RegWindow(self.parent, self.connector))
		self.mainFrame.pack(expand=True)
		self.additionalFrame.pack(side = BOTTOM)

class RegWindow:
	def __init__(self, parent, connector):
		self.parent = Toplevel()
		self.connector = connector
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13)
		self.width = parent.winfo_width() + 100
		self.height = parent.winfo_height() + 200
		self.Frames = []
		self.Entries = []
		self.Labels = []
		self.initUI()

	def handler(self, label):
		for elem in self.Entries:
			if elem.get() == "":
				messagebox.showerror("Ошибка регистрации", "Что-то пошло не так")
				return

		ok = server.add_user(connector=self.connector,
						login=self.Entries[5].get(),
						password=self.Entries[6].get(),
						FIO="{} {} {}".format(self.Entries[0].get(), self.Entries[1].get(), self.Entries[2].get()),
						passport=self.Entries[4].get(),
						user_type=self.Entries[7].get(),
						telephone=self.Entries[3].get())
		if ok == -1:
			messagebox.showerror("Ошибка регистрации", "Что-то пошло не так")
		else:
			messagebox.showinfo("Оповещение", "Вы успешно зарегестрированы")
			self.parent.destroy()

	def initUI(self):
		self.parent.geometry("{}x{}".format(self.width, self.height))
		self.parent.title("Регистрация")
		Lbls_names = ("Имя", "Фамилия", "Отчество", "Телефон", "Номер паспорта", "Логин", "Пароль", "Тип пользователя")

		self.Frames.append(Frame(self.parent))
		self.Frames[-1].columnconfigure(0, pad=15)
		self.Frames[-1].columnconfigure(1, pad=15)

		self.Frames[-1].rowconfigure(0, pad=10)
		self.Frames[-1].rowconfigure(1, pad=10)
		self.Frames[-1].rowconfigure(2, pad=10)
		self.Frames[-1].rowconfigure(3, pad=10)
		self.Frames[-1].rowconfigure(4, pad=10)
		self.Frames[-1].rowconfigure(5, pad=10)
		self.Frames[-1].rowconfigure(6, pad=10)
		self.Frames[-1].rowconfigure(7, pad=10)

		for n in range(8):
			self.Labels.append(Label(self.Frames[-1], text=Lbls_names[n], font=self.text_font))
			self.Labels[-1].grid(row=n, column=0, sticky=E)
			self.Entries.append(Entry(self.Frames[-1]))
			self.Entries[-1].grid(row=n, column=1)

		self.Frames[-1].pack(expand=True)

		self.Frames.append(Frame(self.parent))
		self.Labels.append(Label(self.Frames[-1], text="", font=self.text_font))
		self.Labels[-1].pack(fill=X)

		confirm = Button(self.Frames[-1],
						 text="Зарегестрироваться",
						 background="lightgrey",
						 foreground="black",
						 font=self.buttons_font)

		confirm.bind("<Button-1>", lambda event:self.handler(self.Labels[-1]))
		confirm.pack(pady=10)

		self.Frames[-1].pack(fill=X, expand=True)

class MainWindow:
	def __init__(self, connector, user_id, user_type):
		self.parent = Tk()
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.connector = connector
		self.user_id = user_id
		self.user_type = user_type
		self.Frames = []
		self.Buttons = []
		self.Buttons_names = []
		self.Labels = []
		self.width = 600
		self.height = 500
		self.initUI()
		self.parent.mainloop()

	def initUI(self):
		self.parent.title("Главное окно")

		if self.user_type == "1":
			self.Create_client_interface()
		if self.user_type == "2":
			self.Create_worker1_interface()
		if self.user_type == "3":
			self.Create_worker2_interface()

	def scroll(self, canvas):
		canvas.configure(scrollregion=canvas.bbox("all"))

	def handler_2(self, event):
		self.parent.destroy()
		AuthWindow()

	def Create_client_interface(self):
		self.Buttons_names = ["Личный кабинет", "Подробнее", "Выход"]
		client_devices = server.return_client_devices(self.connector, self.user_id)

		self.Frames.append(Frame(self.parent))
		Label(self.Frames[-1],
			  text="Список ваших устройств:",
			  font=self.text_font).pack(padx=30, pady=20)
		self.Frames[-1].pack(fill=X, side=TOP)

		self.Frames.append(Frame(self.parent))
		canvas = Canvas(self.Frames[-1])
		scrollbar = Scrollbar(self.Frames[-1], orient="vertical", command=canvas.yview)
		scrollbar.pack(side=LEFT, fill=Y)
		canvas.pack()
		self.Frames[-1].pack(expand=True)

		self.Frames.append(Frame(canvas, background="lightgrey"))
		canvas.create_window((0, 0), window=self.Frames[-1])
		self.Frames[-1].bind("<Configure>",
							 lambda event: self.scroll(canvas))
		for i in range(7):
			self.Frames[-1].columnconfigure(i, pad=20)
		for j in range(len(client_devices)):
			self.Frames[-1].rowconfigure(j, pad=20)

		n,m = 0,0
		for device in client_devices:
			m = 0
			Label(self.Frames[-1],
				  text="{}.".format(n+1),
				  font=self.text_font,
				  background="lightgrey").grid(row=n, column=m, sticky=N+S)
			m+=1
			for i in [2,6,3,5,7]:
				tmp = device[i]
				if len(tmp) > 20:
						tmp = device[i][0:int(len(tmp)/2)] + "\n-" + device[i][int(len(tmp)/2):]
				if i == 7:
					tmp = statuses_dict[device[i]]

				Label(self.Frames[-1],
					  text=tmp,
					  font=self.text_font,
					  background="lightgrey").grid(row=n, column=m, sticky=N+S)
				m+=1
			self.Buttons.append(Button(self.Frames[-1],
									   text=self.Buttons_names[1],
									   background="lightgrey",
									   foreground="black",
									   font=self.buttons_font))
			self.Buttons[-1].grid(row=n, column=m)
			self.Buttons[-1].bind("<Button-1>",
								lambda event, id_=device[0]: ClientDeviceWindow(self.connector, self.user_id, id_))
			n += 1

		self.parent.update()
		if self.Frames[-1].winfo_width() > 50:
			self.width = self.Frames[-1].winfo_width()+40

		canvas.configure(yscrollcommand=scrollbar.set,
						 width=self.width,
						 height=350)
		self.parent.geometry("{}x{}+{}+{}".format(self.width,
											self.height,
											int(screen_res[0]/2 - self.height/2),
											int(screen_res[1]/2 - self.width/2)))

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1],
								   text=self.Buttons_names[0],
								   background="lightgrey",
								   foreground="black", font=self.buttons_font))
		self.Buttons[-1].pack(side=LEFT, padx=10, pady=20)
		self.Buttons[-1].bind("<Button-1>", lambda event: ClientPersonalCabWindow(self.connector,
																				  self.parent,
																				  self.user_id))

		self.Buttons.append(Button(self.Frames[-1],
								   text=self.Buttons_names[2],
								   background="lightgrey",
								   foreground="black", font=self.buttons_font))
		self.Buttons[-1].pack(side=RIGHT, padx=10, pady=20)
		self.Buttons[-1].bind("<Button-1>", self.handler_2)

		self.Frames[-1].pack(side=BOTTOM)

	def Create_worker1_interface(self):
		tmp = server.return_employees_list(self.connector)
		self.Buttons_names = ["Добавить устройство",
							  "Список всех заказов",
							  "Устройства,\n готовые к ремонту",
							  "Устройства, готовые\n к передаче клиенту"]
		worker_info = []
		for worker in tmp:
			if worker[1] == self.user_id:
				worker_info = worker
				break

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		self.Labels.append(Label(self.Frames[-1],
								 text=worker_info[0],
								 font=self.text_font,
								 background="lightgrey"))
		self.Labels[-1].pack(side=TOP, padx=10)
		self.Labels.append(Label(self.Frames[-1],
								 text="приемный отдел",
								 font=font.Font(family="Halvetica", size=11, slant="italic"),
								 background="lightgrey"))
		self.Labels[-1].pack(side=TOP, padx=10)
		self.Frames[-1].pack(side=TOP, expand=True, pady=20, padx=20)

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		for i in range(len(self.Buttons_names)):
			self.Buttons.append(Button(self.Frames[-1],
									   text=self.Buttons_names[i],
									   font=self.buttons_font,
									   background="lightgrey"))
			self.Buttons[-1].pack(side=TOP, fill=X, pady=20, padx=20)

		self.Buttons[0].bind("<Button-1>", lambda event: AddOrderWindow(self.connector))
		self.Buttons[1].bind("<Button-1>", lambda event: OrdersListWindow(self.connector, self.user_id, 0))
		self.Buttons[2].bind("<Button-1>", lambda event: OrdersListWindow(self.connector, self.user_id, 1))
		self.Buttons[3].bind("<Button-1>", lambda event: OrdersListWindow(self.connector, self.user_id, 2))

		self.Frames[-1].pack(expand=True)

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1],
							text="Выход",
							font=self.buttons_font,
							background="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", self.handler_2)
		self.Buttons[-1].pack()
		self.Frames[-1].pack(side=BOTTOM, fill=X, pady=20)

	def Create_worker2_interface(self):
		tmp = server.return_employees_list(self.connector)
		self.Buttons_names = ["Устройства на\nдиагонстике",
							  "Устройства в ремонте"]
		worker_info = []
		for worker in tmp:
			if worker[1] == self.user_id:
				worker_info = worker
				break

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		self.Labels.append(Label(self.Frames[-1],
								 text=worker_info[0],
								 font=self.text_font,
								 background="lightgrey"))
		self.Labels[-1].pack(side=TOP, padx=10)
		self.Labels.append(Label(self.Frames[-1],
								 text="ремонтный отдел",
								 font=font.Font(family="Halvetica", size=11, slant="italic"),
								 background="lightgrey"))
		self.Labels[-1].pack(side=TOP, padx=10)
		self.Frames[-1].pack(side=TOP, expand=True, pady=20, padx=20)

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		for i in range(len(self.Buttons_names)):
			self.Buttons.append(Button(self.Frames[-1],
									   text=self.Buttons_names[i],
									   font=self.buttons_font,
									   background="lightgrey"))
			self.Buttons[-1].pack(side=TOP, fill=X, pady=20, padx=20)

		self.Buttons[0].bind("<Button-1>", lambda event: OrdersListWindow(self.connector, self.user_id, 3))
		self.Buttons[1].bind("<Button-1>", lambda event: OrdersListWindow(self.connector, self.user_id, 4))

		self.Frames[-1].pack(expand=True)

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1],
								   text="Выход",
								   font=self.buttons_font,
								   background="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", self.handler_2)
		self.Buttons[-1].pack()
		self.Frames[-1].pack(side=BOTTOM, fill=X, pady=20)

class AddOrderWindow:
	def __init__(self, connector):
		self.parent = Toplevel()
		self.connector = connector
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13)
		self.Buttons = []
		self.Labels = []
		self.Entries = []
		self.Frames = []
		self.initUI()
	def handler_1(self,):
		for i in range(len(self.Entries)):
			if self.Entries[i] == "" and i != 3 and i != 6:
				messagebox.showerror("Ошибка", "Возникла ошибка при добавлении заказа")

		ok = server.add_order(self.connector,
							  self.Entries[0].get(),
							  self.Entries[1].get(),
							  self.Entries[2].get(),
							  self.Entries[3].get(),
							  self.Entries[4].get(),
							  self.Entries[5].get(),
							  self.Entries[6].get())
		if ok != -1:
			messagebox.showinfo("Оповещение", "Заказ #{} добавлен".format(ok))
			self.parent.destroy()
		else:
			messagebox.showerror("Ошибка", "Возникла ошибка при добавлении заказа")

	def initUI(self):
		self.parent.title("Оформление заказа")
		lbls_names = ["ID клиента*",
					  "Тип устройства*",
					  "Модель устройства*",
					  "Пароль на устройстве",
					  "Краткое описание проблемы*",
					  "Производитель устройства*",
					  "Комментарий к заказу"]

		self.Frames.append(Frame(self.parent))
		for i in range(len(lbls_names)+2):
			self.Frames[-1].rowconfigure(i, pad=10)

		self.Frames[-1].columnconfigure(0, pad=10)
		self.Frames[-1].columnconfigure(1, pad=10)

		for i in range(len(lbls_names)):
			self.Labels.append(Label(self.Frames[-1], text=lbls_names[i], font=self.text_font))
			self.Labels[-1].grid(row=i, column=0, sticky=E)
			self.Entries.append(Entry(self.Frames[-1]))
			self.Entries[-1].grid(row=i, column=1, ipadx=40)
		self.Frames[-1].pack(expand=True)

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1],
								   text="Создать заказ",
								   font=self.buttons_font,
								   background="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", lambda event: self.handler_1())
		self.Buttons[-1].pack(pady=10)
		self.Frames[-1].pack(expand=True, side=BOTTOM)

		self.parent.update()
		self.parent.geometry("{}x{}".format(self.Frames[-2].winfo_width() + 20, self.parent.winfo_height()))

class OrdersListWindow:
	def __init__(self, connector, user_id, window_type=0):
		self.parent = Toplevel()
		self.statuses = {0:("", "Список всех заказов", "Подробнее о заказе", ClientDeviceWindow),
						 1:('priemnyi otdel', "Готово к передаче в ремонт", "Передать в ремонт", self.change_status),
						 2:('iz remonta v priemky', "Устройства, готовые к выдаче", "Передать клиенту", ClientInfoWindow),
						 3:('diagnostika', "Устройства на диагностике", "Завершить диагностику", DiagnosticsWindow),
						 4:('remont', "Устройства в ремонте", "О ремонте", RepairDetailsWindow)}
		self.employee = user_id
		self.window_type = window_type
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.connector = connector
		self.Orders = []
		self.Frames = []
		self.Buttons = []
		self.Labels = []
		self.clear_window()
		self.initUI()

	def scroll(self, canvas):
		canvas.configure(scrollregion=canvas.bbox("all"))

	def clear_window(self):
		slaves = self.parent.slaves()
		for slave in slaves:
			slave.destroy()
		self.Orders = []
		self.Frames = []
		self.Buttons = []
		self.Labels = []

	def redraw_window(self):
		self.clear_window()
		self.initUI()

	def resolve_client(self, device_id):
		c = self.connector.cursor()
		c.execute('select client_id from device where device_id={}'.format(device_id))
		tmp = c.fetchone()[0]
		c.close()
		return tmp

	def change_status(self, device_id, status):
		server.change_device_status(self.connector, device_id, status)
		messagebox.showinfo("Оповещение", "Устройство отправлено\nна диагностику")
		self.redraw_window()

	def initUI(self):
		self.Orders = server.return_orders(self.connector, self.statuses[self.window_type][0])
		if self.Orders == -1:
			self.Orders = ""

		self.Frames.append(Frame(self.parent))
		Label(self.Frames[-1],
			  text=self.statuses[self.window_type][1],
			  font=self.text_font).pack(padx=30, pady=20)
		self.Frames[-1].pack(fill=X, side=TOP)

		self.Frames.append(Frame(self.parent))
		canvas = Canvas(self.Frames[-1])
		scrollbar = Scrollbar(self.Frames[-1], orient="vertical", command=canvas.yview)
		scrollbar.pack(side=LEFT, fill=Y)
		canvas.pack()
		self.Frames[-1].pack()

		self.Frames.append(Frame(canvas, bg="lightgrey"))
		canvas.create_window((0, 0), window=self.Frames[-1])
		self.Frames[-1].bind("<Configure>",
							 lambda event: self.scroll(canvas))

		for i in range(5):
			self.Frames[-1].columnconfigure(i, pad=20)
		for j in range(len(self.Orders)):
			self.Frames[-1].rowconfigure(j, pad=20)

		m,n = 0,0
		for order in self.Orders:
			n = 0
			c = self.connector.cursor()
			c.execute('select * from device where device_id={}'.format(order[1]))
			device_info = c.fetchone()
			c.close()
			for j in range(4):
				if j == 1:
					self.Labels.append(Label(self.Frames[-1], text=device_info[2] + " " + device_info[6] + " " + device_info[3], font=self.text_font, background="lightgrey"))
					self.Labels[-1].grid(row=m, column=n)
				elif j == 3:
					self.Labels.append(Label(self.Frames[-1], text=statuses_dict[device_info[7]],
											 font=self.text_font, background="lightgrey"))
					self.Labels[-1].grid(row=m, column=n)
				else:
					self.Labels.append(Label(self.Frames[-1], text=order[j], font=self.text_font, background="lightgrey"))
					self.Labels[-1].grid(row=m, column=n, padx=20)
				n+=1
			self.Buttons.append(Button(self.Frames[-1], text=self.statuses[self.window_type][2], font=self.buttons_font, background="lightgrey"))
			self.Buttons[-1].grid(row=m, column=n+1)

			if self.window_type == 0:
				self.Buttons[-1].bind("<Button-1>", lambda event, device_id=order[1]: self.statuses[self.window_type][3](self.connector,
																														 0,
																														 device_id))
			elif self.window_type == 1:
				self.Buttons[-1].bind("<Button-1>", lambda event, device_id=order[1]: self.statuses[self.window_type][3](device_id,
																														 "diagnostika"))
			elif self.window_type == 2:
				self.Buttons[-1].bind("<Button-1>", lambda event, device_id=order[1], order_id=order[0]: self.statuses[self.window_type][3](self.connector,
																																			self,
																																			self.resolve_client(device_id),
																																			device_id,
																																			order_id))
			elif self.window_type == 3:
				self.Buttons[-1].bind("<Button-1>", lambda event, ord_id=order[0]: self.statuses[self.window_type][3](self.connector,
																													  self,
																													  ord_id))
			else:
				self.Buttons[-1].bind("<Button-1>", lambda event, device_id=order[1], ord_id=order[0]: self.statuses[self.window_type][3](self,
																																		  self.connector,
																																		  ord_id,
																																		  device_id,
																																		  self.resolve_client(device_id),
																																		  self.employee))
			m+=1

		self.parent.update()
		self.parent.geometry("{}x500".format(self.Frames[-1].winfo_width()+40))
		self.parent.update()
		canvas.configure(yscrollcommand=scrollbar.set, width=self.parent.winfo_width(), height=300)

		if self.Frames[-1].winfo_width() < 10:
			self.parent.geometry("700x500")
		self.Frames[-1].pack(side=TOP)

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1], text="Назад", font=self.buttons_font, background="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", lambda event: self.parent.destroy())
		self.Buttons[-1].pack(side=LEFT, pady=30, padx=20)

		self.Buttons.append(Button(self.Frames[-1], text="Обновить окно", font=self.buttons_font, background="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", lambda event: self.redraw_window())
		self.Buttons[-1].pack(side=RIGHT, pady=30, padx=20)
		self.Frames[-1].pack(side=BOTTOM)
		self.parent.update()

class ClientInfoWindow:
	def __init__(self, connector, parent, client_id, device_id, order_id):
		self.connector = connector
		self.device_id = device_id
		self.order_id = order_id
		self.parent = Toplevel()
		self.prev_window = parent
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.client_id = client_id
		self.ClientInfo = []
		self.Frames = []
		self.Labels = []
		self.Buttons = []
		self.initUI()

	def handler(self):
		if server.change_device_status(self.connector, self.device_id, "gotovo k vydache klienty"):
			messagebox.showinfo("Оповещение", "Статус заказа изменен на 'Готов к выдаче'")
		else:
			messagebox.showerror("Ошибка", "Возникла ошибка при смене статуса заказа")
			return

		server.set_order_ending_date(self.connector, self.order_id)
		self.prev_window.redraw_window()
		self.parent.destroy()

	def initUI(self):
		self.ClientInfo = server.return_client_info(self.connector, self.client_id)
		self.Frames = []
		self.Labels = []
		self.Buttons = []
		self.parent.title("Инфо клиента")
		Lbls_names = ("ФИО:", "Номер телефона:", "Номер пасспорта:", "ID:")

		self.Frames.append(Frame(self.parent, background="lightgrey"))

		self.Frames[-1].rowconfigure(0, pad=15)
		self.Frames[-1].rowconfigure(1, pad=15)
		self.Frames[-1].rowconfigure(2, pad=15)
		self.Frames[-1].rowconfigure(3, pad=15)

		self.Frames[-1].columnconfigure(0, pad=20)
		self.Frames[-1].columnconfigure(1, pad=20)

		counter=0
		for i in [4,3,2,0]:
			self.Labels.append(Label(self.Frames[-1], text=Lbls_names[counter], font=self.text_font, background="lightgrey"))
			self.Labels[-1].grid(row=counter, column=0, sticky=E)
			self.Labels.append(Label(self.Frames[-1], text=self.ClientInfo[i], font=self.text_font, background="lightgrey"))
			self.Labels[-1].grid(row=counter, column=1, sticky=E)
			counter+=1

		self.Frames[-1].pack(pady=20)

		self.Frames.append(Frame(self.parent))
		err_label = Label(self.Frames[-1])
		err_label.pack(side=BOTTOM)

		self.Buttons.append(Button(self.Frames[-1],
								   text="Завершить заказ",
								   background="lightgrey",
								   foreground="black",
								   font=self.buttons_font))
		self.Buttons[-1].bind("<Button-1>", lambda event: self.handler())
		self.Buttons[-1].pack(side=BOTTOM)

		self.Frames[-1].pack(side=BOTTOM, pady=20)

		self.parent.update()
		self.parent.geometry("{}x{}".format(self.Frames[-2].winfo_width()+40, self.Frames[-1].winfo_height()+self.Frames[-2].winfo_height()+80))

class DiagnosticsWindow:
	def __init__(self, connector, parent, order_id):
		self.connector = connector
		self.parent = Toplevel()
		self.prev_window = parent
		self.parent.title("Результаты диагностики")
		self.order_id = order_id
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.entry_text_font = font.Font(family="Halvetica", size=11)
		self.Frames = []
		self.Buttons = []
		self.Labels = []
		self.Entries = []
		self.InitUI()

	def pressed_button(self):
		c = self.connector.cursor()
		c.execute('select device_id from orders where order_id={}'.format(self.order_id))
		d_id = c.fetchone()[0]
		if len(self.Entries[-1].get(1.0, END)) < 20:
			messagebox.showwarning("Предупреждение", "Введите больше данных")
			return
		if server.change_order_comment(self.connector,self.order_id, self.Entries[-1].get(1.0, END)) != -1:
			if server.change_device_status(self.connector, d_id, "remont") != -1:
				messagebox.showinfo("Оповещение", "Заказ перемещен в 'Устройства в ремонте'")
				self.prev_window.redraw_window()
				self.parent.destroy()
		messagebox.showerror("Ошибка", "Проблема при загрузке\nданных диагностики")

	def InitUI(self):
		self.Frames.append(Frame(self.parent))
		self.Labels.append(Label(self.Frames[-1], text="Введите результаты диагностики", font=self.text_font))
		self.Labels[-1].pack(side=TOP, pady=10, fill=X)
		self.Frames[-1].pack(padx=20, pady=20)
		self.parent.update()

		self.Frames.append(Frame(self.parent))
		self.Entries.append(Text(self.Frames[-1], width=50, height=20, font=self.entry_text_font))
		self.Entries[-1].pack()
		self.Frames[-1].pack()
		self.parent.update()

		self.parent.geometry("{}x{}".format(self.Frames[-1].winfo_width()+40, self.Frames[-1].winfo_height() + self.Frames[-2].winfo_height() + 120))

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1], text="Завершить диагностику", font=self.buttons_font, bg="lightgrey"))
		self.Frames[-1].pack(side=BOTTOM)
		self.Buttons[-1].pack(pady=10)
		self.Buttons[-1].bind("<Button-1>", lambda event: self.pressed_button())

class RepairDetailsWindow:
	def __init__(self, parent, connector, order_id, device_id, client_id, employee_id):
		self.parent = Toplevel()
		self.prev_window = parent
		self.connector = connector
		self.order_id = order_id
		self.device_id = device_id
		self.client_id = client_id
		self.employee = employee_id
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.service_font = font.Font(family="Halvetica", size=15, weight="bold")
		self.Labels = []
		self.Frames = []
		self.Buttons = []
		self.current_order_price = 0
		self.initUI()

	def redraw_window(self):
		s = self.parent.slaves()
		for i in s:
			i.destroy()
		self.Labels = []
		self.Frames = []
		self.Buttons = []
		self.initUI()

	def change_status(self):
		ok = server.change_device_status(self.connector, self.device_id, "iz remonta v priemky")
		if ok == 1:
			messagebox.showinfo("Сообщение", "Ремонт по заказу №{} завершен.\n"
											 " Заказ передан в приемный отдел.".format(self.order_id))
			self.prev_window.redraw_window()
			self.parent.destroy()
		else:
			messagebox.showerror("Ошибка", "Возникла ошибка при смене статуса заказа.")

	def initUI(self):
		self.parent.title("О ремонте")
		self.current_order_price = 0
		self.DeviceInfo = server.return_detailed_device_info(self.connector, self.device_id)

		for service in self.DeviceInfo[1]:
			self.current_order_price += service[2]
		for component in self.DeviceInfo[2]:
			self.current_order_price += component[3]

		server.update_order_total_price(self.connector, self.order_id, self.current_order_price)

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		for i in range(len(self.DeviceInfo[0])):
			self.Frames[-1].columnconfigure(i, pad=30)
		self.Frames[-1].rowconfigure(0, pad=20)
		self.Frames[-1].rowconfigure(1, pad=20)

		top_lbls_names = ["Номер заказа", "ID клиента", "Дата начала заказа", "Дата завершения заказа", "Конечная стоимость"]
		top_info = (self.DeviceInfo[0][0], self.client_id, self.DeviceInfo[0][2], self.DeviceInfo[0][3], self.current_order_price)
		for i in range(5):
			self.Labels.append(Label(self.Frames[-1],
									 text=top_lbls_names[i],
									 font=self.text_font,
									 background="lightgrey"))
			self.Labels[-1].grid(row=0, column=i, sticky=W + E)
			self.Labels.append(Label(self.Frames[-1],
									 text=top_info[i],
									 font=self.text_font,
									 background="lightgrey"))
			self.Labels[-1].grid(row=1, column=i, sticky=W + E)
		self.Frames[-1].pack(fill=X, pady=10, padx=20)

		self.Frames.append(Frame(self.parent, bg="lightgrey", width=self.Frames[-1].winfo_width(), height=60))
		self.Labels.append(Label(self.Frames[-1], bg="lightgrey", text="Результаты диагностики", font=self.text_font))
		self.Labels[-1].pack(side=TOP, padx=20, pady=10)
		self.Labels.append(Text(self.Frames[-1], height=4, width=100))
		self.Labels[-1].insert(1.0, self.DeviceInfo[0][-1])
		self.Labels[-1].pack(side=TOP, fill=X, padx=20, pady=10)
		self.Frames[-1].pack(fill=X, padx=20, pady=10)

		servecies_lbls_names = ["Выполнил:", "Стоимость:", "Продолжительность:"]
		self.Frames.append(Frame(self.parent))
		self.Frames.append(Frame(self.Frames[2]))
		self.Frames.append(Frame(self.Frames[2]))
		if self.DeviceInfo[1] == []:
			self.Labels.append(Label(self.Frames[3], text="Нет ремонтных работ", font=self.text_font, bg="lightgrey"))
			self.Labels[-1].pack(padx=20, pady=10)
		for service in self.DeviceInfo[1]:
			self.Frames.append(Frame(self.Frames[3], bg="lightgrey"))
			self.Frames[-1].rowconfigure(0)
			self.Frames[-1].rowconfigure(1)
			self.Frames[-1].rowconfigure(2)
			self.Frames[-1].rowconfigure(3)

			self.Frames[-1].columnconfigure(0, pad=20)
			self.Frames[-1].columnconfigure(1, pad=20)

			self.Labels.append(Label(self.Frames[-1], text=service[0], font=self.service_font, bg="lightgrey", fg="red"))
			self.Labels[-1].grid(row=0, columnspan=2, sticky=W+E)
			print(service)
			for i in [1,2,3]:
				self.Labels.append(Label(self.Frames[-1], text=servecies_lbls_names[i-1], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i, column=0, sticky=E)
				self.Labels.append(Label(self.Frames[-1], text=service[i], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i, column=1, sticky=W)
			self.Frames[-1].pack(side=TOP, padx=10, pady=10, fill=X , expand=True)

		self.Buttons.append(
			Button(self.Frames[3], text="Добавить этап ремонта", font=self.buttons_font, bg="lightgrey"))
		self.Buttons[-1].bind("<Button-1>", lambda event: AddServiceWindow(self.connector, self, self.DeviceInfo[0][0],
																		   self.employee))
		self.Buttons[-1].pack(padx=20, pady=20, side=BOTTOM)

		self.Frames[3].pack(side=LEFT, pady=10, fill=X)
###-----------------------------------------------------------------------------------###

		servecies_lbls_names = ["Стоимость:", "Поставщик:", "Номер чека:"]
		if self.DeviceInfo[2] == []:
			self.Labels.append(Label(self.Frames[4], text="Нет использованных компонентов", font=self.text_font, bg="lightgrey"))
			self.Labels[-1].pack(padx=20, pady=10)
		for component in self.DeviceInfo[2]:
			self.Frames.append(Frame(self.Frames[4], bg="lightgrey"))
			self.Frames[-1].rowconfigure(0)
			self.Frames[-1].rowconfigure(1)
			self.Frames[-1].rowconfigure(2)
			self.Frames[-1].rowconfigure(3)

			self.Frames[-1].columnconfigure(0, pad=20)
			self.Frames[-1].columnconfigure(1, pad=20)

			self.Labels.append(
				Label(self.Frames[-1], text=component[2], font=self.service_font, bg="lightgrey", fg="red"))
			self.Labels[-1].grid(row=0, columnspan=2, sticky=W+E)
			print(component)
			for i in [0,1,2]:
				self.Labels.append(
					Label(self.Frames[-1], text=servecies_lbls_names[i], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i+1, column=0, sticky=E)
				self.Labels.append(Label(self.Frames[-1], text=component[i+3], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i+1, column=1, sticky=W)
			self.Frames[-1].pack(side=TOP, padx=10, pady=10, fill=X, expand=True)

		self.Buttons.append(
			Button(self.Frames[4], text="Добавить компонент", font=self.buttons_font, bg="lightgrey"))
		self.Buttons[-1].bind("<Button-1>",
							  lambda event: AddComponentWindow(self.connector, self, self.DeviceInfo[0][0]))
		self.Buttons[-1].pack(padx=20, pady=20, side=BOTTOM)

		self.Frames[4].pack(side=RIGHT, pady=10, fill=X)

		self.Frames[2].pack(side=TOP, expand=True)
###-----------------------------------------------------------------------------------###

		self.Frames.append(Frame(self.parent))

		self.Buttons.append(
			Button(self.Frames[-1], text="Завершить ремонт", font=self.buttons_font, bg="lightgrey"))
		self.Buttons[-1].bind("<Button-1>",
							  lambda event: self.change_status())
		self.Buttons[-1].pack(padx=20, pady=20, side=BOTTOM)
		self.Frames[-1].pack(side=BOTTOM, fill=X, pady=10, padx=20)

class AddServiceWindow:
	def __init__(self, connector, parent, order_id, employee_id):
		self.child = Toplevel()
		self.parent = parent
		self.connector = connector
		self.order_id = order_id
		self.employee = employee_id
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.initUI()

	def upload_service_info(self, service_name):
		ok = server.add_used_service(self.connector, self.order_id, service_name, self.employee, "-")
		if ok == -1:
			messagebox.showerror("Ошибка", "Возникла проблема при добавлении услуги")
			return
		self.parent.redraw_window()
		self.child.destroy()

	def initUI(self):
		self.child.title("Добавить услугу")
		fr = Frame(self.child)
		lbl = Label(fr, text="Выберите услугу из списка", font=self.text_font, bg="lightgrey")
		fr.pack(expand=True, fill=X)

		fr2 = Frame(self.child)
		ListBox = Listbox(fr2, width=40, height=5, font=self.text_font)
		scrollbar = Scrollbar(fr2, command=ListBox.yview)
		scrollbar.pack(fill=Y, side=RIGHT)
		ListBox.configure(yscrollcommand=scrollbar.set)

		services = server.return_service_names_list(self.connector)
		for service in services:
			ListBox.insert(END, service)

		fr2.pack(padx=20, pady=10)
		ListBox.pack(padx=20, pady=20)
		scrollbar.pack(fill=Y, side=RIGHT)

		fr3 = Frame(self.child)
		btn = Button(fr3, text="Добавить услугу", font=self.buttons_font, bg="lightgrey")
		btn.bind("<Button-1>", lambda event: self.upload_service_info(ListBox.get(ListBox.curselection()[0])))

		fr3.pack(side=BOTTOM, padx=20, pady=10)
		btn.pack(pady=10)

class AddComponentWindow:
	def __init__(self, connector, parent, order_id):
		self.child = Toplevel()
		self.parent = parent
		self.connector = connector
		self.order_id = order_id
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.Labels = []
		self.Buttons = []
		self.Frames = []
		self.Entries = []
		self.initUI()

	def upload_component_info(self):
		ok = server.add_used_component(self.connector,
									   self.order_id,
									   self.Entries[0].get(),
									   self.Entries[1].get(),
									   self.Entries[2].get(),
									   self.Entries[3].get())
		if ok == -1:
			messagebox.showerror("Ошибка", "Возникла проблема при добавлении компонента")

		self.parent.redraw_window()
		self.child.destroy()

	def initUI(self):
		self.child.title("Добавить компонент")
		fr = Frame(self.child)
		lbl = Label(fr, text="Введите данные о компоненте", font=self.text_font, bg="lightgrey")
		fr.pack(expand=True, fill=X)

		fr2 = Frame(self.child)
		fr2.rowconfigure(0, pad=20)
		fr2.rowconfigure(1, pad=20)
		fr2.rowconfigure(2, pad=20)
		fr2.rowconfigure(3, pad=20)

		fr2.columnconfigure(0, pad=20)
		fr2.columnconfigure(1, pad=20)

		lbls_names = ["Название*:", "Цена*:", "Поставщик*:", "Номер чека*:"]
		for i in range(4):
			self.Labels.append(Label(fr2, text=lbls_names[i], font=self.text_font))
			self.Labels[-1].grid(row=i, column=0, sticky=E)
			self.Entries.append(Entry(fr2))
			self.Entries[-1].grid(row=i, column=1, sticky=W+E)

		fr2.pack(expand=True, side=TOP, padx=20, pady=10)

		fr3 = Frame(self.child)
		btn = Button(fr3, text="Добавить компонент", font=self.buttons_font, bg="lightgrey")
		btn.bind("<Button-1>", lambda event: self.upload_component_info())

		fr3.pack(side=BOTTOM, pady=10, padx=20)
		btn.pack()

class ClientDeviceWindow:
	def __init__(self, connector, user_id, device_id):
		self.parent = Toplevel()
		self.connector = connector
		self.current_order_price = 0
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.service_font = font.Font(family="Halvetica", size=15, weight="bold")
		self.client_id = user_id
		self.device_id = device_id
		self.DeviceInfo = []
		self.Frames = []
		self.Buttons = []
		self.Labels = []
		self.initUI()

	def scroll(self, canvas):
		canvas.configure(scrollregion=canvas.bbox("all"))

	def initUI(self):
		self.parent.title("Информация об устройстве")
		self.DeviceInfo = server.return_detailed_device_info(self.connector, self.device_id)

		for service in self.DeviceInfo[1]:
			self.current_order_price += service[2]
		for component in self.DeviceInfo[2]:
			self.current_order_price += component[3]

		server.update_order_total_price(self.connector, self.DeviceInfo[0][0], self.current_order_price)

		self.Frames.append(Frame(self.parent, background="lightgrey"))
		print(self.DeviceInfo)
		for i in range(len(self.DeviceInfo[0])):
			self.Frames[-1].columnconfigure(i, pad=30)
		self.Frames[-1].rowconfigure(0, pad=20)
		self.Frames[-1].rowconfigure(1, pad=20)

		top_lbls_names = ["Номер заказа", "Дата начала заказа", "Дата завершения заказа", "Конечная стоимость"]
		top_info = (self.DeviceInfo[0][0], self.DeviceInfo[0][2], self.DeviceInfo[0][3], self.current_order_price)
		for i in range(4):
			self.Labels.append(Label(self.Frames[-1],
									 text=top_lbls_names[i],
									 font=self.text_font,
									 background="lightgrey"))
			self.Labels[-1].grid(row=0, column=i, sticky=W+E)
			self.Labels.append(Label(self.Frames[-1],
									 text=top_info[i],
									 font=self.text_font,
									 background="lightgrey"))
			self.Labels[-1].grid(row=1, column=i, sticky=W+E)
		self.Frames[-1].pack(fill=X, expand=True, pady=10, padx=20)

		servecies_lbls_names = ["Выполнил:", "Стоимость:", "Продолжительность:"]
		self.Frames.append(Frame(self.parent))
		self.Frames.append(Frame(self.Frames[1]))
		self.Frames.append(Frame(self.Frames[1]))
		if self.DeviceInfo[1] == []:
			self.Labels.append(Label(self.Frames[2], text="Нет ремонтных работ", font=self.text_font, bg="lightgrey"))
			self.Labels[-1].pack(padx=20, pady=10)
		for service in self.DeviceInfo[1]:
			self.Frames.append(Frame(self.Frames[2], bg="lightgrey"))
			self.Frames[-1].rowconfigure(0)
			self.Frames[-1].rowconfigure(1)
			self.Frames[-1].rowconfigure(2)
			self.Frames[-1].rowconfigure(3)

			self.Frames[-1].columnconfigure(0, pad=20)
			self.Frames[-1].columnconfigure(1, pad=20)

			self.Labels.append(
				Label(self.Frames[-1], text=service[0], font=self.service_font, bg="lightgrey", fg="red"))
			self.Labels[-1].grid(row=0, columnspan=2, sticky=W + E)
			print(service)
			for i in [1, 2, 3]:
				self.Labels.append(
					Label(self.Frames[-1], text=servecies_lbls_names[i - 1], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i, column=0, sticky=E)
				self.Labels.append(Label(self.Frames[-1], text=service[i], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i, column=1, sticky=W)
			self.Frames[-1].pack(side=TOP, pady=10, fill=X)

		self.Frames[2].pack(side=LEFT, padx=20, pady=10, fill=X)
		###-----------------------------------------------------------------------------------###

		servecies_lbls_names = ["Стоимость:", "Поставщик:", "Номер чека:"]
		if self.DeviceInfo[2] == []:
			self.Labels.append(
				Label(self.Frames[3], text="Нет использованных компонентов", font=self.text_font, bg="lightgrey"))
			self.Labels[-1].pack(padx=20, pady=10)
		for component in self.DeviceInfo[2]:
			self.Frames.append(Frame(self.Frames[3], bg="lightgrey"))
			self.Frames[-1].rowconfigure(0)
			self.Frames[-1].rowconfigure(1)
			self.Frames[-1].rowconfigure(2)
			self.Frames[-1].rowconfigure(3)

			self.Frames[-1].columnconfigure(0, pad=20)
			self.Frames[-1].columnconfigure(1, pad=20)

			self.Labels.append(
				Label(self.Frames[-1], text=component[2], font=self.service_font, bg="lightgrey", fg="red"))
			self.Labels[-1].grid(row=0, columnspan=2, sticky=E + W)
			for i in [0, 1, 2]:
				self.Labels.append(
					Label(self.Frames[-1], text=servecies_lbls_names[i], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i + 1, column=0, sticky=E)
				self.Labels.append(Label(self.Frames[-1], text=component[i + 3], font=self.text_font, bg="lightgrey"))
				self.Labels[-1].grid(row=i + 1, column=1, sticky=W)
			self.Frames[-1].pack(side=TOP, pady=10, fill=X)

		self.Frames[3].pack(side=RIGHT, padx=20, pady=10, fill=X)

		self.Frames[1].pack(side=TOP, expand=True, fill=X)
		###-----------------------------------------------------------------------------------###

		self.Frames.append(Frame(self.parent))

		self.Buttons.append(
			Button(self.Frames[-1], text="Назад", font=self.buttons_font, bg="lightgrey"))
		self.Buttons[-1].bind("<Button-1>",
							  lambda event: self.parent.destroy())
		self.Buttons[-1].pack(padx=20, pady=20, side=BOTTOM)
		self.Frames[-1].pack(side=BOTTOM, fill=X, pady=10, padx=20)

class ClientPersonalCabWindow:
	def __init__(self, connector, parent, client_id):
		self.connector = connector
		self.parent = Toplevel()
		self.buttons_font = font.Font(family="Halvetica", size=12)
		self.text_font = font.Font(family="Halvetica", size=13, weight="bold")
		self.client_id = client_id
		self.ClientInfo = []
		self.Frames = []
		self.Labels = []
		self.Buttons = []
		self.initUI()

	def initUI(self):
		self.ClientInfo = server.return_client_info(self.connector, self.client_id)
		self.Frames = []
		self.Labels = []
		self.Buttons = []
		self.parent.title("Личный кабинет")
		Lbls_names = ("ФИО:", "Номер телефона:", "Номер пасспорта:", "Ваш ID:")

		self.Frames.append(Frame(self.parent, background="lightgrey"))

		self.Frames[-1].rowconfigure(0, pad=15)
		self.Frames[-1].rowconfigure(1, pad=15)
		self.Frames[-1].rowconfigure(2, pad=15)
		self.Frames[-1].rowconfigure(3, pad=15)

		self.Frames[-1].columnconfigure(0, pad=20)
		self.Frames[-1].columnconfigure(1, pad=20)
		self.Frames[-1].columnconfigure(2, pad=20)

		counter = 0
		for i in [4,3,2,0]:
			self.Labels.append(Label(self.Frames[-1], text=Lbls_names[counter], font=self.text_font, background="lightgrey"))
			self.Labels[-1].grid(row=counter, column=0, sticky=E)
			self.Labels.append(Label(self.Frames[-1], text=self.ClientInfo[i], font=self.text_font, background="lightgrey"))
			if i == 3:
				self.Buttons.append(Button(self.Frames[-1],
										   text="Изменить номер",
										   background="lightgrey",
										   foreground="black",
										   font=self.buttons_font))
				self.Buttons[-1].grid(row=counter, column=2)
				self.Buttons[-1].bind("<Button-1>", lambda event: ChangeNumberWindow(self.connector,
																					 self,
																					 self.client_id))
			self.Labels[-1].grid(row=counter, column=1, sticky=E)
			counter += 1

		self.Frames[-1].pack(pady=20)

		self.Frames.append(Frame(self.parent))
		self.Buttons.append(Button(self.Frames[-1],
								   text="Назад",
								   background="lightgrey",
								   foreground="black",
								   font=self.buttons_font))
		self.Buttons[-1].bind("<Button-1>", lambda event: self.parent.destroy())
		self.Buttons[-1].pack(side=BOTTOM)

		self.Frames[-1].pack(side=BOTTOM, pady=20)

		self.parent.update()
		self.parent.geometry("{}x{}".format(self.Frames[-2].winfo_width()+40, self.Frames[-1].winfo_height()+self.Frames[-2].winfo_height()+80))

class ChangeNumberWindow:
	def __init__(self, connector, parent, client_id):
		self.connector = connector
		self.parent = parent
		self.window = Toplevel()
		self.buttons_font = font.Font(family="Halvetica", size=10)
		self.text_font = font.Font(family="Halvetica", size=13)
		self.width = 200
		self.height = 100
		self.client_id = client_id
		self.initUI()

	def handler(self, entry):
		ok = server.change_client_telephone(self.connector,
									   self.client_id,
									   entry)
		if ok != -1:
			messagebox.showinfo("Оповещение", "Номер успешно изменен!")
		else:
			messagebox.showerror("Ошибка", "Возникла ошибка при смене номера")
		self.window.destroy()

	def initUI(self):
		self.window.geometry("{}x{}".format(self.width, self.height))
		fm = Frame(self.window)
		Label(fm, text="Введите новый номер", font=self.text_font).pack(side=TOP, fill=X)
		entr = Entry(fm)
		entr.pack(side=TOP)

		btn = Button(fm,
					 text="Подтвердить",
					 background="lightgrey",
					 foreground="black",
					 font=self.buttons_font)
		btn.bind("<Button-1>", lambda event: self.handler(entr.get()))
		btn.pack(side=BOTTOM, pady=10)

		fm.pack(expand=True)

root = AuthWindow()

