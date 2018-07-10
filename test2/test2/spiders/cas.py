# -*- coding: utf-8 -*-

import scrapy
from test2.items import Test0Item
from scrapy_redis.spiders import RedisSpider
import re
#import base64



class CasSpider(RedisSpider):
    name = "cas"

    allowed_domains = ["cheman.chemnet.com", "images-a.chemnet.com"]
    
#    start_urls = ['http://cheman.chemnet.com/dict/zd_more.html']
    redis_key = "casspider:start_urls"
#    headers01 = {
#    'Host':'cheman.chemnet.com',
#    }
    website_possible_httpstatus_list = [404]
    
   
    
    
    
    
    def parse(self, response):
        #判断页面是不是请求成功，不成功的话，给middleware说换个IP
#        if not 'cas' in response:
#            scrapy.Request.meta["change_proxy"] = True
        
        #大分组的所有url
        response = response.body.decode('gb2312', 'ignore')
        reg_of_url_tail_big = re.compile(r'<li><a href="(.*?)"  class="blue">.*?</a></li>')
        cas_list_url_tail_big = reg_of_url_tail_big.findall(response)
        #大分组的所有url
#        item['cas_url_list_big'] = cas_url_lists_big
#        items.append(item)
        
        
        for cas_url_tail_big in cas_list_url_tail_big:
            #取出了所有url链接之后，拼接好。
            cas_url_lists_big = "http://cheman.chemnet.com" + cas_url_tail_big
            yield scrapy.Request(url = cas_url_lists_big, callback = self.parse_url_list_small)

    
    
    def parse_url_list_small(self, response):
        #判断页面是不是请求成功，不成功的话，给middleware说换个IP
#        if not 'cas' in response:
#            scrapy.Request.meta["change_proxy"] = True
            
        response = response.body.decode('gb2312', 'ignore')
        #小分组的所有url
        reg_of_url_tail = re.compile(r'<li class="w22"><a href="(.*?)"  class="blue  xhx">.*?&nbsp;</a></li>')
        cas_list_url_tail = reg_of_url_tail.findall(response)
        for cas_url_tail in cas_list_url_tail:
            #取出了所有url链接之后，拼接好，存储在item上。
            cas_url = "http://cheman.chemnet.com" + cas_url_tail
            yield scrapy.Request(url = cas_url, callback = self.parse_detail)


        
    def parse_detail(self, response):
        #判断页面是不是请求成功，不成功的话，给middleware说换个IP
#        if not 'cas' in response:
#            scrapy.Request.meta["change_proxy"] = True
        
        item = []
        item = Test0Item()
        response = response.body.decode('gb2312', 'ignore')
        reg_item_name = re.compile(r'<.*?"#EFF2FB".*?>(.*?)</td>')
        item_name = reg_item_name.findall(response)
#        print(item_name)
        reg_keys = re.compile(r'<.*?bgcolor="#EFF2FB".*?>(.*?)</td>')#表格左边
        keys = reg_keys.findall(response)
        reg_values = re.compile(r'<.*?bgcolor="#F8F9FD".*?>(.*?)</td>')#表格右边
        values = reg_values.findall(response)
        keys = keys[:len(values) + 1]#水溶性以后的7组奇怪的项目要单独取出来
        if '分子结构：' in keys:
            keys.remove('分子结构：')#删除不规则表格
            molecular_structure_reg1 = re.compile(r'<td align="left" nowrap bgcolor="#F8F9FD"><a href="(.*?)" target="_blank" title=".*?">')
            molecular_structure_url = molecular_structure_reg1.findall(response)#url和name是单独的list不是tuple,得写两个正则
            molecular_structure_reg2 = re.compile(r'<td align="left" nowrap bgcolor="#F8F9FD"><a href=".*?" target="_blank" title="(.*?)">')
            molecular_structure_name = molecular_structure_reg2.findall(response)
            #    print(molecular_structure_url, molecular_structure_name)
            #    分子结构链接,为了提取图片
            item['molecular_structure_url'] = molecular_structure_url[0]
            #    分子结构名字，为了给图片命名
            item['molecular_structure_name'] = molecular_structure_name[0]
