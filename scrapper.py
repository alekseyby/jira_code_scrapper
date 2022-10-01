import os
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from requests_html import HTMLSession
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from urllib.parse import unquote

LOGIN = 'XXXXX'
PASS = 'XXXXX'
HOME_URL = 'https://jira.XXXXX.com'
PROJECT_URL = f'{HOME_URL}/secure/bbb.gp.gitviewer.BrowseGit.jspa?repoId=157&branchName=main&tagName=&commitName=9bd0429eee72a145447c6e1705a7d195f61b5a05&commitId=&gkEnabled=true&gkRepoUrl=gitkraken%3A%2F%2Frepolink%2F5fa5db4ae9a3b791ee0cac2f69c45e4f0d8d0b89%3Furl%3Dssh%253A%252F%252Fgit%254010.50.168.50%252Fitv-api-gateway%252Fapi-gateway&gkBranchUrl=gitkraken%3A%2F%2Frepolink%2F5fa5db4ae9a3b791ee0cac2f69c45e4f0d8d0b89%2Fbranch%2Fmain%3Furl%3Dssh%253A%252F%252Fgit%254010.50.168.50%252Fitv-api-gateway%252Fapi-gateway&gkCommitUrl=gitkraken%3A%2F%2Frepolink%2F5fa5db4ae9a3b791ee0cac2f69c45e4f0d8d0b89%2Fcommit%2F9bd0429eee72a145447c6e1705a7d195f61b5a05%3Furl%3Dssh%253A%252F%252Fgit%254010.50.168.50%252Fitv-api-gateway%252Fapi-gateway&uri=%3FrepoId%3D157%26branchName%3Dmain%26tagName%3D%26commitId%3D%26path%3Dqa_apigw_tests%2Ftests%2Fcommon'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.3'}
visited_links = []


def get_data(page, folder_dir):

    folder_links = []
    driver.get(page)
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    files_rowss = soup.find_all('div', {'class': 'bbb-gp-gitviewer-files-list__row'})
    for file_attr in files_rowss[1::]:
        href = (file_attr.find('a', {'class': 'bbb-gp-gitviewer-files-list__name-link'}).get('href'))
        if href != '#' and href.split('=')[-1] != '' and href.split('=')[-1] not in visited_links:
            folder_links.append(href)
            # create folders
            folder_name = href.split('=')[-1]
            if folder_name.split('=')[-1] == '':
                pass
            else:
                try:
                    folder_name = folder_name.replace('%2F', '/')
                    print("Creating folder - " + unquote(folder_name))
                    os.makedirs(f'{folder_name}', exist_ok=True)
                except FileNotFoundError as e:
                    print(e)
        if href == '#':
            path = (file_attr.find('a', {'class': 'bbb-gp-gitviewer-files-list__name-link'}).get('path'))
            file_name = path.split('/')[-1]
            print('Copy ' + file_name + f' ------->  {unquote(folder_dir)}/{file_name}')


            # FILE_URL = f"{HOME_URL}/rest/gitplugin/latest/files/27/8e54b1a9bcf94105bcf74a30913bb13f56aae074/{file_name}"
            FILE_URL = f"{HOME_URL}/rest/gitplugin/latest/files/157/9bd0429eee72a145447c6e1705a7d195f61b5a05/{path}"
            response = requests.get(FILE_URL,
                                    auth=HTTPBasicAuth(LOGIN, PASS), headers=headers)
            try:
                # open(f"{folder_dir}/{file_name}", "wb").write(response.content)
                open(f"{path}", "wb").write(response.content)
            except FileNotFoundError as e:
                print(e)
    for link in folder_links:
        folder_dir = link.split('=')[-1].replace('%2F', '/')
        print("Go to foder  - " + folder_dir)
        visited_links.append(link.split('=')[-1])
        get_data(HOME_URL + link, folder_dir)


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(PROJECT_URL)
time.sleep(20) # timout to have a time login via real page
get_data(PROJECT_URL, '')
