"""뉴스 메인을 크롤러를 실행하는 파일입니다."""
import crawlerpack
import csv
import threading
import fire
import sys
from time import sleep


def main_crawl(numThread=15):
    """뉴스 메인을 크롤링합니다
        numThread (int, optional): Defaults to 15. 멀티쓰레드 개수
    """
    # NewsLinkOutput.csv 파일을 읽습니다. 존재하지 않을 시 news_link_cralwer를 먼저 실행해야 합니다. 
    with open('data/NewsLinkOutput.csv', 'r', encoding='utf-8') as csvinput:
        # NewsMainOutput.csv 파일을 만듭니다.
        with open('data/NewsMainOutput.csv', 'w', encoding='utf-8', newline='\n') as csvoutput:
            readcsv = csv.reader(csvinput, delimiter='|')
            # NewsMainOutput.csv 파일의 delimeter는 ','가 아닌 '|'임에 주의합니다.
            # 뉴스 본문에 쉼표가 많은 | 로 delimeter를 설정하였습니다.
            writecsv = csv.writer(csvoutput, delimiter='|')
            row0 = next(readcsv)

            # 첫 번째 줄을 씁니다.
            row0 = ['link', 'title', 'time', 'press', 'isNaver', 'main']
            writecsv.writerow(row0)

            # 크롤러 멀티쓰레드를 만들고 실행합니다
            print("Crawling Start")
            for i, item in enumerate(readcsv):
                info_crawler = crawlerpack.NewsMainCrawler(writecsv, i, item, numThread, onlyNaver=True)
                info_crawler.daemon = True
                info_crawler.start()
                sleep(0.1)

            # 모든 멀티쓰레드가 종료할 때 까지 기다립니다
            main_thread = threading.current_thread()
            for t in threading.enumerate():
                if t is main_thread:
                    continue
                t.join()
            print("Crawling End")

if __name__=='__main__':
    import time
    s_time = time.time()
    fire.Fire(main_crawl)
    print(f"Crawling took {time.time() - s_time} seconds")
