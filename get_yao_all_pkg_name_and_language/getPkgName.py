import os
import json





# 拿widget包名的key保存的文件名
WIDGET_PKG_KEY = 'WIDGET_PKG_KEY'
# 拿amber包名的key保存的文件名
AMBER_PKG_KEY = 'AMBER_PKG_KEY'



# 通过一个json字符串，获得包含包名的list
def getPkgNameList(str):
	return json.loads(str).get('result').get('1')
	

# 获得widget请求结果的str
def getWidgetResStr():
	xsrfKey = ''
	with open(WIDGET_PKG_KEY, 'r') as f:
		xsrfKey = f.read()
	return os.popen("curl 'https://play.google.com/apps/publish/androidapps?dev_acc=06161861376464805340' -H 'origin: https://play.google.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8,en;q=0.6' -H 'x-gwt-permutation: F65123E718D31FC0C8171F0098821A97' -H 'x-gwt-module-base: https://ssl.gstatic.com/play-apps-publisher-rapid/fox/bc58dcff4606f3cef508f61a36070fb0/fox/gwt/' -H 'cookie: _ga=GA1.3-3.478732673.1498454345; _gid=GA1.3-3.1965325179.1502864164; CONSENT=YES+CN.zh-CN+20170604-09-0; SID=DQUvvjQHKfnv3BAn5LUh4aSqQA9FrXae37YQT2D8KvetsE33PDwyZfPwtZ4McSd-d87nXg.; HSID=APPIOgNWeGT2-2atY; SSID=AUtclsGZnL40u9DjB; APISID=RE2ygbv_g7QMMbqa/AUZb-ikSpiQUjWVt8; SAPISID=DVHaMfBzmroa_8A5/AhNVTzI1lPFWKe4J5; enabledapps.uploader=0; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=chenbocong@amberweather.com; _ga=GA1.3.478732673.1498454345; _gid=GA1.3.1965325179.1502864164; S=billing-ui-v3=O03J46VBEhTDSM-XqdCxNirm2GoLhDWf:billing-ui-v3-efe=O03J46VBEhTDSM-XqdCxNirm2GoLhDWf; PLAY_PREFS=Cu4KCKeTnOCCCBLkCgoCSlAQze28zd4rGqUKERITFBUWGNQB1QGvAsQE4wXlBegF1wbYBt4G3waQlYEGkZWBBpKVgQaVlYEGl5WBBqSVgQa4lYEGwJWBBsGVgQbElYEGxZWBBsiVgQbOlYEGz5WBBtCVgQbUlYEG2ZWBBvKVgQb4lYEG-ZWBBoSWgQaHloEGi5aBBo-WgQaSloEGm5aBBp6WgQafloEGoJaBBqGWgQamloEGp5aBBqiWgQbul4EG75eBBoGYgQaCmIEGhZiBBomYgQaLmIEGvpiBBqubgQatm4EGyZuBBsqbgQbLm4EG1ZuBBvCbgQa8nYEG3Z2BBt6dgQbnnYEGkJ6BBuKigQbzooEG_KKBBoujgQaapIEGnqSBBrKkgQbqpYEGxqaBBtSmgQbWpoEG_qaBBoCngQaCp4EGhKeBBoangQaIp4EGiqeBBvKogQb0qIEGvKyBBtavgQbBsIEGh7KBBomygQbWsoEGsbSBBta5gQaOwIEGosCBBsDAgQbywIEG1sKBBozFgQaPxYEGysaBBvjHgQaqyoEG2MyBBtzMgQbdzYEGhs6BBqHPgQbE0oEGldWBBtrYgQbi2IEGk9mBBsvZgQby24EG2OSBBpflgQaT5oEGuOiBBs_rgQaw7IEG8e2BBsX0gQbX9YEGuvuBBsP_gQbE_4EGyf-BBtWDggbIhIIG3oWCBrmGggamh4IGp4eCBuyHggbth4IG642CBvuNggaJjoIGkY6CBpaOggbMkYIG7JeCBpWYgga2mYIGvZmCBo-aggaZmoIGwZqCBsiaggbKmoIG4ZqCBveaggbVnYIG4Z2CBp2eggbVnoIGuqCCBrugggbKoYIG9qKCBuKkggaSpYIGq6WCBs2lggbyp4IGnqiCBrSoggaBtIIGg7SCBoa0ggbktYIGrbaCBrG7ggbCu4IG8b6CBo-_ggbqwIIGvMGCBpvJggbnyYIGkcuCBs3LggbRy4IG1MuCBtrLggbfy4IG3MyCBorQggaL0IIG2NCCBvPRgga40oIG29OCBoDVggaC1YIGgdiCBpvYggam2IIGhtqCBo7aggaa2oIGo9qCBq3bggau24IGxduCBpbcggax3IIG6t2CBvjdggaJ3oIGuN6CBuTfggbv34IGpuGCBsjhggbQ4YIG5OGCBuXhggaj5YIGpuaCBoboggaW6YIGheuCBpXsggaj7YIGhe6CBpruggae7oIGsO6CBsbvggaF8IIGjPCCBo3wggac8IIGovCCBrHwggaW8YIGoPGCBr3xgga-8YIGt_KCBrnygga88oIGzfKCBuTyggbr9oIGrfiCBrP4ggbu-YIG9vqCBt77ggbj-4IGhPyCBq_8ggbD_IIG2_yCBt38ggar_YIGsv2CBtP-ggaB_4IGgICDBtyBgwbygYMGxIODBsWDgwbjhIMG6oSDBomFgwaQhYMGy4WDBtCFgwbEh4MGh4iDBp2IgwamiIMG0IiDBuuIgwbwiIMGo4yDBrCMgwbzjYMGqo6DBpCPgwbfkIMG2pGDBv6Rgwa4lYMGxJWDBqSWgwbWloMG5ZaDBtyXgwaVmYMGp5mDBrKZgwbrmYMG8pmDBvSZgwbamoMG45yDBoydgwbtnoMGmZ-DBp-ggwazoIMG_aCDBoihgwbDoYMGzKGDBs-igwbvooMG96KDBqyjgwbapIMGpqWDBtelgwbbpYMGzKeDBu2ogwbzqIMGpqmDBvergwb6q4MGgKyDBoisgwajrIMGoK6DBqOugwbxroMGsq-DBprPvQqxz70KKNvtvM3eKzokNzY0NGFiZWEtNjMyZS00ZDIxLWEzODEtM2E0NjhiNWNmY2VkQAFIAAr_Cgiv_L64lBsS9QoKAkpQEN-DoNTeKxq2ChITFRjxAawCxASHBeMF5QXoBdcG7geQlYEGkZWBBpKVgQaVlYEGl5WBBqSVgQa4lYEGwJWBBsGVgQbElYEGxZWBBsiVgQbJlYEGzJWBBs6VgQbQlYEG1JWBBtmVgQbylYEG-JWBBvqVgQaAloEGhpaBBoeWgQaMloEGj5aBBpGWgQabloEGn5aBBqCWgQahloEGopaBBqeWgQaoloEG7peBBu-XgQaCmIEGhZiBBomYgQaLmIEGvpiBBqubgQatm4EGyZuBBsqbgQbLm4EG1ZuBBvCbgQa8nYEG3Z2BBt6dgQbnnYEGkJ6BBuKigQbzooEG_KKBBoujgQaSo4EGmqSBBp6kgQaypIEG-aSBBv6kgQbrpYEGxqaBBtSmgQbWpoEG_qaBBoCngQaCp4EGhKeBBoangQaIp4EGiqeBBvKogQb0qIEG1qmBBrysgQbIr4EG1q-BBsGwgQaHsoEGibKBBtaygQaztIEG1rmBBo7AgQaiwIEGwMCBBvLAgQbWwoEGj8WBBsrGgQb4x4EG7siBBqrKgQbYzIEG3MyBBt3NgQaGzoEGoc-BBsTSgQaV1YEG2tiBBuLYgQaT2YEGy9mBBvLbgQbY5IEGl-WBBpPmgQa46IEGz-uBBrDsgQbx7YEGxfSBBtf1gQa6-4EGsP-BBrH_gQbA_4EGxf-BBsf_gQbJ_4EG1YOCBsiEggbehYIGuYaCBuiGggamh4IGp4eCBuyHggbth4IG642CBvuNggaJjoIGlY6CBpaOggbPkIIGzJGCBuyXggaVmIIGtpmCBr2ZggaPmoIGmZqCBsGaggbHmoIGzJqCBt-aggb3moIG1Z2CBuKdggadnoIGzp6CBs-eggbVnoIGuqCCBrugggb2ooIG4qSCBpKlggarpYIGzaWCBvKnggaeqIIGtKiCBoG0ggaDtIIGhLSCBuC1ggattoIGsbuCBsK7ggbxvoIGj7-CBurAgga8wYIGm8mCBufJggaRy4IGzcuCBtHLggbWy4IG3cuCBt_LggbczIIGitCCBozQggbY0IIG89GCBrfSggba04IG_tSCBvvVggaK1oIGgdiCBpvYggam2IIGhNqCBo3aggac2oIGo9qCBq3bggau24IGmNyCBrHcggbq3YIG-N2CBonegga53oIG5N-CBu_fggan4YIGx-GCBtDhggbk4YIG5eGCBqPlggam5oIGhuiCBpbpggaF64IGleyCBqPtggaF7oIGmu6CBp7uggaw7oIGzO-CBoXwggaM8IIGjfCCBpzwggah8IIGsfCCBpbxggag8YIGvfGCBr7xgga48oIGufKCBrzyggbM8oIG5fKCBuv2ggat-IIGs_iCBu75ggb2-oIG3vuCBuP7ggaE_IIGr_yCBsL8ggbE_IIG2_yCBt38gga2_YIG0_6CBoH_ggaAgIMG3IGDBvKBgwbDg4MG44SDBuqEgwaJhYMGkIWDBsqFgwbRhYMGh4iDBp2IgwaqiIMG0IiDBuqIgwbwiIMGo4yDBrCMgwbyjYMGqo6DBpCPgwb-kYMGuJWDBsSVgwajloMG1paDBuaWgwbcl4MGpZmDBqeZgwa6mYMG85mDBtqagwaYnIMG45yDBoudgwbNnYMG7Z6DBqGfgwaGoIMGn6CDBrOggwb9oIMGiKGDBsChgwbCoYMGzKGDBs6igwb6ooMGqqWDBtulgwbMp4MGtqiDBt-ogwboqIMG8qiDBvergwb6q4MG_6uDBoisgwajrIMGoK6DBqKugwbxroMGsq-DBprPvQq80b0KKP2UxNLeKzokOTUxY2IwM2EtMjljNC00MTNiLTlmYzItMDRkODRkMDBkMjNhQAFIAA:S:ANO1ljKxCNSW6UoMzQ; NID=110=qy4vav8m6HY28fn41AHu42kXpqE14zyzGUmZqjoiK5Gs-T9NL388I1SApIO1M-DBMur56og1twxQeojgZojWwKYGHbvWTUOchoBz9FwNwyWUAXpUWO2NtmZ-uCufRiBrqObFxf1I26WFJmh1nL_GNQZzrT0tCGBwqld0zkoQm_ur3Sicy209EqFH5bfIeFsE7RhcJSHcVWdJjtZKGPNixpNf5pY; SIDCC=AA248bevuVsQkFh1q2uE_K9crDRCYt6FEhpT0TgyZArPn9fzYOAwLev3IQ-BA3RV-4ZCUpzMZW2m29OQK4wpWA' -H 'x-client-data: CK61yQEIj7bJAQimtskBCMS2yQEIqZ3KAQ==' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' -H 'content-type: application/javascript; charset=UTF-8' -H 'accept: */*' -H 'referer: https://play.google.com/apps/publish/?dev_acc=06161861376464805340' -H 'authority: play.google.com' --data-binary '{\"method\":\"fetchIndex\",\"params\":\"{}\",\"xsrf\":\"" + xsrfKey +"\"}' --compressed").read();

