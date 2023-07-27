import json
import pymysql, requests, os, random, string, time

class XssClient:
    def __init__(self, domain, name, token, server_addr, db):
        #db접속 설정
        self.cursor = self.db.cursor()
        
        # 사용자 이름 및 접속 정보
        self.token = token
        self.flag_addr = f"http://{server_addr}/xss?token={token}"
        self.domain = domain
        self.name = name
    
    def get_flag(self):
        print(self.flag_addr)
        # 전체 FLAG 받아오기 & 저장하기
        self.xss_flag = requests.get(self.flag_addr).text

    def save_flag(self):
        sql = "insert into flag (domain, name, flag, created) values('%s', '%s', '%s', now())" % (
			self.domain,
            self.name,
            self.xss_flag
		)
        
        self.db.execute(sql)
        self.cursor.commit()

class Server:
    def __init__(self):
        self.db = pymysql.connect(
			host = 'localhost', user='TeamA', password='TeamA1234567@', db='kknock'
		)
        
        self.cursor = self.db.cursor()

    def read_user(self):
        self.user_class = {}
        
        with open("json/user.json", "r") as f:
            user_dict = json.load(f)
            
        for key, value in user_dict.items():
            self.user_class[key] = XssClient(name = key, domain=value[2], token=value[3], db=self.db, server_addr="server_addr")
    
    def delete_flag(self):    
        sql = "Truncate flag"
        self.db.execute(sql)
        self.curser.commit()

    def set_flag(self):
        for key, value in self.user_class.items():
            value.get_flag()
            value.save_flag()

if __name__ == "__main__":
    server = Server()
    
    time.sleep(30)
    # server.delete_flag()
    server.read_user()
    server.set_flag()