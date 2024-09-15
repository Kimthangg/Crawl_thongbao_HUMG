from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

email = ''
password = ''
# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Mở trang đăng nhập Facebook
driver.get('https://www.facebook.com')
time.sleep(3)
# Tìm và nhập email
email_input = driver.find_element(By.ID, 'email')
email_input.send_keys(email)

# Tìm và nhập mật khẩu
password_input = driver.find_element(By.ID, 'pass')
password_input.send_keys(password)
time.sleep(1)
# Nhấn nút đăng nhập
password_input.send_keys(Keys.RETURN)

# Đợi một lúc cho trình duyệt xử lý đăng nhập
time.sleep(5)

# Lấy cookie
cookies = driver.get_cookies()

# Đóng trình duyệt
driver.quit()

# Lưu cookie vào tệp JSON
with open('facebook_cookies.json', 'w') as file:
    json.dump(cookies, file)

print("Cookies đã được lưu vào facebook_cookies.json")
