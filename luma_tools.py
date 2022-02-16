import csv
from datetime import datetime
def convert_bf_to_neticrm(bf_filename, neticrm_filename):
    with open(bf_filename, newline='') as csvin:
        bf_rows = csv.DictReader(csvin)
        with open(neticrm_filename, 'w', newline='') as csvout:
            fieldnames = ['捐款金額','訂單類別','捐款日期','交易編號','付款方式','贊助方案','特殊需求',
            '導購來源','商家備註','捐款者留言','姓名','姓氏','名字','捐款徵信','出生年','加入管道','費用類型',
            '性別','族群','資料來源','訂購人姓名','訂購人Email','訂購人電話','wabay會員姓名','收件者姓名','收件者Email',
            '收件者電話','所在國家','居住城市','居住區域','郵遞區號','收件者地址','已建立','收據']
            writer = csv.DictWriter(csvout, fieldnames = fieldnames)
            writer.writeheader()
            for bf_row in bf_rows:
                #捐款金額
                new_row = {'捐款金額':bf_row['總金額']} 
                #訂單類別 #資料來源
                if bf_row['訂單類別'].find('定期定額') != -1:
                    new_row['訂單類別'] = '貝殼放大-定期定額'
                    new_row['資料來源'] = '貝殼放大-定期定額'
                elif bf_row['訂單類別'].find('一般訂單') != -1:
                    new_row['訂單類別'] = '貝殼放大-一般訂單'
                    new_row['資料來源'] = '貝殼放大-一般訂單'
                #捐款日期
                donate_date = datetime.strptime(bf_row['付款時間'], '%Y-%m-%d %H:%M:%S %z')
                new_row['捐款日期'] = donate_date.strftime("%Y-%m-%d")
                #交易編號
                new_row['交易編號'] = bf_row['金流單號']
                #付款方式
                dict_pay_method = {"credit":"信用卡",'atm':'Web ATM','cvs':'超商條碼繳費','direct':'轉帳捐款'}
                new_row['付款方式'] = dict_pay_method[bf_row['付款方式']]
                #贊助方案
                if bf_row['贊助明細'].find('全母語河邊教室') != -1:
                    new_row['贊助方案'] = bf_row['贊助明細'].replace('全母語河邊教室｜集資計畫 - ', '')
                elif bf_row['贊助明細'].find('全魯凱語山上教室') != -1:
                    new_row['贊助方案'] = bf_row['贊助明細'].replace('全魯凱語山上教室 集資計畫 - ', '')
                    new_row['訂單類別'] = new_row['訂單類別'] + '_魯'
                    new_row['資料來源'] = new_row['資料來源'] + '_魯'
                #導購來源
                new_row['導購來源'] = bf_row['導購來源']
                #商家備註
                new_row['商家備註'] = bf_row['商家註記']
                #捐款者留言
                notes_type = ('理念支持 - 備註','片片美意 - 備註','深入南島 - 備註','南島之友*12 - 備註','南島之友 - 備註','理念支持 - 備註',
                '揮汗成雨 - 備註','感謝常存 - 備註','將美留下 - 備註','薪火相傳 - 備註')
                for note in notes_type:
                    if bf_row.get(note) == None:
                        new_row['捐款者留言'] = None
                    else:
                        if len(bf_row[note]) > 0:
                            new_row['捐款者留言'] = bf_row[note]
                            break
                #姓名
                new_row['姓名'] = bf_row['訂購人姓名']
                #姓氏 #名字
                if len(bf_row['訂購人姓名']) == 4:
                    bf_row['訂購人姓名'] = bf_row['訂購人姓名'].replace(' ', '')
                    new_row['姓氏'] = bf_row['訂購人姓名'][2]
                    new_row['名字'] = bf_row['訂購人姓名'][0:2]
                elif len(bf_row['訂購人姓名']) > 3:
                    new_row['姓氏'] = bf_row['訂購人姓名']
                else:
                    new_row['姓氏'] = bf_row['訂購人姓名'][0]
                    new_row['名字'] = bf_row['訂購人姓名'][1:len(bf_row['訂購人姓名'])]
                #捐款徵信 #出生年(只保留西元年，其他格式剔除)
                bf_row['選項'] = bf_row['選項'].replace('\r\n', '')
                options = bf_row['選項'].split(', ')
                options[0] = options[0].replace('捐款人姓名（非必填）: ', '')
                if len(options[0]) > 0:
                    new_row['捐款徵信'] = options[0]
                if len(options) == 2:
                    options[1] = options[1].replace('您的出生年份（非必填）: ', '') 
                    options[1] = options[1].replace('\n', '') 
                    try:
                        birthYear = int(options[1])
                    except:
                        birthYear = 0
                    if birthYear < 1800 or birthYear > 2100:
                        new_row['出生年'] = None
                    else:
                        new_row['出生年'] = birthYear
                #加入管道
                new_row['加入管道'] = '貝殼放大'
                #費用類型
                new_row['費用類型'] = '指定捐款'
                #訂購人姓名
                new_row['訂購人姓名'] = bf_row['訂購人姓名']
                #訂購人Email
                new_row['訂購人Email'] = bf_row['訂購人Email']
                #訂購人電話
                new_row['訂購人電話'] = bf_row['訂購人電話']
                #wabay會員姓名
                new_row['wabay會員姓名'] = bf_row['會員姓名']
                #收件者姓名
                new_row['收件者姓名'] = bf_row['收件者姓名']
                #收件者Email
                new_row['收件者Email'] = bf_row['收件者Email']
                #收件者電話
                bf_row['收件者電話'] = bf_row['收件者電話'].replace('+886', '0')
                bf_row['收件者電話'] = bf_row['收件者電話'].replace('+', '')
                bf_row['收件者電話'] = bf_row['收件者電話'].replace('-', '')
                bf_row['收件者電話'] = bf_row['收件者電話'].replace(' ', '')
                new_row['收件者電話'] = bf_row['收件者電話']
                #所在國家
                new_row['所在國家'] = bf_row['所在國家']
                #居住城市
                new_row['居住城市'] = bf_row['居住城市']
                new_row['居住城市'] = new_row['居住城市'].replace('台','臺')
                #居住區域
                new_row['居住區域'] = bf_row['居住區域']
                #郵遞區號
                new_row['郵遞區號'] = bf_row['郵遞區號']
                #收件者地址
                new_row['收件者地址'] = bf_row['收件者地址']
                writer.writerow(new_row)
