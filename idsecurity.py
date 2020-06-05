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
titles=['Product_url', 'descriptions', 'retail price', 'sales price', 'category', 'product type', 'item #', 'Manufacture Name', 'Sku', "variants", "image_path"]
with open('idsecurity.csv', mode='a', encoding="utf8", newline='') as student_file:
    student_writer = csv.writer(student_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    student_writer.writerow(titles)

def get_product_info(url):
  print(url)
  product_info = ['','','','','','','','','','','']
  product_info[0] = url
  product_content_page = requests.get(url)

  product_content = soup(product_content_page.content, 'html.parser')

  product_info[6] = product_content.find('strong',{'class':'js_sku'}).text
  product_info[8] = product_content.find('strong',{'class':'js_sku'}).text
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
  with open('idsecurity.csv', mode='a', encoding="utf8", newline='') as product:
    student_writer = csv.writer(product, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    student_writer.writerow(product_info)

def main():
  product_list_contents = requests.get("https://www.idsecurityonline.com/single-sided-photo-id-system/")

  product_list_content = soup(product_list_contents.content, 'html.parser')

  product_lists = product_list_content.findAll("div",{'class':'col-sm-12 col-md-12 col-lg-6'})

  for product_list in product_lists:
    get_product_info(product_list.div.div.a['href'])

main()
# get_product_info('https://www.idsecurityonline.com/zenius-classic-base-model-usb-fire-red-photo-id-system.htm')
