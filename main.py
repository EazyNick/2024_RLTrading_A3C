from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys

class Kiwoom:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect()")
        self.ocx.OnEventConnect[int].connect(self.on_event_connect)
        self.ocx.OnReceiveTrData[str, str, str, str, str, str, str, str, str].connect(self.on_receive_tr_data)

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.app.exec_()

    def on_event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.request_stock_price()
        else:
            print("로그인 실패")

    def request_stock_price(self):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005930")
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보", "opt10001", "0", "0101")

    def on_receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "주식기본정보":
            price = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "현재가")
            print(f"현재가: {price.strip()}")

if __name__ == "__main__":
    kiwoom = Kiwoom()
    kiwoom.login()
