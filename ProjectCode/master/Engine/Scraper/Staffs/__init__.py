from staffScraper import staffScraper

if __name__ == '__main__':
    proxies = {"http": "socks5://127.0.0.1:7890", "https": "socks5://127.0.0.1:7890"}
    scraper = staffScraper(3,proxies=None,config='UC')
    scraper.loadConfig()
    scraper.run()

