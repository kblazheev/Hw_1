okved_archive = 'okved_2.json.zip'
okved_file = 'okved_2.json'
egrul_archive = 'egrul.json.zip'
db = 'hw.db'
tab_okved = '''
    CREATE TABLE IF NOT EXISTS okved(
        id integer primary key,
        code text,
        parent_code text,
        section text,
        name text,
        comment text
    );'''
insert_okved = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
tab_telecom = '''
    CREATE TABLE IF NOT EXISTS telecom_companies(
        id integer primary key,
        name text,
        inn text,
        ogrn text,
        ogrn_date date,
        okved text
    );'''
insert_telecom = "INSERT INTO telecom_companies(name, inn, ogrn, ogrn_date, okved) VALUES(?, ?, ?, ?, ?);"
tab_vacancies = '''
            CREATE TABLE IF NOT EXISTS vacancies(
                id integer primary key,
                employer_name text,
                name text,
                description text,
                key_skills text
            );'''
insert_vacancy = "INSERT INTO vacancies(employer_name, name, description, key_skills) VALUES(?, ?, ?, ?);"
tab_vacancies1 = '''
            CREATE TABLE IF NOT EXISTS vacancies1(
                id integer primary key,
                employer_name text,
                name text,
                description text,
                key_skills text
            );'''
insert_vacancy1 = "INSERT INTO vacancies1(employer_name, name, description, key_skills) VALUES(?, ?, ?, ?);"
url = "https://api.hh.ru/vacancies?text=middle+python+developer&area=113&per_page=100&search_field=name"
url2 = "https://hh.ru/search/vacancy?text=middle+python+developer&area=113&items_on_page=100&search_field=name"
user_agent = {'User-agent': 'Mozilla/5.0'}