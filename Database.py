import mysql.connector
from mysql.connector import errorcode

class Database:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password='passord123'
    )

    cursor = db.cursor()

    def __init__(self):
        self.selectDataBase('mydb')

    def selectDataBase(self, database):
        try:
            self.cursor.execute(f'USE {database}')
        except Exception as e:
            print(e)
        else:
            self.db.commit()

    def commit(self):
        self.db.commit()

    def deleteDataBase(self):
        tabels = [
            'Category',
            'Platform',
            'Industry',
            'Companies',
            'AreaServed',
            'CompanyType',
            'GameType',
            'CompanyRoles',
            'ControllerSupportType'
        ]

        for tabel in tabels:
            self.cursor.execute(f'ALTER TABLE {tabel} AUTO_INCREMENT = 0;')

        self.cursor.execute('DROP DATABASE mydb;')

        self.commit()
        print('Database deleted')

    # Database thing
    def simpleInsert(self, tableName, value):
        if value == None:
            return

        insertionTypes = {
            'CompanyType': ['CompanyType', 'CompanyTypeName'],
            'Area served': ['AreaServed', 'AreaServed'],
            'Industry': ['Industry', 'IndustryName'],
            'ControllerSupportType': ['ControllerSupportType', 'SupportType'],
            'GameType': ['GameType', 'GameTypeName'],
            'Category': ['Category', 'CategoryName'],
            'Platform': ['Platform', 'PlatformName'],
            'CompanyRoles': ['CompanyRoles', 'CompanyRoleName']
        }

        table = insertionTypes[tableName][0]
        cell = insertionTypes[tableName][1]

        try:
            self.cursor.execute(f"""
                INSERT INTO {table} ({cell})
                    SELECT * FROM (SELECT '{value}') AS tmp
                    WHERE NOT EXISTS (
                        SELECT {cell} FROM {table} WHERE {cell} = '{value}'
                    )
                    LIMIT 1;
            """)
        except Exception as e:
            print('Simple Insert:', e)
            exit()
        else:
            self.commit()

    def peopleConnectionInsert(self, person, company):
        try:
            self.cursor.execute(f""" 
                INSERT INTO People (PersonName, Companies_companyID)
                    SELECT * FROM (SELECT "{person}", (
                        SELECT CompanyID FROM Companies WHERE CompanyName = "{company}"
                    )) AS tmp
                    WHERE NOT EXISTS (
                        SELECT PersonName FROM People WHERE PersonName = "{person}"
                    )
                    LIMIT 1;
            """)
        except mysql.connector.Error as e:
            print('Person Connector:', e)
            exit()
        else:
            self.commit()

    def connectionInsert(self, destination, table1Name, value1, table2Name, value2):
        if value1 or value2 == None:
            return

        insertionTypes = {
            'Games': ['gameID', 'Games', 'Name'],
            'Category': ['CategoryID', 'Category', 'CategoryName'],
            'Platform': ['PlatformID', 'Platform', 'PlatformName'],
            'Companies': ['CompanyID', 'Companies', 'CompanyName'],
            'Industry': ['IndustryID', 'Industry', 'IndustryName']
        }

        cell1 = insertionTypes[table1Name][0]
        table1 = insertionTypes[table1Name][1]
        name1 = insertionTypes[table1Name][2]

        cell2 = insertionTypes[table2Name][0]
        table2 = insertionTypes[table2Name][1]
        name2 = insertionTypes[table2Name][2]
        
        try:
            self.cursor.execute(f"""
                INSERT INTO {destination} ({table1+ "_" + cell1}, {table2 + "_" + cell2})
                    SELECT * FROM (SELECT (
                        SELECT {cell1} FROM {table1} WHERE {name1} = '{value1}"
                    ), (
                        SELECT {cell2} FROM {table2} WHERE {name2} = "{value2}"
                    )) AS tmp 
                    WHERE NOT EXISTS (
                        SELECT {cell1} FROM {table1} WHERE {name1} = "{value1}"
                    )
                    LIMIT 1;
            """)
        except mysql.connector.Error as e:
            print('Medium Insert:', e)
            exit()
        else:
            self.commit()

    def connectGameAndComp(self, game, comp, role):
        try:
            self.cursor.execute(f""" 
                INSERT INTO GameCompany (Games_GameID, Companies_CompanyID, CompanyRole_CompanyRoleID)
                    SELECT * FROM (SELECT (
                        SELECT GameID FROM Games WHERE Name = "{game}"
                    ),(
                        SELECT CompanyID FROM Companies WHERE CompanyName = "{comp}"
                    ),(
                        SELECT CompanyRoleID FROM CompanyRoles WHERE CompanyRoleName = "{role}"
                    )) AS tmp 
                    WHERE NOT EXISTS (
                        SELECT GameID FROM Games WHERE Name = "{game}"
                    )
                    LIMIT 1;
            """)
        except mysql.connector.Error as e:
            print('Connect game and comp', e)
            exit()
        else:
            self.commit()
        
    def addCompany(self, name, company):
        try:
            self.cursor.execute(f"""
                INSERT INTO companies SET 
                    CompanyName = "{name}",
                    Founded = "{company['Founded']}",
                    HeadQuarters = "{company['Headquarters'] if not None else ''}",
                    NumberOfEmployees = "{company['Number of employees'] if not None else 0}",
                    ParentCompany = "{(company['Parent']) if not None else ''}",
                    Website = "{company['Website'] if not None else ''}",
                    CompanyType_CompanyTypeID = (SELECT CompanyTypeID FROM CompanyType WHERE CompanyTypeName = "{company['Type'] if not None else ''}"),
                    AreaServed_AreaServedID = (SELECT AreaServedID FROM AreaServed WHERE AreaServed = "{company['Area served'] if not None else ''}");
            """)
        except mysql.connector.Error as e:
            if e.errno != 1062 or 23000:
                print('Add company:', e)
        else:
            self.commit()

    def addGame(self, id, game):
        try:
            self.cursor.execute(f""" 
                INSERT INTO games SET
                    GameID = "{id}",
                    Name = "{game['name'] if not None else ''}",
                    Price = "{game['price']['price_NOK'] if not None else 0}",
                    Metacritic = "{game['metacritic'] if not None else ''}",
                    Recommendations = "{game['recommendations'] if not None else ''}",
                    NumDLC = "{game['numDLC'] if not None else ''}",
                    ReleaceDate = "{game['releaceDate'] if not None else ''}",
                    ControllerSupportType_ControllerSupportTypeID = (SELECT ControllerSupportTypeID FROM ControllerSupportType WHERE SupportType = "{game['controllerSupport'] if not None else ''}"),
                    GameType_GameTypeID = (SELECT GameTypeID FROM GameType WHERE GameTypeName = "{game['gameType'] if not None else ''}");
            """)
        except mysql.connector.Error as e:
            if e.errno != 1062 or 23000:
                print('Add game:', e)
        else:
            self.commit()

