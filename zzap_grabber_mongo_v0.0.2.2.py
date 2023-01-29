from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
# from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
s = Service('./chromedriver')

driver = webdriver.Chrome()

car_main_link='https://zzap.laximo.online/index.php?task=vehicles&ft=findByWizard2&c=BMW201910&ssd=$*KwHqss-g6eAAAAAAdMWlhA==$'

# import selenium
def grabber (model_0,
             series_code_0,
             series_description_0,
             region_0,
             engine_0,
             gearbox_0,
             bodyStyle_0,
             steering_0,
             links_0,
             driver):

   
    def wait_for_element(driver, xpath):
        try:
            element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            print('ОШИБКА! Искомого элемента нет 0.1 с')
            element=1
            pass
        return element
    def right_part_collect(driver, leaf):
        # сборка правой части
        first_lvl_id_list = []
        first_lvl_name_list = []
        img_list=[]
        gogo = 0
        
        while True:
            gogo = wait_for_element(driver, "//div[@class='gdImage']/..//a/*[1]")

            if gogo != 0 and gogo != 1:
            
                first_lvl_id = driver.find_elements(By.XPATH, "//div[@class='gdImage']/..//a/*[1]")
                first_lvl_name = driver.find_elements(By.XPATH, "//div[@class='gdImage']/..//*[3]")
                img_ = driver.find_elements(By.XPATH, "//div[@class='gdImage']/../*[2]/*")
                
                break
        

        # собираем все правые узлы

        while True:
            try:
                for i in range(0, len(first_lvl_id)):
                    z = first_lvl_id[i].get_attribute('textContent')
                    zz = first_lvl_name[i].get_attribute('textContent')
                    img= str(img_[i].get_attribute('src')).replace("250","source")
                    z = str(z).replace(' ', '')
                    z = str(z).replace('\n', '')
                    zz = str(zz).replace('  ', '')
                    zz = str(zz).replace('\n', '')
                    first_lvl_id_list.append(z)
                    first_lvl_name_list.append(zz)
                    img_list.append(img)
                    
                break
            except Exception as inst:
                print(inst)
                
                first_lvl_id = driver.find_elements(By.XPATH, "//div[@class='gdImage']/..//a/*[1]")
                first_lvl_name = driver.find_elements(By.XPATH, "//div[@class='gdImage']/..//*[3]")
                print("ОШИБКА! Проблема с прогрузкой узла")
                pass
        
        # прокликиваем свернутое справа
        
        rest_parts_w = wait_for_element(driver, "//td[@colspan='99']/*[1]")
        try:
            rest_parts = driver.find_elements(By.XPATH, "//td[@colspan='99']/*[1]")
        except:
            print("ОШИБКА! Не найдена кнопка Остальные узлы")

            
        while True:
            try:
                for j in range(0, len(rest_parts)):
                    rest_parts[j].click()
                break
            except Exception as ex:
                rest_parts = driver.find_elements(By.XPATH, "//td[@colspan='99']/*[1]")
                template = "ОШИБКА! Проблема при попытке прокликать Остальные узлы"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        # print(first_lvl_id_list)
        # собираем названия и партномера
        part_names = []
        part_nums = []
        knot_name = []
        knot_code = []
        knot_img=[]
        leaf_list = []
        for i in range(0, len(first_lvl_id_list)):
            xpath = "//b[contains(text(),'" + first_lvl_id_list[i] + "')][1]/../../../*[2]/*/*/*/*[4]"
            xpath2 = "//b[contains(text(),'" + first_lvl_id_list[i] + "')][1]/../../../*[2]/*/*/*/*[3]"
            # print(xpath)
            parts_name = driver.find_elements(By.XPATH, xpath)
            parts_num = driver.find_elements(By.XPATH, xpath2)
            for j in range(0, len(parts_name)):
                z = parts_name[j].get_attribute('textContent')
                z = str(z).replace('  ', '')
                z = str(z).replace('\n', '')
                part_names.append(z)
                knot_code.append(first_lvl_id_list[i])
                knot_name.append(first_lvl_name_list[i])
                knot_img.append(img_list[i])
                zz = parts_num[j].get_attribute('textContent')
                zz = str(zz).replace('  ', '')
                zz = str(zz).replace('\n', '')
                part_nums.append(zz)
                leaf_list.append(leaf)
                
        data = {'level3/4': leaf_list,
                'knot_name': knot_name,
                "knot_code": knot_code,
                "knot_img": knot_img,
                "part_names": part_names,
                "part_nums": part_nums}
        df10 = pd.DataFrame(data)
        except_list = ['OEM']
        df11 = df10[df10.part_nums.isin(except_list) == False]
        return df11
    def left_side_build(knots_list,driver):
        # функция сбора левой части иерархии каталога
        main_=[]
        layer1=[]
        for i in range(0,len(knots_list)):
            xpath="(//span[contains(text(),'"+str(knots_list[i])+"')])/../../../*/*/*/div[@class='group-name']/a | (//span[contains(text(),'"+str(knots_list[i])+"')])/../../../*/*/*/div[@class='group-name']/span"
            # print(xpath)
            level_2_list=driver.find_elements(By.XPATH, xpath)
            #print(level_2_list)
            for j in range(0,len(level_2_list)):
                z=level_2_list[j].get_attribute('textContent')
                main_.append(knots_list[i])
                layer1.append(z)
        # print(len(main_))
        # print(main_[0:10])
        # print(len(layer1))
        # print(layer1[0:10])
        data={"main":main_,"level1":layer1}
        df1=pd.DataFrame(data)
        # df1
        layer2=[]
        layer1_2=[]
        main_2=[]
        for i in range(0,len(layer1)):
            # **********************************************************************************************************
            xpath="(//span[contains(text(),'"+str(layer1[i])+"')])/../../../*/*/*/div[@class='group-name']/a | (//span[contains(text(),'"+str(layer1[i])+"')])/../../../*/*/*/div[@class='group-name']/span | //a[contains(text(),'"+str(layer1[i])+"')]/../../../*[3]/*/*/*/*"
            # **********************************************************************************************************
            # print(xpath)
            # "(//span[contains(text(),'Фильтр масляный')])/../../../*/*/*/div[@class='group-name']/a | (//span[contains(text(),'Фильтр масляный')])/../../../*/*/*/div[@class='group-name']/span | //a[contains(text(),'Фильтр масляный')]/../../../*[3]/*/*/*/*"
            level_3_list=driver.find_elements(By.XPATH, xpath)
            for j in range(0,len(level_3_list)):
                z=level_3_list[j].get_attribute('textContent')
                # print(z)
                layer1_2.append(layer1[i])
                layer2.append(z)
        # print(len(layer1_2))
        # print(layer1_2[0:10])
        # print(len(layer2))
        # print(layer2[0:10])
        data2={"level1":layer1_2,"level2":layer2}
        df2=pd.DataFrame(data2)
        # df2
        layer3=[]
        layer2_1=[]
        for i in range(0,len(layer2)):
            xpath="(//a[contains(text(),'"+str(layer2[i])+"')])[1]/../../../*/*/*/*/a"
            # print(xpath) (//a[contains(text(),'Насос топливный, комплектующие')])[1]/../../../*/*/*/*/a
            level_4_list=driver.find_elements(By.XPATH, xpath)
            # print(level_3_list)
            for j in range(0,len(level_4_list)):
                z=level_4_list[j].get_attribute('textContent')
                layer2_1.append(layer2[i])
                layer3.append(z)
        # print(len(layer2_1))
        # layer3[0:10]
        data3={"level2":layer2_1,"level3":layer3}
        df3=pd.DataFrame(data3)
        df3
        # пересобираем из обнаруженных связей
        main=[]
        level1=[]
        level2=[]
        level3=[]
        for i in range(0,len(df1)):
            for j in range(0,len(df2)):
                main.append(df1['main'][i])
                level1.append(df1['level1'][i])
                if df2['level1'][j]==df1['level1'][i]:
                    level2.append(df2['level2'][j])
                else:
                    level2.append('NaN')
        data4={"main":main,"level1":level1,"level2":level2}
        df4=pd.DataFrame(data4)
        df5=df4.drop_duplicates()
        df6=df5.reset_index(drop=True)
        # df6.tail(1000)
        main_=[]
        level1=[]
        level2=[]
        level3=[]
        for i in range(0,len(df6)):
            for j in range(0,len(df3)):
                main_.append(df6['main'][i])
                level1.append(df6['level1'][i])
                level2.append(df6['level2'][i])
                if df3['level2'][j]==df6['level2'][i]:
                    level3.append(df3['level3'][j])
                else:
                    level3.append('NaN')
        # print(len(main_))
        # print(len(level1))
        # print(len(level2))
        # print(len(level3))
        data5={"main":main_,"level1":level1,"level2":level2,"level3":level3}
        df7=pd.DataFrame(data5)
        df7
        df8=df7.drop_duplicates()
        df9=df8.reset_index(drop=True)

        return df9
    #driver = driver
    driver.get(links_0)
    time.sleep(1)
    # открывашка всего, что закрто
    knots_list = []
    leaf_list = []
    openall = driver.find_elements(By.XPATH,
                                "//li[@class='qgNode qgExpandClosed']/div[@class='qgExpand'] | //li[@class='qgNode qgExpandClosed qgIsLast']/div[@class='qgExpand']")
    main_list = driver.find_elements(By.XPATH,
                                    "//li[@class='qgNode qgExpandClosed']/div[@class='qgExpand']/../../../../div/*/*/*[2]/*/*")
    car_man = driver.find_element(By.XPATH, "//ul[@class='breadcrumb']/li[2]/a").get_attribute('textContent')
    car_model = driver.find_element(By.XPATH, "//ul[@class='breadcrumb']/li[3]/a").get_attribute('textContent')
    # собираем список основных узлов
    for i in range(0, len(main_list)):
        z = main_list[i].get_attribute('textContent')
        z = str(z).replace('  ', '')
        z = str(z).replace('\n', '')
        knots_list.append(z)
        time.sleep(0.1)
    # прокликиваем все закрытые узлы
    for i in range(0, len(openall)):
        openall[i].click()
        time.sleep(0.1)
    # вызов функции построения иерархии узлов
    df = left_side_build(knots_list, driver)
    print(car_man, car_model)
    # df


    # выбор только открытых узлов
    empt_list = []
    data = {'level3/4': empt_list, 'knot_name': empt_list, "knot_code": empt_list, "knot_img": empt_list,"part_names": empt_list,
            "part_nums": empt_list}

    open_leaf = driver.find_elements(By.XPATH,"//li[@class='qgNode qgExpandOpen']//ul[@class='qgContainer']/li[@class='qgNode qgExpandLeaf'] | //li[@class='qgNode qgExpandOpen']//ul[@class='qgContainer']/li[@class='qgNode qgExpandLeaf qgIsLast']")
    x = 1
    # *************************
    # здесь надо поправить условия цикла для полноценной работы, на 1 машину уходит где то час
    # *************************

    for r in range(0, len(open_leaf)):
        open_leaf[r].click()
        gogo=0
        while True:
            gogo = wait_for_element(driver, "//div[@class='gdImage']/..//*[3]")
            if gogo != 0:
                break
        while True:
            try:
                z = open_leaf[r].get_attribute('textContent')
                break
            except:
                print('Ошибка! Проблема при загрузке нового листа')
        z = str(z).replace('  ', '')
        z = str(z).replace('\n', '')
        print(z)
        time.sleep(1)

        df2 = right_part_collect(driver, z)

        df_start = pd.DataFrame(data)

        if x == 1:
            df3 = pd.concat([df_start, df2], ignore_index=True, sort=False)
            x = 0
        else:
            df3 = pd.concat([df3, df2], ignore_index=True, sort=False)
            print(str(len(df3)) + " - партномеров собарно")


    # df3

    # собираем левую и правую часть
    level0 = []
    level1 = []
    level2 = []
    level3 = []
    level4 = []
    level5 = []
    level6 = []
    level7 = []
    level8 = []

    car_man_ = []
    car_model_ = []

    model_00= []
    series_code_00= []
    series_description_00= []
    region_00= []
    engine_00= []
    gearbox_00= []
    bodyStyle_00= []
    steering_00= []
    links_00= []
    # temp=[]
    for i in range(0, len(df3)):
        for j in range(0, len(df)):
            if df3['level3/4'][i] == df['level1'][j] or df3['level3/4'][i] == df['level2'][j] or df3['level3/4'][i] == \
                    df['level3'][j]:
                level0.append(df['main'][j])
                level1.append(df['level1'][j])
                level2.append(df['level2'][j])
                level3.append(df['level3'][j])
                level4.append(df3['knot_name'][i])
                level5.append(df3['knot_code'][i])
                level6.append(df3['part_names'][i])
                level7.append(df3['part_nums'][i])
                level8.append(df3['knot_img'][i])
                # temp.append(df3['level3/4'][i])
                car_man_.append(car_man)
                car_model_.append(car_model)
                # ==============================================
                model_00.append(model_0)
                series_code_00.append(series_code_0)
                series_description_00.append(series_description_0)
                region_00.append(region_0)
                engine_00.append(engine_0)
                gearbox_00.append(gearbox_0)
                bodyStyle_00.append(bodyStyle_0)
                steering_00.append(steering_0)
                links_00.append(links_0)

    data = {"Car manufactor": car_man_,
            "Model code": model_00,
            "Series code": series_code_00,
            "Series description": series_description_00,
            "Region": region_00,
            "Engine": engine_00,
            "Gearbox": gearbox_00,
            "BodyStyle": bodyStyle_00,
            "Steering": steering_00,
            "Link": links_00,
            "Car manufactor": car_man_,
            "Car model": car_model_,
            "Main_knot": level0,
            "Sub_1": level1,
            "Sub_2": level2,
            "Sub_3": level3,
            #   "temp": temp,
            "Mid_knot_name": level4,
            "Mid_knot_code": level5,
            "Mid_knot_img": level8,
            "Part_name": level6,
            "Part_num": level7,
            }
    result_df = pd.DataFrame(data)
    result_df = result_df.drop_duplicates()
    result_df = result_df.sort_values(['Main_knot', 'Sub_1', 'Sub_2', 'Sub_3'])
    result_df = result_df.reset_index(drop=True)
    # result_df
            
    print('Сбор данных завершен...')
    # df3
    # складываем в эксель

    import openpyxl
    import datetime as DT

    now = DT.datetime.now()
    now = str(now)[:10]
    car_model = car_model.replace(".", "_")
    car_model = car_model.replace(",", "_")
    path = 'D:/my/@документы/GEEKBRAINS/Методы сбора и обработки данных из сети Интернет/L7/cars/' + car_man + series_description_0 + region_0 + engine_0 + '.xlsx'
    wb = openpyxl.Workbook()
    wb.save(filename=path)

    with pd.ExcelWriter(path, mode="a", engine='openpyxl', if_sheet_exists='replace') as writer:
        result_df.to_excel(writer, sheet_name=now)
    print('Сохранили в эксель...')
    #Складываем в MongoDB

    client = MongoClient()
    db = client['Car_base']
    data_dict = result_df.to_dict("records")
    db.data.insert_many(data_dict)


    print('Сохранили в MongoDB...')
    print("DONE")
