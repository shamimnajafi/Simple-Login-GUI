# ---------------------------------------------فراخوانی کتابخانه های مورد نیاز-----------------------
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import sqlite3

# ---------------------------------------------صفحه اصلی (اول)--------------------------------------
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()                   #چون این کلاس از QDialog ارثبری میکند برای تعریف توابع دیگر باید از متد سوپر استفاده شود
        loadUi("welcomescreen.ui", self)
        self.loginbutton.clicked.connect(self.gotologin)        #ایونت کلیک کردن برای دکمه ها
        self.createaccbutton.clicked.connect(self.gotosignup)
        self.adminbutton.clicked.connect(self.gotoadminlogin)

    def gotologin(self):  # رفتن به صفحه ورود
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosignup(self):  # رفتن به صفحه ساخت حساب کاربری
        signup = SignUpScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoadminlogin(self):                               #رفتن به صفحه ورود ادمین
        adminlogin = AdminLogin()
        widget.addWidget(adminlogin)
        widget.setCurrentIndex(widget.currentIndex()+1)

# --------------------------------------------------------------------صفحه ورود-----------------------
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("loginscreen.ui", self)
        self.passfield.setEchoMode(QtWidgets.QLineEdit.Password)   #پنهان کردن کاراکترهای رمز عبور با نقطه های مشکی
        self.loginbutton.clicked.connect(self.loginfunction)

    def loginfunction(self):                                      #تابع برای دکمه ورود
        user = self.ufield.text()
        password = self.passfield.text()
        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please complete all fields / لطفا تمامی فیلد ها را کامل کنید")
        else:
            conn = sqlite3.connect("MyDatabase.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM login_info WHERE username=? AND password=?", (user,password,))
            result = cur.fetchone()                                 #گرفتن یک ردیف از دیتابیس

            if result == None:
                self.error.setText("Invalid username or password /  نام کاربری یا رمز عبور اشتباه است")
                print("Login failed / ورود ناموفق")
            else:
                print("successfully logged in / ورود با موفقیت انجام شد")
                self.error.setText("successfully logged in / ورود با موفقیت انجام شد")

# -------------------------------------------------------صفحه ساخت حساب کاربری-----------------------
class SignUpScreen(QDialog):
    def __init__(self):
        super(SignUpScreen, self).__init__()
        loadUi("signupscreen.ui", self)
        self.age.setMinimum(0)                             #مشخص کردن کف اسپین باکس
        self.age.setMaximum(110)                           #مشخص کردن سقف اسپین باکس
        self.passfield.setEchoMode(QtWidgets.QLineEdit.Password)  # مخفی کردن کاراکترهای رمز عبور
        self.confirmpassfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.signupfunction)

    def signupfunction(self):
        user = self.ufield.text()
        password = self.passfield.text()
        confirmpassword = self.confirmpassfield.text()
        name = self.name.text()
        lastname = self.lastname.text()
        age = self.age.value()
        gender = self.genderbox.currentText()
        nationality = self.nationbox.currentText()
        education = self.educationbox.currentText()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(name) == 0 or len(lastname)== 0 or age<1 or gender == "Choose / انتخاب کنید" or nationality == "Choose / انتخاب کنید" or education == "Choose / انتخاب کنید":
            self.error.setText("Please complete all fields / لطفا تمامی فیلدها را کامل کنید")
        else:
            conn = sqlite3.connect("MyDatabase.db")
            cur = conn.cursor()

            info = [user, password, name, lastname, age, gender, nationality, education]
            cur.execute("INSERT INTO login_info (username, password, name, lastname, age, gender, nationality, education) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", info)   #اضافه کردن مقادیر به دیتابیس
            conn.commit()
            conn.close()
            self.error.setText("Account successfully completed / حساب کاربری با موفقیت کامل شد")

# --------------------------------------------------------------صفحه ورود ادمین-----------------------
class AdminLogin(QDialog):
    def __init__(self):
        super(AdminLogin, self).__init__()
        loadUi("loginscreen1.ui", self)
        self.adminpassfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.adminloginbutton.clicked.connect(self.adminloginfunction)

    def adminloginfunction(self):
        adminuser = self.adminufield.text()
        adminpass = self.adminpassfield.text()
        if adminuser == "shamim_nji" and adminpass == "sh1379":   #مشخصات ادمین
            admininfotable = AdminInfoTable()
            widget.addWidget(admininfotable)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.error.setText("Invalid username or password /  نام کاربری یا رمز عبور اشتباه است")

# -------------------------------صفحه نمایش اطلاعات دیتابیس در جدول مخصوص ادمین-----------------------
class AdminInfoTable(QDialog):
    def __init__(self):
        super(AdminInfoTable, self).__init__()
        loadUi("admininfotable.ui", self)
        self.tableWidget.setColumnWidth(0, 150)     #مشخص کردن طول ستون ها
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 150)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(7, 150)
        self.loaddata()


    def loaddata(self):                               # انتقال اطلاعات دیتابیس به جدول مخصوص ادمین
        conn = sqlite3.connect("MyDatabase.db")
        cur = conn.cursor()
        self.tableWidget.setRowCount(10)               #مشخص کردن تعداد ردیف در جدول
        tablerow =0
        for row in cur.execute("SELECT * FROM login_info"):   #گرفتن همه اطلاعات از دیتابیس

                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
                self.tableWidget.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(row[7]))
                tablerow += 1



app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()      #برای نمایش تعداد صفحه بیشتر از 1
widget.addWidget(welcome)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)
widget.show()                             #بدون این کد صفحه نمایش داده نخواهد شد
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
