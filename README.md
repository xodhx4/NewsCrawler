# 네이버 뉴스 멀티쓰레딩 크롤러

## 설명

검색하고 싶은 뉴스 `키워드`를 입력하여 나온 결과를 크롤링  하여 csv 파일을 만드는 프로그램입니다.  두 가지 프로그램이 포함되어 있습니다.

최신순서 기준으로 최대 4000개까지 크롤링합니다.

### news_link_crawler.py

- 실행방법

`python news_link_crawler.py 키워드`

뉴스의 본문을 제외한 [제목, 뉴스링크, 시간, 언론사, 네이버뉴스여부]를 크롤링 합니다.

결과는 `./data/NewsLinkOutput.csv`에 저장됩니다.

### news_main_crawler.py

- 실행방법

`python news_main_crawler.py`

`./data/NewsLinkOutput.csv` 파일을 읽어드려 파일에 존재하는 뉴스 링크의 본문을 크롤링합니다. 

결과는 `./data/NewsMainOutput.csv`에 저장됩니다.

### 주의할 점

1. `news_link_crawler.py`가 먼저 실행된 이후에 `news_main_crawler.py` 실행 가능합니다.

2. 뉴스 본문의 쉼표가 많기 때문에 `NewsLinkOutput.csv`, `NewsMainOutput.csv` 파일의 delimiter는 `|` 이므로 결과를 읽을 때 주의하시기 바랍니다.

   ```python
   import pandas as pd
   df = pd.read_csv('NewsMainOutput.csv', sep='|')
   ```

3. csv의 인코딩이 `utf-8`로 되어있기 때문에 윈도우에서 엑셀로 열 경우 한글이 깨져보일 수도 있습니다. 

## 설치

1. 레포지토리 설치

   ```sh
   # git bash에서
   git clone https://github.com/xodhx4/NewsCrawler.git
   ```

2. 필요 패키지 다운로드

   - 다음과 같은 패키지가 설치되어 있지 않으면 설치가 필요합니다

     - fire
     - requests
     - beautifulsoup4

     ```sh
     pip install fire
     pip install requests
     pip install beautifulsoup4
     ```

   - 만약 anaconda가 깔려 있다면 바로 콘다 환경을 만들 수 있습니다.

     ```sh
     # repo 폴더 안에서
     conda env create -f env.yml
     ```

     `crawler`라는 콘다 환경이 생성됩니다.

## TODO

- [ ] 네이버 뉴스를 제외한 뉴스 파서 추가
- [ ] interactive shell 제작

