'''네이버 뉴스 링크 크롤러와 메인 내용 크롤러 클래스가 있는 파일입니다.'''
import requests
import threading
from bs4 import BeautifulSoup
from logger import getMyLogger

# 로깅 남길 로거 얻기
mylogger = getMyLogger()


class NewsMainCrawler(threading.Thread):
    """뉴스의 메인 내용 멀티 쓰레딩 크롤러

    Naver 뉴스로 올라가 있는 경우 본문만 크롤링 되지만,
    자체 뉴스사이트로 링크가 존재할 시 html 파일을 통째로 가져옵니다. 

    Args:
        threading (Thread): 멀티쓰레딩 클래스를 구현하기 위한 부모 클래스
    """

    def __init__(self, csvfile, num, item, numThread=15):
        """생성자 설정

        Args:
            csvfile (csv파일 포인터): csv.writecsv() 함수로 리턴받은 csv 파일 포인터
            num (int): link의 순서
            item (list): csv 한 로우를 포함한 string
            numThread (int, optional): Defaults to 15. 멀티쓰레드 풀의 수. 클수록 동시에
                많은 멀티쓰레드 크롤러가 작동합니다.
        """
        threading.Thread.__init__(self)
        self.csvfile = csvfile
        self.num = num
        self.item = item
        self.link = item[0]
        self.title = item[1]
        self.time = item[2]
        self.press = item[3]
        self.isNaver = item[4]

        # 실제 사용자 처럼 보이기 위한 해더 추가
        self.header = {"Referer": self.link,
                       "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"}
        self.threadLimiter = threading.BoundedSemaphore(numThread)

        self.main = None

        # thread 클래스 생성 로그
        mylogger.info(f"{self.num} thread generate")

    def get_news(self):
        """링크로 부터 뉴스를 크롤링해서 정보를 리스트로 만들어 리턴"""
        link = self.link
        headers = self.header
        try:
            # 네이버에 request를 보냄
            response = requests.get(link, headers=headers)
            encoding = response.encoding

            # response를 받을 시 로그 남김
            mylogger.info(
                f"{self.num} | {self.press} requests get, {self.title}")

            # soup 객체로 파싱
            # 실제 한글이 euc-kr인코딩일 시 jsp에서 서버쪽의 오류로 ISO-8859-1로 보내는 경우가 있다고함
            # 이를 위해 올바른 인코딩으로 교체
            if encoding == "ISO-8859-1":
                response.encoding = 'euc-kr'
            html = response.text
            print(response.encoding)
            
            soup = BeautifulSoup(html, 'html.parser')
            entertainment = "https://m.entertain.naver.com"
            news = "https://m.news.naver.com"

            # 네이버 엔터테이먼트 뉴스일 시 파싱
            if response.url[:len(entertainment)] == entertainment:
                main = soup.find('div', {'id': 'contentArea'}).text
            # 네이버 뉴스일 시 파싱
            elif response.url[:len(news)] == news:
                main = soup.find('div', {'id': 'dic_area'}).text
            # 다른 신문사 뉴스일 시 파싱
            else:
                for script in soup(["script", "style"]):
                    script.decompose()
                try:
                    # 바디 파트 파싱
                    main = soup.find('body').get_text()
                except Exception as e:
                    # 에러 발생 시 전체 파싱
                    main = soup.get_text()
                    mylogger.info(
                        f"Reload in {self.num} | {self.press} | {self.link}")
            # 줄바꿈 빈칸으로 교체
            self.main = main.replace('\r',"").replace('\n',"")

        except Exception as e:
            # 크롤링 과정에서 오류 발생시 에러문 로깅
            mylogger.error(
                f"Error in {self.num} | {self.press} : " + str(e) + f"| {self.link}")

    def run(self):
        """멀티쓰레드로 실행되는 함수"""
        # 클레스의 파라미터로 주어진 numThread에 맞게 thread 수 설정
        self.threadLimiter.acquire()
        try:
            # 크롤링 후 csv 파일 쓰기
            self.get_news()
            item = [self.link, self.title, self.time,
                    self.press, self.isNaver, self.main]
            self.csvfile.writerow(item)
        except Exception as e:
            # 에러 발생시 로깅
            mylogger.error(f"Error in {self.num}, {self.press} : " + str(e))
        finally:
            #  끝날 때 로깅
            mylogger.info(f"{self.num} finish")
            self.threadLimiter.release()


