import csv
from datetime import datetime

def check_if_rukau(inputFileName):
    with open(inputFileName, newline='') as csvin:
        bf_rows = csv.DictReader(csvin)
        for bf_row in bf_rows:
            if bf_row['贊助明細'].find('全魯凱語山上教室') != -1:
                return True
            else:
                return False

def modify_header(inputFileName, outputFileName):
    with open(inputFileName, newline='') as inFile, open(outputFileName, 'w', newline='') as outfile:
        r = csv.reader(inFile)
        w = csv.writer(outfile)

        next(r, None)  # skip the first row from the reader, the old header
        # write new header
        w.writerow(['訂單類別','金流單號','贊助明細','總數量','商品總金額','額外贊助','其他金額款項','小計','運費',
        '折扣金額（折扣券）','折抵紅利點數','總金額','預計發送紅利點數','已退款金額','目前金額','幣別','商家註記','標籤',
        '導購來源','導購參數','選項','狀態','收件者姓名','收件者Email','收件者電話','所在國家','居住城市','居住區域',
        '郵遞區號','收件者地址','想說的話','寄送方式','超商系統','門市名稱','門市代號','門市地址','訂購人姓名','訂購人Email',
        '訂購人電話','會員ID','會員姓名','會員Email','付款方式','信用卡末四碼','訂單建立時間','付款時間','退款／狀態更新時間',
        '退款／狀態更新原因','退款／狀態更新操作者','退款／狀態更新操作者身份','實際單位數量','折扣券','出貨狀態','物流編號','分期',
        '重新扎根 NTD$ 221','重新扎根紙本收據抬頭','重新扎根捐款人姓名','重新扎根出生年份','重新扎根性別','重新扎根職業','重新扎根年齡','重新扎根備註',
        '寸草春暉 NTD$ 416','寸草春暉紙本收據抬頭','寸草春暉捐款人姓名','寸草春暉出生年份','寸草春暉職業','寸草春暉性別','寸草春暉年齡','寸草春暉備註',
        '春風化雨 NTD$ 641','春風化雨紙本收據抬頭','春風化雨捐款人姓名','春風化雨出生年份','春風化雨職業','春風化雨年齡','春風化雨性別','春風化雨備註',
        '薪火相傳 NTD$ 830','薪火相傳紙本收據抬頭','薪火相傳捐款人姓名','薪火相傳出生年份','薪火相傳職業','薪火相傳性別','薪火相傳年齡','薪火相傳備註',
        '眾志成城 NTD$1300','眾志成城紙本收據抬頭','眾志成城捐款人姓名','眾志成城出生年份','眾志成城職業','眾志成城性別','眾志成城年齡','眾志成城備註',
        '理念支持 NTD$ 221','理念支持紙本收據抬頭','理念支持捐款人姓名','理念支持出生年份','理念支持職業','理念支持性別','理念支持年齡','理念支持備註',
        '企業贊助 NTD50000','企業贊助紙本收據抬頭','企業贊助捐款人姓名','企業贊助出生年份','企業贊助職業','企業贊助性別','企業贊助年齡','企業贊助備註',
        '理念支持 NTD$ 100','理念支持100備註',
        '寸草春暉 NTD$ 400','寸草四百紙本收據抬頭','寸草四百捐款人姓名','寸草四百出生年份','寸草四百職業','寸草四百性別','寸草四百備註'])

        # copy the rest
        for row in r:
            w.writerow(row)

