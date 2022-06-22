#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 6 15:29:23 2019

@author: eps
"""

def downloadBOE():
    
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    import bs4
    import sys
    
    string=sys.argv[1]
    field=sys.argv[2]
    date1=sys.argv[3]
    date2=sys.argv[4]
    dirtosave=sys.argv[5]
        
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    
    options = Options();
    options.set_preference("browser.download.folderList",2);
    options.set_preference("browser.download.manager.showWhenStarting", False);
    options.set_preference("browser.download.dir",dirtosave);
    #options.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    options.set_preference("pdfjs.disabled", True)
    #options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/download,application/octet-stream");
    driver = webdriver.Firefox(executable_path='/Users/eps/Downloads/geckodriver', options=options)
    
    buscar=string
    
    
    boehtmlurl='https://www.boe.es/buscar/boe.php'
    driver.get(boehtmlurl)
    
    if(field=='texto'):
        fieldxpath="//*[@id='DOC']"
    if(field=='titulo'):
        fieldxpath="//*[@id='TIT']"
    
    busqueda = driver.find_element_by_xpath(fieldxpath)
    busqueda.send_keys(buscar)
    
    date1day=date1.split('/')[0]
    date1month=date1.split('/')[1]
    date1year=date1.split('/')[2]
    date2day=date2.split('/')[0]
    date2month=date2.split('/')[1]
    date2year=date2.split('/')[2]
    fecha1field = driver.find_element_by_xpath('//*[@id="desdeFP"]')
    fecha1field.click()
    fecha1field.send_keys(date1year+"-"+date1month+"-"+date1day)
    fecha2field = driver.find_element_by_xpath('//*[@id="hastaFP"]')
    fecha2field.click()
    fecha2field.send_keys(date2year+"-"+date2month+"-"+date2day)
    
    driver.find_element_by_xpath("/html/body/div[4]/div/form/div/div/input[1]").click()
    
    completecode=driver.page_source
    
    soup0=bs4.BeautifulSoup(completecode)
    
    notfoundstring='No se han encontrado documentos que satisfagan sus criterios de búsqueda'
    notfound=notfoundstring in [a.string for a in soup0.find_all("p")]
    if notfound:
        sys.exit("No documents were found with requested fields.")
    
    abc=soup0.find_all("span")[-1]
    
    if 'siguiente' in abc.text:
        numberofpages=int(soup0.find_all("span")[-2].string)
    if 'siguiente' not in abc.text:    
        numberofpages=1
    #counter = 0
    for page in range(numberofpages):
        print('Página',page+1)
    
        driver.get(boehtmlurl)
        busqueda = driver.find_element_by_xpath(fieldxpath)
        busqueda.send_keys(buscar)
        
        date1day=date1.split('/')[0]
        date1month=date1.split('/')[1]
        date1year=date1.split('/')[2]
        date2day=date2.split('/')[0]
        date2month=date2.split('/')[1]
        date2year=date2.split('/')[2]
        fecha1field = driver.find_element_by_xpath('//*[@id="desdeFP"]')
        fecha1field.click()
        fecha1field.send_keys(date1year+"-"+date1month+"-"+date1day)
        fecha2field = driver.find_element_by_xpath('//*[@id="hastaFP"]')
        fecha2field.click()
        fecha2field.send_keys(date2year+"-"+date2month+"-"+date2day)
    
        driver.find_element_by_xpath("/html/body/div[4]/div/form/div/div/input[1]").click()
    
        if(page+1 > 1):
            for timesnext in range(page):
                if(timesnext==0):
                    driver.find_element_by_xpath('/html/body/div[4]/div/div[3]/ul/li[4]/a').click()
                if(timesnext>0):
                    driver.find_element_by_xpath('/html/body/div[4]/div/div[3]/ul/li[5]/a').click()

    
        htmlsource=driver.page_source
        pagedocs=htmlsource.split('<li class="resultado-busqueda">\n')
    
        counter=0
        for i in range(len(pagedocs)-1):
            counter = counter + 1
            print('Documento',counter)
            
            docstring=pagedocs[i+1]
            soup = bs4.BeautifulSoup(docstring)
            aTags = soup.find_all("a")
            url = aTags[0]['href']
            urlcompleta= 'https://www.boe.es/' + url[3:]
            driver.get(urlcompleta)
            
            #doccode=driver.page_source
            #soup2 = bs4.BeautifulSoup(doccode,'html5lib')
            #pdfurl=soup2.find('li', attrs={'class': 'puntoPDF'}).find_all("a")[0]['href']
            #pdfcompleteurl = 'https://www.boe.es'+ pdfurl
            #driver.get(pdfcompleteurl)
            #driver.find_element_by_xpath('//*[@id="download"]').click()
            
            
            #driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/ul/li[2]/a').click()
            driver.find_element_by_partial_link_text('PDF').click()
            
    

downloadBOE()

