import psycopg2

class PgsqlConn:
    def __init__(self,config:dict) -> None:
        try:
            self.conn=psycopg2.connect(database=config['db'], user=config['user'], password=config['password'], host=config['host'], port= config['port'])
            # self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except:
            print('Error in connection')
            self.cursor.close()
            self.conn.close()
    
    def execute(self,sql:str)->bool:
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            data = obj.cursor.fetchone()
            print(data)
            return True
        except:
            return False

    def createDb(self,dbName:str) -> None:
        sql = "CREATE DATABASE "+dbName
        out="Database "+dbName+" created successfully :)" if(self.execute(sql)) else "Error creating database :("
        print(out)

    def createTable(self,table:dict) -> None:
        sql="CREATE TABLE "+table['tableName']+"("
        for _ in table:
            if(_=='attributes'):
                for i in table[_]:
                    sql+=i+' '+table[_][i]+','
        sql=sql[:-1]+");"
        # print(sql)
        out="Table "+table['tableName']+" created successfully :)" if(self.execute(sql)) else "Error creating table :("
        print(out)

    def insertTable(self,table:dict,values:list) -> None:
        sql="INSERT INTO "+table['tableName']+"("
        for _ in table:
            if(_=='attributes'):
                for i in table[_]:
                    sql+=i+','
        sql=sql[:-1]+") VALUES("
        for _ in values:
            for __ in _:
                sql+="'"+__+"'"+','
        sql=sql[:-1]+");"
        # print(sql)
        out="Inserted successfully :)" if(self.execute(sql)) else "Error inserting :("
        print(out)

    def __del__(self):
        self.cursor.close()
        self.conn.close()


myDb={
    'db':'keycloak',
    'user':'keycloak',
    'password':'password',
    'host':'127.0.0.1',
    'port':'5432'
}

myTable={
    'tableName':'test1',
    'attributes':{
        'uid':'VARCHAR',
        'count':'INT'
    }
}

myValues=[["abc123","1"]]

obj=PgsqlConn(myDb)
# obj.createDb("rj")
# obj.createTable(myTable)
obj.insertTable(myTable,myValues)

'''CREATING STRING FROM ATTRIBUTES
attr=""
for x in myTable:
    if(x=='attributes'):
        for i in myTable[x]:
            attr+=i+' '+myTable[x][i]+','
attr=attr[:-1]
print(temp)
'''

