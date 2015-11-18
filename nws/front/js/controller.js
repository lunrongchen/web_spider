/*
 *  init the map
 */

var map = new BMap.Map("map-container");
map.centerAndZoom("Beijing", 12);
map.enableScrollWheelZoom(); //启用滚轮放大缩小，默认禁用
map.enableContinuousZoom(); //启用地图惯性拖拽，默认禁用
map.addControl(new BMap.NavigationControl()); //添加默认缩放平移控件
map.addControl(new BMap.OverviewMapControl()); //添加默认缩略地图控件
map.addControl(new BMap.OverviewMapControl({
    isOpen: true,
    anchor: BMAP_ANCHOR_BOTTOM_RIGHT
})); //右下角，打开
var localSearch = new BMap.LocalSearch(map);
localSearch.enableAutoViewport(); //允许自动调节窗体大小


// controll all the news
// and bind to a grouped list

/**
 * data manager
 */

//var NewsManager = function () {
//    this.rawData = [];
//    this.groupData = new Map();
//    this.initRaw = function (data) {
//        this.rawData = data;
//        this.groupData = new Map();
//    }
//    this.appendRaw = function (data) {
//        var tmp = this.rawData.concat(data);
//        this.rawData = tmp;
//        this.grouplist(data);
//    }
//    this.add2group = function (obj) {
//        console.log("at add2group");
//        d = new Date(Date.parse(obj['pubdate'] + "T" + obj['pubtime'] + ".800Z"));
//
//        console.log(d.toISOString());
//
//        content = contentWrapper(d.toLocaleString() + '<br>' + obj['content']);
//
//        if (this.groupData.get(obj['location']) == undefined) {
//            this.groupData.set(obj['location'], content);
//        } else {
//            pre = this.groupData.get(obj['location']);
//            this.groupData.set(obj['location'], content + pre)
//        }
//    }
//    this.grouped = function () {
//        console.log("at grouped");
//        this.grouplist(this.rawData);
//    }
//    this.grouplist = function (data) {
//        for (var i in data) {
//            var obj = data[i];
//            this.add2group(obj);
//        }
//    }
//    this.getGroupByAddr = function (addr) {
//        return '<ul>' + this.groupData.get(addr) + '</ul>';
//    }
//    return this;
//}
//
//nm = NewsManager();
//nm.initRaw(DATA);
//nm.grouped()
//



/**
 * add content to BaiduMarker
 */

function webContentWrapper(tag, attr, content) {
    return '<' + tag + " " + attr + ' >' + content + '</' + tag + '>';
}

function infoWindowWrapper(divcontent) {
    return webContentWrapper('div', 'class="infoWindow"', divcontent);
}

function contentWrapper(content) {
    return webContentWrapper('li', 'class="infoWindowItem"', content);
}


//function appendList(contentList) {
//    //清空原来的标注
//    map.clearOverlays();
//
//    // 添加需要插入的内容序列
//    console.log('appendList2');
//    for (var idx in contentList) {
//        var obj = contentList[idx];
//
//        // 搜索列表中的地名， 相当于添加到了地图中
//        localSearch.search(obj["location"]);
//
//        console.log(obj["location"], obj["content"]);
//    }
//    console.log("appendList3");
//
//
//    // 当一次地点搜索完成时， 会执行的回调函数
//    localSearch.setSearchCompleteCallback(
//        /**
//         * [[搜索完成的回调函数]]
//         * @param {BaiduLocationObject}   searchResult [[百度地图搜索结果对象]]
//         */
//        function (searchResult) {
//            // 获取地点
//            var poi = searchResult.getPoi(0);
//
//            //创建一个地点的标记
//            var marker = new BMap.Marker(new BMap.Point(poi.point.lng, poi.point.lat)); // 创建标注，为要查询的地方对应的经纬度
//
//            //将标记添加到地图上
//            map.addOverlay(marker);
//
//            //将地图的中心点设置为当前搜索的地点，缩放为6
//            map.centerAndZoom(poi.point, 6);
//
//
//            // keyword是被搜索的地名
//            var keyword = searchResult.keyword;
//
//
//            // 获取新闻的内容（通过地名获取新闻列表）
//            var content = "";
//            content = nm.getGroupByAddr(keyword);
//
//            // 创建一个弹窗，将内容包裹起来
//            var infoWindow = new BMap.InfoWindow(webContentWrapper('h3', '', keyword) + infoWindowWrapper(content));
//
//
//            // 监听鼠标移入事件
//            marker.addEventListener("mouseover", function () {
//                this.openInfoWindow(infoWindow);
//                console.log(this);
//            });
//
//            /*
//            // 监听鼠标移出事件
//            marker.addEventListener("mouseout", function () {
//                this.closeInfoWindow(infoWindow);
//                console.log(this, this.getBoundingClientRect());
//            });
//            */
//        });
//}
//
//appendList(DATA);

console.log('hello2');

function getData(url) {
    console.log('gts');
    var p = $.getJSON(
        url,
        function (data) {
            var tmp = [];
            for (var i in data) {
                var o = data[i];

                // 验证数据的有效性
                if (o != undefined && o.hasOwnProperty('pubdate') != false && o.hasOwnProperty('content') != false) {
                    tmp.push(o);
                }
            }
            console.log(tmp);
            nm.initRaw(tmp);
            nm.grouped()
            appendList(tmp);
        });

    console.log('gte');
}


console.log('hello3');