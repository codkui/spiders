from selenium import webdriver
 
# 创建chrome参数对象
opt = webdriver.ChromeOptions()
# opt.add_argument("--proxy-server=http://127.0.0.1:1080")

# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
opt.set_headless()


# 创建chrome无界面对象
driver = webdriver.Chrome(options=opt)


# 访问百度
driver.get('https://www.google.com/')
print (driver.page_source)