"""네이버 뉴스 정보 크롤링을 실행하는 파일입니다."""
import crawlerpack
import csv
from time import sleep
import threading
import fire

# KEYWORD="미세먼지"


def link_crawl(KEYWORD, numThread=15):
    """주어진 키워드로 최신 뉴스기사 4000건을 멀티쓰레드 크롤링 한다

    Args:
        KEYWORD (string): 네이버에 검색할 키워드
        numThread (int, optional): Defaults to 15. 멀티쓰레드의 개수
    """
    with open('data/NewsLinkOutput.csv', 'w', encoding='utf-8', newline='\n') as csvoutput:
        # csv 파일 생성 후 첫 줄 만들기
        writecsv = csv.writer(csvoutput)
        row0 = ['link', 'title', 'time', 'press', 'isNaver']
        writecsv.writerow(row0)

        # 크롤러 멀티쓰레드를 만들고 실행합니다
        print("Crawling Start")
        for index in range(1, 4000, 15):
            info_crawler = crawlerpack.NaverNewsLinkCrawler(
                writecsv, [index, KEYWORD], numThread)
            info_crawler.daemon = True
            info_crawler.start()
            sleep(1)

        # 모든 멀티쓰레드가 종료할 때 까지 기다립니다
        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()

        print("Crawling End")

if __name__ == '__main__':
    import time
    s_time = time.time()
    fire.Fire(link_crawl)
    print(f"Crawling took {time.time() - s_time} seconds")