#            molecular_structure_image_in_base64 = []
#            item['molecular_structure_image_in_base64'] = molecular_structure_image_in_base64
#            item['molecular_structure_image_in_base64'] = 0
        else:
            molecular_structure_url = []
            item['molecular_structure_url'] = 0
            #    分子结构名字，为了给图片命名
            item['molecular_structure_name'] = 0
#            molecular_structure_image_in_base64 = []
#            item['molecular_structure_image_in_base64'] = molecular_structure_image_in_base64
            item['molecular_structure_image_in_base64'] = 0

        #print(keys)
        #print(values)
        dict_of_excel = dict(zip(keys, values))#变量名和函数名不能重名
        #print(dict_of_excel)
        if '中文名称：' in dict_of_excel:
            item['chinese_name'] = dict_of_excel['中文名称：']
        else:
            item['chinese_name'] = 0

        if '中文别名：' in dict_of_excel:
            item['chinese_alias'] = dict_of_excel['中文别名：']
        else:
            item['chinese_alias'] = 0

        if '英文名称：' in dict_of_excel:
            item['english_name'] = dict_of_excel['英文名称：']
        else:
            item['english_name'] = 0

#            english_name = []
        #这个英文别名有可能是个空格，长度是1，超级坑。
        if '英文别名：' in dict_of_excel and len(dict_of_excel['英文别名：'])!= 1:
#        if '英文别名：' in dict_of_excel:
            item['english_alias'] = dict_of_excel['英文别名：']
        else:
            item['english_alias'] = 0

        if 'CAS号：' in dict_of_excel:
            item['cas_number'] = dict_of_excel['CAS号：']
        else:
            item['cas_number'] = 0

        if 'EINECS号：' in dict_of_excel:
            item['einecs_number'] = dict_of_excel['EINECS号：']
        else:           
            item['einecs_number'] = 0

        if '分子式：' in dict_of_excel:
            item['molecular_formula'] = dict_of_excel['分子式：']
        else:
            item['molecular_formula'] = 0

        if '分子量：' in dict_of_excel:
            item['relative_molecular_mass'] = dict_of_excel['分子量：']
        else:
            item['relative_molecular_mass'] = 0

        if 'InChI：' in dict_of_excel:
            item['inchi'] = dict_of_excel['InChI：']
        else:
            item['inchi'] = 0

        #分子结构行在最前
        if '密度：' in dict_of_excel:
            item['density'] = dict_of_excel['密度：']
        else:
            item['density'] = 0

        if '熔点：' in dict_of_excel:
            item['melting_point'] = dict_of_excel['熔点：']
        else:
            item['melting_point'] = 0

        if '沸点：' in dict_of_excel:
            item['boiling_point'] = dict_of_excel['沸点：']
        else:
            item['boiling_point'] = 0

        if '闪点：' in dict_of_excel:
            item['flashing_point'] = dict_of_excel['闪点：']
        else:
            item['flashing_point'] = 0

        if '水溶性：' in dict_of_excel:
            item['water_solubility'] = dict_of_excel['水溶性：']
        else:
            item['water_solubility'] = 0

        if '蒸汽压：' in dict_of_excel:
            item['vapour_pressure'] = dict_of_excel['蒸汽压：']

        else:
            item['vapour_pressure'] = 0
        if '物化性质：' in dict_of_excel:
            
            item['physical_and_chemical_properties'] = dict_of_excel['物化性质：']
        else:
            item['physical_and_chemical_properties'] = 0

#            physical_and_chemical_properties = []
        if '产品用途：' in dict_of_excel:
            item['product_usage'] = dict_of_excel['产品用途：']
        else:
            item['product_usage'] = 0