if __name__ == '__main__':
    db = Database()

    db.deleteDataBase()

    exit()

    db.simpleInsert('CompanyType', 'Public')
    db.simpleInsert('AreaServed', 'Worldwide')
    db.simpleInsert('Industry', 'Video Games')

    db.addCompany()

    db.peopleConnectionInsert('Mike Harrington', 'valve')
    db.connectionInsert('CompanyIndustry', 'Companies', 'Valve', 'Industry', 'Video games')



    exit()

    # Simple Company
    ## Company Type
    db.simpleInsert('CompanyType', 'Public')
    ## Area Served
    db.simpleInsert('AreaServed', 'Worldwide')    
    ## Industry
    db.simpleInsert('Industry', 'Video Games')

    # Connection Company
    ## People Inster
    db.peopleConnectionInsert('Mike Harrington', 'valve')
    ## Company Industry connector
    db.connectionInsert('CompanyIndustry', 'Companies', 'Valve', 'Industry', 'Video games')
    
    # Add Company


    # Simple Game
    ## Controller Support Type
    db.simpleInsert('ControllerSupportType', 'None')
    ## Game Type
    db.simpleInsert('GameType', 'Game')
    ## Category
    db.simpleInsert('Category', 'Multi-player')
    ## Platform
    db.simpleInsert('Platform', 'Windows')

    # Connection Game
    ## Category Connection
    db.connectionInsert('Categories', 'Games', 'Counter-Strike', 'Category', 'Multi-player')
    ## Platform Connection
    db.connectionInsert('Platforms', 'Games', 'Counter-Strike', 'Platform', 'Windows')
    
    # Add Game


    # Connect game to company
    db.connectGameAndComp('ID', 'Valve', 'role')
    
    