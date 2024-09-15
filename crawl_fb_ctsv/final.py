
from selenium import webdriver
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import asyncio
from telegram import Bot
#Thay thế api_key và user_id ở dòng 96 và 98
# Tạo đối tượng ChromeOptions
chrome_options = webdriver.ChromeOptions()

# Tắt popup cấp quyền thông báo
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})
# # Thêm tùy chọn chạy ở chế độ headless
# chrome_options.add_argument("--headless")

# # Nếu bạn muốn không hiển thị giao diện người dùng đồ họa, thêm tùy chọn này (chỉ cần trên một số hệ thống)
# chrome_options.add_argument("--disable-gpu")

# Khởi tạo trình duyệt
driver = webdriver.Chrome(options=chrome_options)

# Truy cập trang Facebook
driver.get("https://www.facebook.com/")


# Đọc cookie từ file JSON
with open("facebook_cookies.json", "r") as file:
    cookies = json.load(file)

# Thêm cookie vào trình duyệt
for cookie in cookies:
    driver.add_cookie(cookie)


driver.get("https://www.facebook.com/TuvancongtacsinhvienHUMG")
# Đợi một chút để trang tải xong
time.sleep(3)

dem_xt = 0
max_xt = 2
# Tìm nút "Xem thêm" với aria-posinset="1"
temp = driver.find_elements(By.CLASS_NAME, 'x1a2a7pz')
# Lặp qua từng phần tử và tìm nút "Xem thêm" trong mỗi phần tử
for element in temp:
    if dem_xt > max_xt:
        break
    try:
        see_more_button = element.find_element(By.XPATH, './/div[text()="Xem thêm"]')
        # Cuộn đến nút và nhấp vào
        ActionChains(driver).move_to_element(see_more_button).perform()
        see_more_button.click()
        dem_xt += 1
    except Exception as e:
        print(f"Lỗi khi tìm hoặc nhấp nút 'Xem thêm': {e}")


time.sleep(3)

dem = 0
img = []
dem_max = 2
data = []
#Lấy ds post
temp_posts = driver.find_elements(By.CSS_SELECTOR, 'div[aria-posinset]')
for post in temp_posts:
    #Nếu đã lấy hơn sl cần thì dừng
    if dem > dem_max:
        break
    #Tìm tag img của post
    imgs = temp_posts[dem].find_elements(By.CSS_SELECTOR,'img[src]')
    #Nếu có nhiều hơn 1 ảnh thì lấy cả
    if len(imgs)>1:
        img = []
        for i in imgs:
            if 'https://scontent' in i.get_attribute('src'):
                img.append(i.get_attribute('src'))
                # print(img)
    # img_final = '\n'.join(img)
    #lấy nội dung của bài viết
    text = temp_posts[dem].find_element(By.CSS_SELECTOR,'div[data-ad-preview="message"]').text
    # print(text)
    data.append({'content':text,'link':img})
    print({'content':text,'link':img})
    dem+=1

# Đọc dictionary từ tệp JSON
with open('data.json', 'r') as file:
    data_old = json.load(file)
 
def tele(text,img):
    # Thay thế bằng token của bot Telegram của bạn
    api_key = ''
    # Thay thế bằng Chat ID của người dùng hoặc nhóm bạn muốn gửi tin nhắn
    user_id = ''
    bot = Bot(token=api_key)
    async def send_message():
        await bot.send_photo(chat_id=user_id, photo = img, parse_mode='HTML')
        await bot.send_message(chat_id=user_id, text = text,parse_mode='HTML')
    # Xử lý vòng lặp sự kiện đang chạy
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Nếu vòng lặp sự kiện đang chạy, sử dụng loop.create_task
        task = loop.create_task(send_message())
        # Nếu cần, đợi cho task hoàn thành (không phải lúc nào cũng cần thiết)
        # await task
    else:
        # Nếu không có vòng lặp sự kiện đang chạy, sử dụng asyncio.run
        asyncio.run(send_message())

#Kiểm tra nếu khác
if data_old[0]['content'] != data[0]['content']:
    print('Khác')
    link = data[0]['link']
    #Gửi thông báo
    if len(link)>1:
        #Gửi ảnh đầu
        tele(" ",link[0])
        #Gửi ảnh t2 kèm cap
        tele(data[0]['content'],link[1])
    else:
        tele(data[0]['content'],link[0])
    #Lưu lại data
    with open('data.json', 'w',encoding='utf-8') as file:
        json.dump(data, file, indent=4)  # indent=4 để có định dạng dễ đọc
else:
    print('Giống')