#            product_usage = []
        if '<a href="hazard_symbols.html" target="_blank" class="blues">危险性标志:</a>' in item_name:#源代码就是英文的冒号，还缺一张图片,最后尝试单独加，未解决
#            reg_hazard_symbols = re.compile(r'.*?&nbsp;<b>(.*?)</b>(.*?)<br>')
#            hazard_symbols = re.findall(reg_hazard_symbols, response)
        #    print(hazard_symbols)
        
            reg_hazard_symbols = re.compile(r'.*?&nbsp;<b>(.*?)</b>(.*?)<br>')
        #    hazard_symbols = re.findall(reg_hazard_symbols, html)
            
            hazard_symbols_beta = re.findall(reg_hazard_symbols, response)
            hazard_symbols = []
            for iii in hazard_symbols_beta:
                hazard_symbols = hazard_symbols + list(iii)
            item['hazard_symbols'] = "".join(hazard_symbols)
        else:
            item['hazard_symbols'] = 0

#            hazard_symbols = []
        if '<a href="risk_codes.html" target="_blank" class="blues">风险术语：</a>' in item_name:#list里面缺个R,所以用个循环加上
            reg_risk_term = re.compile(r'>R(.*?)</a>.*?<br>')
            risk_term_beta = re.findall(reg_risk_term, response)
            risk_term_seperate = []
            for iii in risk_term_beta:
                to_add_r = 'R{}:;'.format(iii)
                risk_term_seperate.append(to_add_r)
        #    print(risk_term)
            risk_term = ''.join(risk_term_seperate)
            item['risk_term'] = risk_term
        else:
            item['risk_term'] = 0

#            risk_term = []
        if '<a href="safety_description.html" target="_blank" class="blues">安全术语：</a>' in item_name:#list里面缺个S,所以用个循环加上
            reg_security_term = re.compile(r'>S(.*?)</a>.*?<br>')
            security_term_beta = re.findall(reg_security_term, response)
            security_term_seperate = []
            for iii in security_term_beta:
                to_add_s = 'S{}:;'.format(iii)
                security_term_seperate.append(to_add_s)
        #    print(security_term)
            security_term = ''.join(security_term_seperate)
            item['security_term'] = security_term
        else:
            item['security_term'] = 0
               
            
        if '上游原料：' not in item_name and '下游产品：' not in item_name:#上下游分不开啊
            item['upstream_raw_materials'] = 0
            item['downstream_products'] = 0
        
        
            
        elif '上游原料：' in item_name and '下游产品：' not in item_name:
        #    reg_upstream_raw_materials = re.compile(r'<td width="77%" align="left" bgcolor="#F8F9FD">(.*?)</a></td>')
        #    upstream_raw_materials = re.findall(reg_upstream_raw_materials, html)
            
            reg_upstream_raw_materials = re.compile(r"arget='_blank' class='u'(.*?)/a></td>")
            upstream_raw_materials_beta = re.findall(reg_upstream_raw_materials, response)
            reg_upstream_raw_materials_again = re.compile(r'>(.*?)<') 
            upstream_raw_materials_alpha = re.findall(reg_upstream_raw_materials_again, str(upstream_raw_materials_beta))
            upstream_raw_materials = ''.join(upstream_raw_materials_alpha)
            item['upstream_raw_materials'] = upstream_raw_materials
        

            item['downstream_products'] = 0

            
        elif '上游原料：' not in item_name and '下游产品：' in item_name:
        #    reg_downstream_products = re.compile(r'<td width="77%" align="left" bgcolor="#F8F9FD">(.*?)</a></td>')    
        #    downstream_products = re.findall(reg_downstream_products, html)
            
            reg_downstream_products = re.compile(r"arget='_blank' class='u'(.*?)/a></td>")
            reg_downstream_products_beta = re.findall(reg_downstream_products, response)
            reg_downstream_products_again = re.compile(r'>(.*?)<') 
            downstream_products_alpha = re.findall(reg_downstream_products_again, str(reg_downstream_products_beta))
            downstream_products = ''.join(downstream_products_alpha)
            item['downstream_products'] = downstream_products
            
