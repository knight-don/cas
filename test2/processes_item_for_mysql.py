# -*- coding: utf-8 -*-

import redis
import pymysql
import json


def process_item():


    redisconn = redis.Redis(
            host = "192.192.192.192",
            port = 6379,
            db = 0
            )
    

    mysqlconn = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "1111111",
            passwd = "1111111",
            db = "casscrapy",
            charset = 'utf8'
            )
    
    while True:

        source, data = redisconn.blpop("cas:items")
        
        item = json.loads(data)
        
        try:
            cur = mysqlconn.cursor()
            
            cur.execute("insert into cas(中文名称ChineseName, 中文别名ChineseAlias, 英文名称EnglishName, 英文别名EnglishAlias, CAS号CASNumber, EINECS号EINECSNumber, 分子式MolecularFormula, 分子量RelativeMolecularMass, InChI, 分子结构MolecularStructure, 密度Density, 熔点MeltingPoint, 沸点BoilingPoint, 闪点FlashingPoint, 水溶性Water_solubility, 蒸汽压VapourPressure, 物化性质PhysicalandChemicalProperties, 产品用途ProductUsage, 危险性标志HazardSymbols, 风险术语RiskTerm, 安全术语SecurityTerm, 上游原料UpstreamRawMaterials, 下游产品DownstreamProducts) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(item['chinese_name'], item['chinese_alias'], item['english_name'], item['english_alias'], item['cas_number'], item['einecs_number'], item['molecular_formula'], item['relative_molecular_mass'], item['inchi'], item['molecular_structure_image_in_base64'], item['density'], item['melting_point'], item['boiling_point'], item['flashing_point'], item['water_solubility'], item['vapour_pressure'], item['physical_and_chemical_properties'], item['product_usage'], item['hazard_symbols'], item['risk_term'], item['security_term'], item['upstream_raw_materials'], item['downstream_products']))
        
            mysqlconn.commit()
            
            cur.close()
        except:
            pass
    
if __name__ == "__main__":
    process_item()
    