# 获得amber请求结果的str
def getAmberResStr():
	xsrfKeyAmber = ''
	with open(AMBER_PKG_KEY, 'r') as f:
		xsrfKeyAmber = f.read()
	return os.popen("curl 'https://play.google.com/apps/publish/androidapps?dev_acc=01419791378100621000' -H 'origin: https://play.google.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8,en;q=0.6' -H 'x-gwt-permutation: F65123E718D31FC0C8171F0098821A97' -H 'x-gwt-module-base: https://ssl.gstatic.com/play-apps-publisher-rapid/fox/bc58dcff4606f3cef508f61a36070fb0/fox/gwt/' -H 'cookie: _ga=GA1.3-3.478732673.1498454345; _gid=GA1.3-3.1965325179.1502864164; CONSENT=YES+CN.zh-CN+20170604-09-0; SID=DQUvvjQHKfnv3BAn5LUh4aSqQA9FrXae37YQT2D8KvetsE33PDwyZfPwtZ4McSd-d87nXg.; HSID=APPIOgNWeGT2-2atY; SSID=AUtclsGZnL40u9DjB; APISID=RE2ygbv_g7QMMbqa/AUZb-ikSpiQUjWVt8; SAPISID=DVHaMfBzmroa_8A5/AhNVTzI1lPFWKe4J5; _ga=GA1.3.478732673.1498454345; _gid=GA1.3.1965325179.1502864164; NID=110=qy4vav8m6HY28fn41AHu42kXpqE14zyzGUmZqjoiK5Gs-T9NL388I1SApIO1M-DBMur56og1twxQeojgZojWwKYGHbvWTUOchoBz9FwNwyWUAXpUWO2NtmZ-uCufRiBrqObFxf1I26WFJmh1nL_GNQZzrT0tCGBwqld0zkoQm_ur3Sicy209EqFH5bfIeFsE7RhcJSHcVWdJjtZKGPNixpNf5pY; enabledapps.uploader=0; SIDCC=AA248bftnAuvKgGCFOjrTz0gh-MKTF-qvcuYwR2o7LAebdhk1yixkHTp8wc0F5MtXU1qZC-_w_F6vngoXPNNRQ' -H 'x-client-data: CK61yQEIj7bJAQimtskBCMS2yQEIqZ3KAQ==' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' -H 'content-type: application/javascript; charset=UTF-8' -H 'accept: */*' -H 'referer: https://play.google.com/apps/publish/?dev_acc=01419791378100621000' -H 'authority: play.google.com' --data-binary '{\"method\":\"fetchIndex\",\"params\":\"{}\",\"xsrf\":\"" + xsrfKeyAmber + "\"}' --compressed").read()


# 挨个输出报名
def printPkgName(nameList, array):
	for item in nameList:
		appState = item.get('5')
		pkgName = item.get('2')
		if appState == 1 and not 'com.amberweather.watchapp' in pkgName:# 已发布状态
			array.append(pkgName)



# 拿所有包名
def getPkgNameArray():
	widgetResultStr = getWidgetResStr()
	amberResultStr = getAmberResStr()
	pkgArray = []
	printPkgName(getPkgNameList(widgetResultStr), pkgArray)
	printPkgName(getPkgNameList(amberResultStr), pkgArray)
	return pkgArray

# 拿widget账号下的包名
def getWidgetPkgNameArray():
	widgetResultStr = getWidgetResStr()
	resultArray = []
	printPkgName(getPkgNameList(widgetResultStr), resultArray)

	return resultArray
# 拿amber账号下的包名
def getAmberPkgNameArray():
	amberResultStr = getAmberResStr()
	resultArray = []
	printPkgName(getPkgNameList(amberResultStr), resultArray)
	return resultArray