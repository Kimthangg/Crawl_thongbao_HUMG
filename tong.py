import requests as rq
import os
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
import json
import time
def tele(text):
    # Thay thế bằng token của bot Telegram của bạn
    api_key = ''
    # Thay thế bằng Chat ID của người dùng hoặc nhóm bạn muốn gửi tin nhắn
    user_id = ''
    async def send_message():
        bot = Bot(token=api_key)
        
        await bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
        
    # Chạy hàm send_message() bất đồng bộ
    asyncio.run(send_message())
def ctsv():
    html_sub = rq.get('https://ctsv.humg.edu.vn/')
    if not html_sub.ok:
        print("Truy cập thất bại")
    #Đọc nội dung mới
    soup_sub = BeautifulSoup(html_sub.content, 'html.parser')
    # Lưu nội dung HTML vào tệp ctsv.html
    noidung = soup_sub.find('h2',class_='margin-bottom-sm').find('a')
    file_path = 'data_ctsv.txt'
    if os.path.exists(file_path):
        # Đọc lại nội dung tệp ctsv.html và phân tích cú pháp
        with open(file_path, 'r', encoding='utf-8') as file:
            soup_cu = file.read()
        # So sánh nội dung
        if str(noidung) != soup_cu: 
            link = html_sub + noidung['href']
            #Gọi tele để gửi tin nhắn
            tele(f'<b>CÔNG TÁC SINH VIÊN</b>\n\nTitle: {noidung.text}\n\nLink: {link}')
            print('Đã thay đổi')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(noidung))
        else:
            print('Giống')
    else:
        print('Tạo file thành công')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(noidung))
def cfi():
    html_sub = rq.get('https://cfi.humg.edu.vn/tin-tuc/Pages/chi-tiet.aspx?CateID=593',verify=False)
    base_url = 'https://cfi.humg.edu.vn/tin-tuc/Pages/chi-tiet.aspx'
    if not html_sub.ok:
        print("Truy cập thất bại")
    #Đọc nội dung mới
    soup_sub = BeautifulSoup(html_sub.content, 'html.parser')
    item = soup_sub.find_all('div',class_ = 'newsItem')
    if os.path.exists('data_cfi.html'):
        with open('data_cfi.html', 'r', encoding='utf-8') as file:
            soup_cu = file.read()
        if str(item) != soup_cu:
            item_0 = item[0].find('p',class_ = 'title')
            title = item_0.text
            link  = base_url + item_0.find('a')['href']
            #Gọi tele để gửi tin nhắn
            tele(f'<b>TT NGOẠI NGỮ TIN HỌC</b>\n\nTitle: {title}\n\nLink: {link}')
            print('Đã thay đổi')
            with open('data_cfi.html', 'w', encoding='utf-8') as file:
                file.writelines(str(item))
        else:
                print('Giống')
    else:
        print('Tạo file thành công')
        with open('data_cfi.html', 'w', encoding='utf-8') as file:
            file.writelines(str(item))
def daotao():
    url_api = 'https://daotaodaihoc.humg.edu.vn:443/api/web/w-locdsbaiviet'
    play_load = {
        "filter":{
            "ky_hieu":2,
            "is_hien_thi":True,
            "is_hinh_dai_dien":True,
            "so_luong_hinh_dai_dien":20,
            "is_khong_phan_cap":True,
            "is_quyen_xem":False
        },
        "additional":{
            "paging":{
                "limit":5,
                "page":1
            },
            "ordering":[
                {
                    "name":"do_uu_tien",
                    "order_type":1
                },
                {
                    "name":"ngay_dang_tin",
                    "order_type":1
                }
            ]
        }
    }
    id_sub = ''
    play_load_sub={
        "filter":{
            "id":id_sub,
            "is_noi_dung":True,
            "is_hinh_dai_dien":False,
            "is_quyen_xem":False,
            "so_luong_hinh_dai_dien":1,
            "is_khong_phan_cap":True
        },
        "additional":{
            "paging":{
                "limit":1,
                "page":1
            },
            "ordering":[
                {
                    "name":None,
                    "order_type":None
                }
            ]
        }
    }
    response = rq.post(url_api,json=play_load)
    if response.ok:
        print('ok')
    else:
        print('lỗi')
    data = response.json()
    if os.path.exists('data_daotao.json'):
        # Đọc dictionary từ tệp JSON
        with open('data_daotao.json', 'r') as file:
            data_old = json.load(file)
            if data != data_old:
                id_sub = data['data']['ds_bai_viet'][0]['id']
                response_sub = rq.post(url_api,json=play_load_sub)
                if response_sub.ok:
                    print('sub ok')
                    #lấy json từ id bài viết
                    data_sub = response_sub.json()
                    #lấy tiêu đề từ json
                    tieu_de = data_sub['data']['ds_bai_viet'][0]['tieu_de']
                    temp = data_sub['data']['ds_bai_viet'][0]['noi_dung']
                    #lấy nội dung
                    noidung = BeautifulSoup(temp,'lxml').get_text('\n')
                    #tạo link từ id
                    link = f'https://daotaodaihoc.humg.edu.vn/#/home/listbaiviet/tb/page/1/baivietct/{id_sub}'
                    #gửi thông báo đến tele
                    tele(f'<b>PHÒNG ĐÀO TẠO</b>\nTitle: {tieu_de}\n\nContent: {noidung}\n\nLink: {link}')
                    print('Đã gửi')
                    #lưu file mới
                    with open('data_daotao.json', 'w',encoding='utf-8') as file:
                        json.dump(data, file, indent=4)  # indent=4 để có định dạng dễ đọc
                else:
                    print('lỗi sub')
            else:
                print('Giống nhau')
    else:
        print('Tạo file thành công')
        with open('data_daotao.json', 'w',encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # indent=4 để có định dạng dễ đọc
print("Chạy CTSV:")
ctsv()
print('='*50)
print("Chạy CFI:")
time.sleep(5)
cfi()
print('='*50)
print("Chạy DAOTAO:")
time.sleep(5)
daotao()