## 視覺化區 - 地圖
import folium # 匯入 folium 套件
import csv
import datetime

# 留著未來以後作為User所在地的定位參考使用
city = {'台中市' : [24.144144, 120.679654], 
		'南投縣' : [23.909384, 120.683914] }

def main():
	# 讀資料
	data = readData('covid19List.csv')
	# 畫地圖 & 儲存資料
	drawMap(data)
	print('OK!')

def readData(fileName):
	# 開啟 CSV 檔案
	with open(fileName, newline='') as csvfile:
		# 讀取 CSV 檔案內容
		# 日期, 編號, 地點, 備註, 狀態, 經度, 緯度
		data = list(csv.reader(csvfile)) # 資料要打包, 否則資料不能在外面用
	return data

def drawMap(data):	
	# 建立地圖與設定位置
	# zoom_start 為畫面細節
	fmap = folium.Map(location=city['台中市'], zoom_start=10)
	for row in data:
		# 0: 日期, 1:編號, 2:地點, 3:備註, 4:狀態, 5:經度, 6:緯度
		# 狀態為true表示這份資料沒問題, 可以顯示
		date, num, addr, note, status = row[0], row[1], row[2], row[3], bool(row[4])
		place = [float(row[5]), float(row[6])] # 經緯度

		# 顯示狀態為ture的地址
		if status:
			# 一週內顯示紅色, 一週以上顯示橘色
			now = datetime.datetime.now()
			d = datetime.datetime.strptime(date, '%Y-%m-%d')
			delta = now - d

			if delta.days <= 14: # 小於兩週的再顯示
				color = 'red' if delta.days <= 7 else 'orange'

				# 型態為市場則畫範圍
				date = "_" + date.replace("-","/") + "_";
				msg = date +'有確診者足跡'
				if '市場' in addr or '夜市' in addr or '商圈' in addr:
					mapChild = folium.Circle(location=place,
                	            color=color, # Circle 顏色
                    	        radius=150, # Circle 寬度
                        	    popup=msg, # 彈出視窗內容
                            	fill=True, # 填滿中間區域
                            	fill_opacity=0.3 # 設定透明度
                            	)
					fmap.add_child(child=mapChild)
				mapChild = folium.Marker(location=place,
        	         		popup=msg,
            	       		icon=folium.Icon(icon='info-sign', color=color))
				fmap.add_child(child=mapChild)

	fmap.save('covid19Map.html')

if __name__ == '__main__':
    main()