""" from langchain.document_loaders import UnstructuredURLLoader

urls = [
    "https://cn.cryptonews.com/exclusives/jia-mi-huo-bi-chu-xu-zhang-hu-crypto-savings-accounts-ta-men-shi-shen-me-yi-ji-shi-fou-zhi-de-yong-you.htm",
    "https://cn.cryptonews.com/news/bi-an-binance-shou-xi-zhi-xing-zhang-zhao-zhang-peng-ling-xian-zan-yang-ou-meng-xin-chu-lu-de-jia-mi-huo-bi-fa-gui-mica.htm",
    "https://www.bbc.com/zhongwen/trad/business-63620144",
]

loader = UnstructuredURLLoader(urls=urls)

data = loader.load()
print(len(data))

print(data) """

from langchain.document_loaders import SeleniumURLLoader

urls = [
    "https://cn.cryptonews.com/exclusives/jia-mi-huo-bi-chu-xu-zhang-hu-crypto-savings-accounts-ta-men-shi-shen-me-yi-ji-shi-fou-zhi-de-yong-you.htm",
    "https://www.bbc.com/zhongwen/trad/topics/czp2ywe1qwmt",
    "https://www.bbc.com/zhongwen/trad/business-63620144",
    "https://www.dailyfxasia.com/cn/bitcoin/news-and-analysis",
    "https://www.dailyfxasia.com/cn/cmarkets/20230417-23719.html",
    "https://cn.cryptonews.com/news/bi-an-binance-shou-xi-zhi-xing-zhang-zhao-zhang-peng-ling-xian-zan-yang-ou-meng-xin-chu-lu-de-jia-mi-huo-bi-fa-gui-mica.htm",

]

loader = SeleniumURLLoader(urls=urls)

data = loader.load()
print(len(data))

print(data)