def convert_bf_to_neticrm(bf_filename, neticrm_filename):
    with open(bf_filename, newline='') as csvin:
        bf_rows = csv.DictReader(csvin)
        with open(neticrm_filename, 'w', newline='') as csvout:
            fieldnames = ['捐款金額','訂單類別','捐款日期','交易編號','付款方式','贊助方案','職業','性別','特殊需求',
            '導購來源','商家備註','捐款者留言','姓名','姓氏','名字','捐款徵信','出生年','加入管道','費用類型',
            '性別','族群','資料來源','訂購人姓名','訂購人Email','訂購人電話','wabay會員姓名','收件者姓名','收件者Email',
            '收件者電話','所在國家','居住城市','居住區域','郵遞區號','收件者地址','已建立','收據','收據抬頭']
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
                    new_row['贊助方案'] = bf_row['贊助明細'].replace('《全魯凱語山上教室》集資計畫｜讓扎根在石板屋裡的魯凱族，重新萌芽於山林之間 - ', '')
                    new_row['訂單類別'] = '02' + new_row['訂單類別']
                    new_row['資料來源'] = '02' + new_row['資料來源']
                #導購來源
                new_row['導購來源'] = bf_row['導購來源']
                #商家備註
                new_row['商家備註'] = bf_row['商家註記']
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

                #全母語河邊教室專用的相關欄位
                if bf_row['贊助明細'].find('全母語河邊教室') != -1:
                    #捐款者留言
                    notes_type = ('理念支持 - 備註','片片美意 - 備註','深入南島 - 備註','南島之友*12 - 備註','南島之友 - 備註','理念支持 - 備註',
                    '揮汗成雨 - 備註','感謝常存 - 備註','將美留下 - 備註','薪火相傳 - 備註','寸草春暉 - 備註',)
                    for note in notes_type:
                        if bf_row.get(note) == None:
                            new_row['捐款者留言'] = None
                        else:
                            if len(bf_row[note]) > 0:
                                new_row['捐款者留言'] = bf_row[note]
                                break
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

                #全魯凱語山上教室專用的相關欄位
                if bf_row['贊助明細'].find('全魯凱語山上教室') != -1:
                    if bf_row['重新扎根 NTD$ 221'] == '1':
                        donate_type = '重新扎根'
                    elif bf_row['寸草春暉 NTD$ 416'] == '1':
                        donate_type = '寸草春暉'
                    elif bf_row['春風化雨 NTD$ 641'] == '1':
                        donate_type = '春風化雨'
                    elif bf_row['薪火相傳 NTD$ 830'] == '1':
                        donate_type = '薪火相傳'
                    elif bf_row['眾志成城 NTD$1300'] == '1':
                        donate_type = '眾志成城'
                    elif bf_row['理念支持 NTD$ 221'] == '1':
                        donate_type = '理念支持'
                    elif bf_row['企業贊助 NTD50000'] == '1':
                        donate_type = '企業贊助'
                    elif bf_row['理念支持 NTD$ 100'] == '1':
                        donate_type = '理念支持100'             
                    elif bf_row['寸草春暉 NTD$ 400'] == '1':
                        donate_type = '寸草四百'    
                    #備註
                    new_row['捐款者留言'] = bf_row[donate_type + '備註']
                    #轉換選項欄位dict
                    bf_row['選項'] = bf_row['選項'].replace('\n', '')
                    option = bf_row['選項'].replace(' ', '')
                    if len(option) > 0:
                        option_dict = dict(x.split(":") for x in option.split(","))
                        #職業
                        new_row['職業'] = option_dict.get('職業（非必填）')
                        #性別
                        if option_dict.get('性別（非必填）') != None:
                            new_row['性別'] = option_dict.get('性別（非必填）').replace('性', '') 
                        #收據抬頭
                        new_row['收據抬頭'] = option_dict.get('紙本收據抬頭')
                        #捐款徵信
                        if option_dict.get('捐款人姓名') == '與紙本收據抬頭相同':
                            new_row['捐款徵信'] = new_row['姓名']
                        else:
                            new_row['捐款徵信'] = option_dict.get('捐款人姓名')
                        #出生年
                        birthYearDict = {'19歲以下':2007, '20～29歲':1997, '30～39歲':1987, '40～49歲':1977, '50～59歲':1967, '60歲以上':1957} 
                        new_row['出生年'] = birthYearDict.get(option_dict.get('年齡（非必填）'))
                writer.writerow(new_row)
