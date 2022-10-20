# -*- encoding:utf8 -*-

def create(data):
    script = 'var smallchart = AmCharts.makeChart("smallchart", {"type": "serial",'
    script += '"theme": "light","marginRight": 3,"marginLeft": 3,"autoMarginOffset": 2,'
    script += '"mouseWheelZoomEnabled":true,"dataDateFormat": "YYYY-MM","valueAxes": [{'
    script += '"id": "v1","axisAlpha": 0,"position": "left","ignoreAxisWidth":true}],'
    script += '"balloon": {"borderThickness": 1,"shadowAlpha": 0},"graphs": [{"id": "g1",'
    script += '"balloon":{"drop":true,"adjustBorderColor":false,"color":"#ffffff"},'
    script += '"bullet": "round","bulletBorderAlpha": 1,"bulletColor": "#FFFFFF","bulletSize": 3,'
    script += '"hideBulletsCount": 5,"lineThickness": 2,"title": "red line","useLineColorForBulletBorder": true,'
    script += '"valueField": "value","balloonText": "<span style=\'font-size:18px;\'>[[value]]</span>"'
    script += '}],"chartScrollbar": {"graph": "g1","oppositeAxis":false,"offset":30,'
    script += '"scrollbarHeight": 80,"backgroundAlpha": 0,"selectedBackgroundAlpha": 0.1,'
    script += '"selectedBackgroundColor": "#888888","graphFillAlpha": 0,"graphLineAlpha": 0.5,'
    script += '"selectedGraphFillAlpha": 0,"selectedGraphLineAlpha": 1,"autoGridCount":true,'
    script += '"color":"#AAAAAA"},"chartCursor": {"pan": true,"valueLineEnabled": true,'
    script += '"valueLineBalloonEnabled": true,"cursorAlpha":1,"cursorColor":"#258cbb",'
    script += '"limitToGraph":"g1","valueLineAlpha":0.2,"valueZoomable":true},'
    script += '"valueScrollbar":{"oppositeAxis":false,"offset":5,"scrollbarHeight":6'
    script += '},"categoryField": "date","categoryAxis": {"parseDates": true,"dashLength": 1,'
    script += '"minorGridEnabled": true},"export": {"enabled": false},'
    script += ' "dataProvider": ['
    
    provider = []
    for v in data:
        provider.append('{"date":"' + str(v.date) + '","value":"' + str(v.count) + '"}')
        
    script += ','.join(provider) + ']});'
    script += 'smallchart.addListener("rendered", zoomChart);'
    script += 'zoomChart();function zoomChart() {'
    script += 'smallchart.zoomToIndexes(smallchart.dataProvider.length - 100, smallchart.dataProvider.length - 1);}'
    script += 'window.onload = function() {document.getElementById("smallchart").style.width = "500px";'
    script += 'document.getElementById("smallchart").style.height = "210px";'
    script += '}'
    
    return script