# ======================================================================================================================================
# Собираем список моделей
all_done = 0
#  MAIN RUN
while True:
    driver.close
    if all_done == 1:
        print(f'ALL DONE')
        break
    try:
        driver.get(car_main_link)
        time.sleep(1)

        # прокликиваем свернутое справа

        try:
            rest_parts = driver.find_elements(By.XPATH, "//td[@colspan='99']/*[2]")
        except:
            print("ОШИБКА! Не найдена кнопка Больше модификаций")

            
        while True:
            try:
                for j in range(0, len(rest_parts)):
                    rest_parts[j].click()
                    
                break
            except Exception as ex:
                rest_parts = driver.find_elements(By.XPATH, "//td[@colspan='99']/*[2]")
                template = "ОШИБКА! Проблема при попытке прокликать Больше модификаций"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

        manufactor = []
        #model_name = []
        model = []
        series_code = []
        series_description =[]
        region = []
        engine =[]
        gearbox = []
        bodyStyle =[]
        steering = []
        links=[]
        manufactor_ = driver.find_elements(By.XPATH, "//li/a")
        #model_name_ = driver.find_elements(By.XPATH, "//div[@class='grouped-vehicles']//h3")
        model_ = driver.find_elements(By.XPATH, "//td[1]/*/a")
        series_code_ = driver.find_elements(By.XPATH, "//td[2]/*/*")
        series_description_ =driver.find_elements(By.XPATH, "//td[3]")
        region_ = driver.find_elements(By.XPATH, "//td[4]")
        engine_ = driver.find_elements(By.XPATH, "//td[5]")
        gearbox_ = driver.find_elements(By.XPATH, "//td[6]")
        bodyStyle_ =driver.find_elements(By.XPATH, "//td[7]")
        steering_ = driver.find_elements(By.XPATH, "//td[8]")
        links_ = driver.find_elements(By.XPATH, "//td[1]/span/a")





        for i in range(0, len(links_)):
            manufactor.append(manufactor_[1].get_attribute('textContent'))
            #model_name.append(model_name_[j].get_attribute('textContent'))
            model.append(model_[i].get_attribute('textContent'))
            series_code.append(series_code_[i].get_attribute('textContent'))
            series_description.append(series_description_[i].get_attribute('textContent'))
            region.append(region_[i].get_attribute('textContent'))
            engine.append(engine_[i].get_attribute('textContent'))
            if gearbox_[i].get_attribute('textContent') == None:
                gearbox.append('NaN')
            else:
                gearbox.append(gearbox_[i].get_attribute('textContent'))
            bodyStyle.append(bodyStyle_[i].get_attribute('textContent'))
            steering.append(steering_[i].get_attribute('textContent'))
            links.append(links_[i].get_attribute('href'))
            data ={"manufactor" : manufactor,
        # "model_name" : model_name,
        "model" : model,
        "series_code" : series_code,
        "series_description" : series_description,
        "region" : region,
        "engine" : engine,
        "gearbox": gearbox,
        "bodyStyle" : bodyStyle,
        "steering": steering,
        "links":links
        }

        df_hl=pd.DataFrame(data)

        client = MongoClient()
        db = client['Car_base']
        for i in range(0,len(df_hl)):
            db_existance_chek=db.data.count_documents({"Model code":df_hl['model'][i]}, limit=1)
            if db_existance_chek == 1:
                print(df_hl['series_description'][i] + df_hl['model'][i] + ' уже есть в базе')
                i=i+1
                if i==len(df_hl):
                    all_done = 1
                    break
            else:
                grabber (df_hl['model'][i],
                df_hl['series_code'][i],
                df_hl['series_description'][i],
                df_hl['region'][i],
                df_hl['engine'][i],
                df_hl['gearbox'][i],
                df_hl['bodyStyle'][i],
                df_hl['steering'][i],
                df_hl['links'][i],
                driver)
    except:
        print("Что то пошло не так, перезапускаем")
    

    



