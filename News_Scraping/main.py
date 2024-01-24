import requests
from bs4 import BeautifulSoup


class News:
    def __init__(self,state = None, city = None):
        self.bhaskar_base_url = "https://www.bhaskar.com/"
        self.db_categories = ['career','ayodhya-ram-mandir','db-original',f'mera-shaher/local/{state}/{city}','sports/cricket','entertainment','lifestyle','israel-hamas-war','women','national','international','business','tech-auto','jeevan-mantra','sports','no-fake-news','opinion','madhurima','magazine','happylife','utility']

    def url_builder(self,category):
        category = category.lower()
        if category in self.db_categories:
            return self.bhaskar_base_url + category
    def fetch_bhaskar_news(self,category):
        url = self.url_builder(category=category)
        all_urls_dict = {}
        all_urls = []
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                headlines = soup.find_all(class_='c7ff6507')
                for i in headlines:
                    for j in i.contents:
                        all_urls_dict[j.text] = []
                        slug = j.get('href')
                        if slug:
                            all_urls_dict[j.text].append(url+slug)
                            all_urls.append(url+slug)
                for key,value in all_urls_dict.items():
                    headline = key
                    news = ''''''
                    for i in value:
                        response = requests.get(i)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        news_element = soup.find_all('p')
                        for n in news_element:
                            news += n.text
                    print("_"*len(headline))
                    print(headline)
                    print("_"*len(headline))
                    print(news)
                    print("\n")
            else:
                print("Webpage not responding, Code: " + str(response.status_code))
        except Exception as e:
            print("There was an error", str(e))



    
if __name__ == "__main__":
    dbnews = News(state='haryana', city = 'gurugram')
    print(f"Choose from the categories listed: \n{dbnews.db_categories}")
    cat = input("Enter category: ")
    dbnews.fetch_bhaskar_news(category=cat)



