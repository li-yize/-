from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
import time
import pandas as pd

# 配置 Edge 浏览器选项
options = Options()

# 创建 Service 对象并通过 WebDriver Manager 自动安装 WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# 打开目标网页
url = "https://re.jd.com/search?keyword=%e4%ba%ac%e4%b8%9c&ev=brand_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89&keywordid=172887082207&re_dcp=202m0QjIIg==&traffic_source=1004&enc=utf8&cu=true&utm_source=baidu-search&utm_medium=cpc&utm_campaign=t_262767352_baidusearch&utm_term=172887082207_0_6a1293cf4a7147219c15fc4d9a9fcf45"
driver.get(url)

# 等待页面加载
time.sleep(5)

# 初始化商品列表
product_list = []

# 定义函数：爬取当前页面的商品信息
def scrape_current_page():
    global product_list
    try:
        # 商品名称和价格的 CSS Selector 模板
        name_selector_template = "#shop_list > li:nth-child({}) > div > div.li_cen_bot > a > div.commodity_tit"
        price_selector_template = "#shop_list > li:nth-child({}) > div > div.li_cen_bot > a > div.commodity_info > span"

        # 遍历商品
        for i in range(1, 50):  # 假设最多有 50 个商品，按需调整
            try:
                # 获取名称
                name_selector = name_selector_template.format(i)
                name = driver.find_element("css selector", name_selector).text

                # 获取价格
                price_selector = price_selector_template.format(i)
                price = driver.find_element("css selector", price_selector).text

                # 添加到列表
                product_list.append({"商品名称": name, "价格": price})
                print(f"已爬取商品: {name} - {price}")
            except Exception:
                # 如果当前索引商品不存在，跳过
                break
    except Exception as e:
        print(f"爬取当前页面商品时出错: {e}")

# 定义函数：检查并点击“下一页”按钮
def go_to_next_page():
    try:
        # 定位下一页按钮
        next_button = driver.find_element("css selector", "#page > a.pn-next")
        # 如果按钮可见并可点击，则点击
        if "javascript:;" in next_button.get_attribute("href"):
            next_button.click()
            time.sleep(5)  # 等待页面加载
            return True
        else:
            print("没有下一页按钮了！")
            return False
    except Exception as e:
        print(f"下一页按钮无法点击: {e}")
        return False

# 开始爬取
try:
    while True:
        # 爬取当前页面
        scrape_current_page()
        # 尝试点击下一页，如果没有下一页则退出循环
        if not go_to_next_page():
            break

    # 创建 DataFrame
    df = pd.DataFrame(product_list)

    # 保存为 Excel 文件到指定路径
    excel_path = r"E:\桌面\新建文件夹\华为手机信息_所有商品.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"所有商品数据已保存到 {excel_path}")

except Exception as e:
    print(f"爬取时出错: {e}")

# 关闭浏览器
driver.quit()