#            print(downstream_products)

            item['upstream_raw_materials'] = 0
            
            
        else:#        if '上游原料：' in item_name and '下游产品：' in item_name:


        #    reg_upstream_raw_materials = re.compile(r'<td width="77%" align="left" bgcolor="#F8F9FD">(.*?)</a></td>')
        #    upstream_raw_materials = re.findall(reg_upstream_raw_materials, html)
            
            reg_upstream_raw_materials = re.compile(r"arget='_blank' class='u'(.*?)/a></td>")
            upstream_raw_materials_beta = re.findall(reg_upstream_raw_materials, response)
            reg_upstream_raw_materials_again = re.compile(r'>(.*?)<') 
            upstream_raw_materials_alpha = re.findall(reg_upstream_raw_materials_again, str(upstream_raw_materials_beta))
        
        
        #    print(upstream_raw_materials_alpha)
        
        
            jjj = 0
            kkk = []
            try:
                index_of_dunhao = upstream_raw_materials_alpha.index('、')
            #    print(count_of_dunhao, index_of_dunhao)
                upstream_raw_materials_alpha_reverse = list(reversed(upstream_raw_materials_alpha))
            #    print(upstream_raw_materials_alpha_reverse)
                index_of_dunhao_reverse = upstream_raw_materials_alpha_reverse.index('、')
            except:
                pass
            #00类型
            if not '、' in upstream_raw_materials_alpha:
                up = upstream_raw_materials_alpha[0]
                down = upstream_raw_materials_alpha[1]
            #01,0n类型
            elif index_of_dunhao == 2:
                up = upstream_raw_materials_alpha[0]
                down = upstream_raw_materials_alpha[1:]
            #10,n0类型
            elif index_of_dunhao_reverse == 2:
                up = upstream_raw_materials_alpha[:-1]
                down = upstream_raw_materials_alpha[-1]
            #11,nn类型
            else:
                for iii in upstream_raw_materials_alpha:
                    if '、' == iii:
                        kkk.append(jjj) 
                    jjj = jjj + 1
                for mmm in range(len(kkk) - 1):
                    if kkk[mmm + 1] - kkk[mmm] > 2:
                        nnn = kkk[mmm] + 2
                        up = upstream_raw_materials_alpha[nnn]
                        down = upstream_raw_materials_alpha[nnn:]
        #    print(kkk)
            upstream_raw_materials = ''.join(up)
            downstream_products = ''.join(down)
            item['upstream_raw_materials'] = upstream_raw_materials
            item['downstream_products'] = downstream_products

            
            
#        print(water_solubility)



        
        if len(molecular_structure_url)> 0: 
            headers_picture = {
            'Host':'images-a.chemnet.com',
#            'User-Agent':random.choice(user_agent_list),
            }
            
            yield scrapy.Request(url = item['molecular_structure_url'], headers = headers_picture, meta = {'meta_3' : item}, callback = self.parse_molecular_structure)
        else:
            yield item
        

#        取出图片
    def parse_molecular_structure(self, response):

            
        meta_3 = response.meta['meta_3']    
        item = []        
        item = meta_3
#        
        picture_name = 'E:\caspicturetest\\' + item['molecular_structure_name'] + '.gif'
        item['molecular_structure_location'] = 'E:\caspicture\\' + item['molecular_structure_name']
        fp = open(picture_name, 'wb')
        fp.write(response.body)
        fp.close()
        return item
        
#        image_as_base64 = base64.b64encode(response.body)
#        molecular_structure_image_in_base64
#        item['molecular_structure_image_in_base64'] = str(image_as_base64)
#        item['molecular_structure_image_in_base64'] = 0

        yield item