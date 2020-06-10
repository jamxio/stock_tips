# -*- coding: utf-8 -*-
import json
# 导入需要的python模块httplib，用来模拟提交http请求，详细的用法可见python帮助手册
import http.client as httplib


def main(stock_codes):
    conn = httplib.HTTPConnection('qd.10jqka.com.cn')

    # 提交登录的post请求
    conn.request('GET', url="/quote.php?cate=real&return=json&type=stock&callback=&code=" + ','.join(stock_codes))

    # 获取服务器的返回
    res = conn.getresponse()

    urlContent = res.read()
    jsonStr = urlContent.strip('()'.encode())
    realPiao = json.loads(jsonStr.decode(), encoding='gbk')
    piaoInfo = realPiao.get('info')
    piaoData = realPiao.get('data')

    tip = ''
    for code in piaoData:
        try:
            name = piaoInfo[code]['name']
            now = float(piaoData[code]["10"])

            average = float(piaoData[code]['1378761'])
            diff = now / average
            rise = piaoData[code]['199112']
            print(diff, name, now, rise)
            if diff >= 1.02:
                tip += name + ' ' + ('%.2f' % (diff * 100 - 100)) + '%' + u' 卖出\r\n'
            elif diff <= 0.98:
                tip += u'{name} {diff:.2f}% 买入\r\n'.format(name=name, diff=diff * 100 - 100)
        except:
            pass;
    return tip


if __name__ == '__main__':
    stock_codes = [
        '000089', '300071', '601777', '300259', '600029', '600017', '1A0001', '399001',
        '000903', '601939', '600210', '600226', '000068', '002580', '000058', '601766'
    ]  #
    print(main(stock_codes))
