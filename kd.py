import re
import requests
import configparser
import random
import string
import pyperclip


session = requests.Session()


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://bm.cumt.edu.cn/index.jsp',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


config = configparser.ConfigParser()
config.read('config.ini')


name = config.get('Account', 'name')
sel = config.get('Account', 'sel')
password = config.get('Account', 'password')


payload = {
    'name': name,
    'sel': sel,
    'password': password
}


response = session.post('http://bm.cumt.edu.cn/LoginServlet', headers=headers, data=payload)


def generate_random_alias(length):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# 复制到剪切板
def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("已复制到剪切板")


# 菜单循环
while True:
    print("1. 随机生成别名")
    print("2. 输入自定义别名")
    print("3. 退出脚本")

    choice = input("请输入选项（1-3）：")

    if choice == '1':
        random_name = generate_random_alias(random.randint(5, 8))

        response = session.get(f'http://bm.cumt.edu.cn/SlaveUpdateServlet?vpn-12-o1-yxbm.aufe.edu.cn&slave={random_name}&i=1')

        if "添加成功" in response.text:
            match = re.search(r'slave=([^&]+)', response.url)
            if match:
                slave_value = match.group(1)
                alias_email = slave_value + "@cumt.edu.cn"
                print("新增别名邮箱:", alias_email)
                copy_to_clipboard(alias_email)
        else:
            print("添加失败或未找到相关信息")
    elif choice == '2':
        custom_alias = input("请输入自定义别名：")

        response = session.get(f'http://bm.cumt.edu.cn/SlaveUpdateServlet?vpn-12-o1-yxbm.aufe.edu.cn&slave={custom_alias}&i=1')

        if "添加成功" in response.text:
            alias_email = custom_alias + "@cumt.edu.cn"
            print("新增别名邮箱:", alias_email)
            copy_to_clipboard(alias_email)
        else:
            print("添加失败或未找到相关信息")
    elif choice == '3':
        break
    else:
        print("无效的选项。请重试。")
