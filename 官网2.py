import requests#请求
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import schedule
import time#定时系统
import xlwt#表格
headers={
    "User_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}#请求头
#请求定时模式
print(''' 
          模式1:按每？分钟执行一次爬取
          模式2：按每？小时执行一次爬取
          模式3：按每天的？点？分执行一次爬取
          模式4：每？小时运行，？点后停止
          ''')
way1_content=r'<p(.*)</p>'
#URL
url1="https://www.view.sdu.edu.cn/"
#post请求方法外包
def pachong(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }
    request = urllib.request.Request(url=url, headers=headers, method="POST")
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup
def job():
    sb = 0
    mb = 0
    nb = 0
    kb = 0
    #website 1 shandashidian
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建表格
    worksheet = workbook.add_sheet('山大要闻', cell_overwrite_ok=True)#创建表单
    content = requests.get(f"https://www.view.sdu.edu.cn/sdyw.htm", headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")  # beautiful soup分析
    all_titles = soup.find_all("a", attrs={
        "style": "    display: inline-block;    width: 551px;    overflow: hidden;    text-overflow: ellipsis;    white-space: nowrap;"})
    findtitle = re.compile(r'title="(.*)"')  # 正则表达式
    all_times = soup.find_all("span")
    findlink = re.compile(r'<a href="(.*?)" style')
    findtext = re.compile(r'<p>(.*)</p>')
    print("finished")
    #标题
    for title in all_titles:
        title=str(title.encode("ISO-8859-1").decode("utf-8"))
        date=[]
        title=re.findall(findtitle,title)[0]
        worksheet.write(sb,2,title)
        sb+=1
    #时间
    for time in all_times:
        if"2024" in str(time):
            worksheet.write(mb,0,str(time))
            mb+=1
    #链接
    for link in all_titles:
        link = str(link.encode("ISO-8859-1").decode("utf-8"))
        date = []
        link = re.findall(findlink, link)[0]
        if "info" not in str(link):
            jb=link
        else:
            jb=url1+str(link)
        worksheet.write(nb, 1, jb)
        nb += 1
    #内容
    for link in all_titles:
        link = str(link.encode("ISO-8859-1").decode("utf-8"))
        date = []
        link = re.findall(findlink, link)[0]
        if "info" not in str(link):
            jb=link
        else:
            jb=url1+str(link)
        soup=pachong(jb)
        text=soup.find_all("p")
        text=str(text)
        text=re.findall(findtext,text)
        worksheet.write(kb, 3,text)
        kb+=1
    #website 2 shandariji\
    sb = 0
    mb = 0
    nb = 0
    kb = 0
    worksheet1 = workbook.add_sheet('山大日记', cell_overwrite_ok=True)
    url2="https://www.sdrj.sdu.edu.cn/"
    findurl = r'<a href="(.*)" target="_blank" title='
    findtime=r'<span class="date">(.*)</span>'
    findtitle = r'title="(.*?)">'
    findtext=r'<p(.*)</p>'
    soup=pachong("https://www.sdrj.sdu.edu.cn/mrtt.htm")
    all_titles = soup.find_all("h4")
    #title
    for title in all_titles:
        title = str(title)
        date = []
        title = re.findall(findtitle, title)[0]
        worksheet1.write(sb, 2, title)
        sb += 1
    #time
    all_times =  soup.find_all("span")
    for time in all_times:
        time=re.findall(findtime,str(time))
        if"2024" in str(time):
            worksheet1.write(mb,0,time)
            mb+=1
    #link
    for link in all_titles:
        link = str(link.encode("ISO-8859-1").decode("utf-8"))
        date = []
        link = re.findall(findurl, link)[0]
        if "info" not in str(link):
            jb = link
        else:
            jb = url2 + str(link)
        worksheet1.write(nb, 1, jb)
        nb += 1
    #text
        soup = pachong(jb)
        text = soup.find_all("p")
        text = str(text)
        text = re.findall(findtext, text)
        worksheet1.write(kb, 3, text)
        kb += 1
    #保存表格
    workbook.save("sdu_news.xls")
#定时系统
moudule=input("请输入你需要模式几")
if moudule == "1":
    schedule.every(float(input("请输入分钟数"))).minutes.do(job)
if moudule == "2":
    schedule.every(float(input("请输入小时数"))).hour.do(job)
if moudule == "3":
    schedule.every().day.at("11:25").do(job)
if moudule == "4":
    schedule.every(float(input("请输入小时数"))).hours.until("input('请输入：小时：分钟，如13：15代表13点15分，需要输入冒号')").do(job)

while True:
     schedule.run_pending()
     time.sleep(1)