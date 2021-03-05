INSERT INTO {table} ({cell})
    SELECT * FROM (SELECT '{value}') AS tmp
    WHERE NOT EXISTS (
        SELECT {cell} FROM {table} WHERE {cell} = '{value}'
    )
    LIMIT 1;

INSERT INTO People (PersonName, Companies_companyID)
    SELECT * FROM (SELECT "{person}", (
        SELECT CompanyID FROM Companies WHERE CompanyName = "{company}"
    )) AS tmp
    WHERE NOT EXISTS (
        SELECT PersonName FROM People WHERE PersonName = "{person}"
    )
    LIMIT 1;

INSERT INTO {destination} ({table1}_{cell1}, {table2}_{cell2})
    SELECT * FROM (SELECT (
        SELECT {cell1} FROM {table1} WHERE {name1} = "{value1}"
    ), (
        SELECT {cell2} FROM {table2} WHERE {name2} = "{value2}"
    )) AS tmp
    LIMIT 1;

INSERT INTO GameCompany SET
    Games_GameID = (SELECT GameID FROM Games WHERE Name = "{game}"),
    Companies_CompanyID = (SELECT CompanyID FROM Companies WHERE CompanyName = "{comp}"),
    CompanyRole_CompanyRoleID = (SELECT CompanyRoleID FROM CompanyRoles WHERE CompanyRoleName = "{role}");

INSERT INTO companies SET 
    CompanyName = "{name}",
    Founded = "{company['Founded']}",
    HeadQuarters = "{company['Headquarters'] if not None else ''}",
    NumberOfEmployees = "{company['Number of employees'] if not None else 0}",
    ParentCompany = "{(company['Parent']) if not None else ''}",
    Website = "{company['Website'] if not None else ''}",
    CompanyType_CompanyTypeID = (SELECT CompanyTypeID FROM CompanyType WHERE CompanyTypeName = "{company['Type'] if not None else ''}"),
    AreaServed_AreaServedID = (SELECT AreaServedID FROM AreaServed WHERE AreaServed = "{company['Area served'] if not None else ''}");

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