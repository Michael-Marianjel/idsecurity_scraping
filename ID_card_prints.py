from bs4 import BeautifulSoup as soup
from random import randint
from multiprocessing import Pool
import requests
import re
import random
import time
import csv 
import urllib.request
# generate the csv
# titles=['product name', 'item #', 'descriptions', 'Manufacture Name', 'retail price', 'sales price', 'category1', 'category2', 'category3', 'Sku', "variants", "image_path"]
# with open('id_card_prints.csv', mode='a', encoding="utf8", newline='') as student_file:
#     student_writer = csv.writer(student_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#     student_writer.writerow(titles)

def get_product_info(url):
  print(url)
  product_info = ['','','','','','','','','','','']
  # product_info[0] = url
  product_content_page = requests.get(url)

  product_content = soup(product_content_page.content, 'html.parser')

  product_info[6] = product_content.find('strong',{'class':'js_sku'}).text
  product_info[8] = product_info[6] 
  try:
    variants = product_content.find('select',{'class','product_option form-control'}).findAll("option")

    for variant in variants:
      product_info[9] += variant.text + "\n"
    if ( product_content.find('span',{'class':'retail_price2show js_msrp_container'}) != None ):
      product_info[2] = product_content.find('span',{'class':'retail_price2show js_msrp_container'}).text
  except:
    pass
  else:
    try:
      product_info[2] = product_content.find('span',{'class':'retail_price2show js_price_container'}).text
    except:
      pass
  try:
    product_info[3] =  product_content.find('span',{'class':'sale_price2show js_price_container'}).text
  except:
    pass
  product_info[7] = product_content.find('div',{'class':'vendor'}).strong.text
  try:
    product_info[1] = re.sub('\s\s+',' ',product_content.find('div',{'class':'desc_pan'}).text)
  except:
    pass
  product_info[5] = product_content.find('h1',{'class':'title_zoom'}).text
  category_lists = product_content.findAll('li',{'class':'breadcrumb-item path'})

  image_url = product_content.find('div',{'class':'pict_zoom'})
  urllib.request.urlretrieve(image_url.a.img['src'], "./product_images/" + product_info[6] + ".jpg")
  product_info[10] = "./product_images/" + product_info[6] + ".jpg"
  for i in range(len(category_lists)):
    if i == 0:
      product_info[4] += category_lists[i].text
    else:
      product_info[4] += " / " + category_lists[i].text
  with open('id_card_prints.csv', mode='a', encoding="utf8", newline='') as product:
    student_writer = csv.writer(product, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    student_writer.writerow(product_info)

def main():
  product_content_list = []
  product_category_contents = requests.get("https://www.idsecurityonline.com/id-card-printers/")
  products_category = soup(product_category_contents.content, 'html.parser')
  category_list_contents = products_category.find("div",{'class','shopbybrand'}).findAll('li')

  for category_list_content in category_list_contents:
    product_list_contents = requests.get(category_list_content.a['href'])

    product_list_content = soup(product_list_contents.content, 'html.parser')

    product_lists = product_list_content.findAll("div",{'class':'cat-logo_desc'})
    for product_list in product_lists:
      if ( product_list.a['href'].count('https') > 0):
        product_contents = requests.get(product_list.a['href'])
        product_content = soup(product_contents.content, 'html.parser')

        item_lists = product_content.findAll('div',{'class':'col-sm-12 col-md-12 col-lg-6'})
        for item_list in item_lists:
          product_content_list.append(item_list.find('div',{'class':'pict'}).a['href'])
      else:
        product_content_list.append("https://www.idsecurityonline.com"+product_list.a['href'])
      # get_product_info("https://www.idsecurityonline.com"+product_list.div.a['href'])
  print(len(product_content_list))
main()
# get_product_info('https://www.idsecurityonline.com/zenius-classic-base-model-usb-fire-red-photo-id-system.htm')
