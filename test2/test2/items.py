# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#from scrapy import Field, Item
#class Test0Item(Item):
#下面这样就不用写成chinese_name = scrapy.Field()，直接写成chinese_name = Field()

class Test0Item(scrapy.Item):
    # define the fields for your item here like:

#所有cas的url地址尾部,这个写的早，其实后面用不到
#    cas_url_list_big = scrapy.Field()  
#    cas_url_list_small = scrapy.Field()  


        
        
#    中文名称
    chinese_name = scrapy.Field()
#    中文别名
    chinese_alias = scrapy.Field()
#    英文名称
    english_name = scrapy.Field()
#    英文别名
    english_alias = scrapy.Field()
#    cas号
    cas_number = scrapy.Field()
#    EINECS号
    einecs_number = scrapy.Field()
#    分子式
    molecular_formula = scrapy.Field()
#    分子量
    relative_molecular_mass = scrapy.Field()    
#    InChI
    inchi = scrapy.Field()





#    分子结构,分子结构是一张图片，刚开始只能获得名字和链接，再次请求才得到图片
#    molecular_structure_image_in_base64 = scrapy.Field()
#    分子结构链接
    molecular_structure_url = scrapy.Field()
#    分子结构名字
    molecular_structure_name = scrapy.Field()




#    密度
    density = scrapy.Field()
#    熔点
    melting_point = scrapy.Field()
#    沸点
    boiling_point = scrapy.Field()
#    闪点
    flashing_point = scrapy.Field()
#    水溶性
    water_solubility = scrapy.Field()
#    蒸汽压
    vapour_pressure = scrapy.Field()
#    物化性质
    physical_and_chemical_properties = scrapy.Field()
#    产品用途
    product_usage = scrapy.Field()
#    危险性标志
    hazard_symbols = scrapy.Field()    
#    风险术语
    risk_term = scrapy.Field()
#    安全术语
    security_term = scrapy.Field()    
#    上游原料
    upstream_raw_materials = scrapy.Field()
#    下游产品
    downstream_products = scrapy.Field()
  

