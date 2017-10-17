import psycopg2
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly
import webbrowser

DBNAME = "news"


def get_most_popular_articals():
    """Return most popular three articles of all time"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select a.title,count(*) as views 
    from articles as a ,log as l  
    where l.path like concat('%',a.slug) 
    group by a.title order by views desc limit 3''')
    entries = c.fetchall()
    db.close()
    
    return [('Title', 'Views')] + entries


def get_most_popular_authors():
    """Return most popular article authors of all time"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select authors.name, sum(author_views.views) 
    as views from (select a.author,count(*) as views 
    from articles as a ,log as l  
    where l.path like concat('%',a.slug) 
    group by a.author order by views desc) as author_views, authors 
    where authors.id = author_views.author 
    group by authors.name order by views desc''')
    entries = c.fetchall()
    db.close()
    return [('Author', 'Views')] + entries


def get_days_with_many_errors():
    """Return which days did more than 1% of requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select error_rates.date, error_rates.error_rate 
    from (select s.date,s.num as sucess_num , e.num as error_num, 
    (e.num*100.0)/(s.num+e.num) as error_rate 
    from (select time::date as date, count(*) as num 
    from log where status='200 OK' GROUP BY time::date) as s, 
    (select time::date as date, count(*) as num from log 
    where status != '200 OK' GROUP BY time::date) as e 
    where s.date = e.date order by error_rate desc) as error_rates 
    where error_rates.error_rate > 1.0;''')
    entries = c.fetchall()
    db.close()
    return [('Date', 'Error Rate(%)')] + entries

if __name__ == '__main__':
    plotly.tools.set_credentials_file(username='rmilinda', api_key='''HHPl
    wmzzyzb40nEIkU9M''')
    table1 = ff.create_table(get_most_popular_articals())
    url1 = py.plot(table1, filename='Most Popular Articals')
    print '''Please Click on the link if it did not 
    open you browser automatically ''' + url1
    webbrowser.open_new_tab(url1)
    
    table2 = ff.create_table(get_most_popular_authors())
    url2 = py.plot(table2, filename='Most Popular Authors')
    print '''Please Click on the link if it did not 
    open you browser automatically ''' + url2
    webbrowser.open_new_tab(url2)
    
    table3 = ff.create_table(get_days_with_many_errors())
    url3 = py.plot(table3, filename='''Days that have 
    more than 1% error rate''')
    print '''Please Click on the link if it did not 
    open you browser automatically ''' + url3
    webbrowser.open_new_tab(url3)
    