class NaverNewsLinkCrawler(threading.Thread):
    """네이버 뉴스 링크 크롤러

    주어진 키워드의 특정 순서의 기사 제목, 링크, 언론사, 시간, Navernews여부를
    크롤링 하고 csv 파일에 쓴다.

    Args:
        threading (Thread): 멀티쓰레드를 위한 부모 클래스
    """

    def __init__(self, csvfile, item, numThread=15):
        """생성자 설정

        Args:
            csvfile (csv파일 포인터): csv.writecsv() 함수로 리턴받은 csv 파일 포인터
            item (list): csv 한 로우를 포함한 string
            numThread (int, optional): Defaults to 15. 멀티쓰레드 풀의 수. 클수록 동시에
                많은 멀티쓰레드 크롤러가 작동합니다.
        """
        threading.Thread.__init__(self)
        self.csvfile = csvfile
        self.item = item
        self.num = item[0]
        self.keyword = item[1]
        self.link = f"https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query={self.keyword}&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all&start={self.num}".encode(
            'utf-8')
        self.header = {"Referer": self.link,
                       "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"}
        self.news_list = None
        self.threadLimiter = threading.BoundedSemaphore(numThread)

        mylogger.info(f"{self.num} thread generate")

    def get_news_info(self):
        """주어진 키워드와 순서의 기사 정보를 클롱링해서 list로 만든다"""
        link = self.link
        headers = self.header
        try:
            # 서버에 request를 보냄
            response = requests.get(link, headers=headers)

            # response를 받을 시 로깅
            mylogger.info(f"{self.num} | {self.keyword} requests get")
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # mylogger.info(soup)

            # 필요한 부분 파싱
            # FIXME : 현재 홈페이지가 바뀌어 파싱이 안되는 것으로 판단됩니다. 변경이 필요합니다.
            news_articles = soup.find_all('div', {'class': "news_wrap"})
            self.news_list = [NewsWrapper(wrapper).parsing()
                              for wrapper in news_articles]
        except Exception as e:
            # 크롤링 과정에서 오류 발생시 로깅
            mylogger.error(f"Error in {self.num}, {self.keyword} : " + str(e))

    def run(self):
        """멀티쓰레드로 실행되는 함수"""
        self.threadLimiter.acquire()
        try:
            # 뉴스 정보 크롤링 후 csv에 쓰기
            self.get_news_info()
            for item in self.news_list:
                self.csvfile.writerow(item)
        except Exception as e:
            # 에러 발생시 로깅
            mylogger.error(f"Error in {self.num}, {self.keyword} : " + str(e))
        finally:
            # 크롤링 종료시 로깅
            mylogger.info(f"{self.num} finish")
            self.threadLimiter.release()


class NewsWrapper(object):
    """네이버 뉴스 링크 wapper를 파싱"""

    def __init__(self, wrapper):
        self.wrapper = wrapper
        # mylogger.info("NewsWrapper")
        # mylogger.info(wrapper)

    def parsing(self):
        """주어진 wapper에서 정보 파싱하여 list로 만들어 return"""
        try:
            link = self.wrapper.find('a', {'class':'news_tit'})['href']
            mylogger.info(link)
            title = self.wrapper.find('div', {'class': 'api_txt_lines tit'}).text
            mylogger.info(title)
            time = self.wrapper.find('span', {'class': 'sub_txt sub_time'}).text
            mylogger.info(time)
            press = self.wrapper.find('cite', {'class': 'sub_txt'}).text
            mylogger.info(press)
            naver = "https://m.news.naver.com"
        except:
            mylogger.error(self.wrapper)

        # 네이버 뉴스인지 아닌지 추가
        if link[:len(naver)] == naver:
            isNaver = "O"
        else:
            isNaver = "X"
        return [link, title, time, press, isNaver]
