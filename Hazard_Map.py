import folium
from folium import plugins
import geopandas as gpd
import pandas as pd

#地図の中心を設定
#https://geoshape.ex.nii.ac.jp/ka/resource/25/25202140002.html
center=[35.215976,136.12398]
##OpenStreetMap
fmap1 = folium.Map(location=center,zoom_start = 15)

#シェイプファイル(.shp)の読み込み
#出典：国土数値情報 | 避難施設データ
#https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P20.html
#滋賀県内の避難施設データ
p20gdf25=gpd.read_file('https://japanhazardmap.github.io/DATA/GIS/MLITKSJ/P20Zips/P20-12_25_GML.zip')

#データフレームのカラムのリネーム
df=p20gdf25.rename(columns={
    'P20_001':'行政区域コード',
    'P20_002':'名称',
    'P20_003':'住所',
    'P20_004':'施設の種類',
    'P20_005':'収容人数',
    'P20_006':'施設規模(m2)',
    'P20_007':'地震災害',
    'P20_008':'津波災害',
    'P20_009':'水害',
    'P20_010':'火山災害',
    'P20_011':'災害分類その他',
    'P20_012':'災害分類指定なし'})

#GeoJSONファイル(p20kansai.geojson)の作成
df.to_file('p20shiga.geojson', driver='GeoJSON')

#GeoJSONに変換して地図に追加
folium.GeoJson(
    df,
    attribution='&copy; <a href="https://nlftp.mlit.go.jp/" target="_blank" rel="noopener">国土数値情報</a> ',
    name='避難施設',
    tooltip=folium.GeoJsonTooltip(fields=['名称', '住所', '施設の種類']),
    popup=folium.GeoJsonPopup(fields=['名称', '住所', '施設の種類']),
    zoom_on_click=True,
    ).add_to(fmap1)

#地理院地図
#出典：地理院地図｜地理院タイル一覧
#https://maps.gsi.go.jp/development/ichiran.html
folium.raster_layers.TileLayer(
    tiles='https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank" rel="noopener">国土地理院</a> ',
    name = '地理院地図',
    overlay = False,
    control = True
    ).add_to(fmap1)
#English GSI Map
folium.raster_layers.TileLayer(
    tiles='https://cyberjapandata.gsi.go.jp/xyz/english/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank" rel="noopener">国土地理院</a> ',
    name = 'English',
    overlay = False,
    control = True
    ).add_to(fmap1)
#Satellite Map
#https://gis.stackexchange.com/questions/290861/python-folium-package-for-satellite-map
#https://gist.github.com/Yago/05d479de169a21ba9fff
folium.raster_layers.TileLayer(
    tiles = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr = 'Esri',
    name = 'Esri Satellite',
    overlay = False,
    control = True
    ).add_to(fmap1)
#全国最新写真（シームレス）
folium.raster_layers.TileLayer(
    tiles = 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',
    attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank" rel="noopener">国土地理院</a> ',
    name = '全国最新写真（シームレス）',
    overlay = False,
    control = True
    ).add_to(fmap1)

#Layer of Disasters
#出典：ハザードマップポータルサイト
#https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html
#洪水浸水想定区域（想定最大規模）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_kuni_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '洪水浸水想定区域（想定最大規模）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#浸水継続時間（想定最大規模）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/01_flood_l2_keizoku_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '浸水継続時間（想定最大規模）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#家屋倒壊等氾濫想定区域（氾濫流）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/01_flood_l2_kaokutoukai_hanran_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '家屋倒壊等氾濫想定区域（氾濫流）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#家屋倒壊等氾濫想定区域（河岸侵食）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/01_flood_l2_kaokutoukai_kagan_data/{z}/{x}/{y}.png',
    fmt='image/png',
   attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '家屋倒壊等氾濫想定区域（河岸侵食）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#内水（雨水出水）浸水想定区域
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/02_naisui_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '内水（雨水出水）浸水想定区域',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#高潮浸水想定区域
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/03_hightide_l2_shinsuishin_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '高潮浸水想定区域',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#津波浸水想定
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/04_tsunami_newlegend_data/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '津波浸水想定',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#土砂災害警戒区域（土石流）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/05_dosekiryukeikaikuiki/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '土砂災害警戒区域（土石流）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#土砂災害警戒区域（急傾斜地の崩壊）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/05_kyukeishakeikaikuiki/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '土砂災害警戒区域（急傾斜地の崩壊）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#土砂災害警戒区域（地すべり）
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/05_jisuberikeikaikuiki/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '土砂災害警戒区域（地すべり）',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)
#雪崩危険箇所
folium.raster_layers.TileLayer(
    tiles='https://disaportaldata.gsi.go.jp/raster/05_nadarekikenkasyo/{z}/{x}/{y}.png',
    fmt='image/png',
    attr='&copy; <a href="https://disaportal.gsi.go.jp/hazardmap/copyright/opendata.html" target="_blank" rel="noopener">ハザードマップポータルサイト</a> ',
    name = '雪崩危険箇所',
    tms=False,
    overlay=True,
    control=True,
    opacity=0.7
    ).add_to(fmap1)


#Layer Control
folium.LayerControl().add_to(fmap1)

#Fullscreen
folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(fmap1)

# 地図を保存
fmap1.save('evacuation_map_shiga.html')

#fmap1
fmap1
