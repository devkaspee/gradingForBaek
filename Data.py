class DB:
    def __init__(self):
        self.f = open("/home/ghwns407/ServerForBeak/DB.txt", 'r')
        self.DB = {}
        lines = self.f.readlines()
        for i in range(len(lines)):
            temp = lines[i].split()
            self.DB[temp[0]] = (temp[1], temp[2])
        print(self.DB)

    def read(self, username):
        try:
            return self.DB[username]
        except:
            return

    def un_submit(self, username):
        money = (int(self.DB[username][0]) + 500 * (2 ** int(self.DB[username][1])))
        self.write(username, money, int(self.DB[username][1]) + 1)

    def submit(self, username):
        self.write(username, int(self.DB[username][0]), 0)

    def write(self, username, don, ill=0):
        self.DB[username] = (don, ill)

    def closes(self):
        self.f.close()
        self.f = open('/home/ghwns407/ServerForBeak/DB.txt', 'w')
        for i in self.DB:
            self.f.write(i + ' ' + str(self.DB[i][0]) + ' ' + str(self.DB[i][1]) + '\n')
        self.f.close()
