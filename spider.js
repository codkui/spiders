var Crawler = require("crawler");

var c = new Crawler({
    // 在每个请求处理完毕后将调用此回调函数
    callback : function (error, res, done) {
        if(error){
            console.log(error);
        }else{
            var $ = res.$;
            // $ 默认为 Cheerio 解析器
            // 它是核心jQuery的精简实现，可以按照jQuery选择器语法快速提取DOM元素
            console.log($("title").text());
        }
        done();
    }
});

// 将一个URL加入请求队列，并使用默认回调函数
c.queue('https://www.baidu.com');

// 将多个URL加入请求队列
c.queue(['https://www.zhihu.com/','https://www.163.com']);

// 对单个URL使用特定的处理参数并指定单独的回调函数
// c.queue([{
//     uri: 'https://parishackers.org/',
//     jQuery: false,

//     // The global callback won't be called
//     callback: function (error, res, done) {
//         if(error){
//             console.log(error);
//         }else{
//             console.log('Grabbed', res.body.length, 'bytes');
//         }
//         done();
//     }
// }]);

// 将一段HTML代码加入请求队列，即不通过抓取，直接交由回调函数处理（可用于单元测试）
// c.queue([{
//     html: '<p>This is a <strong>test</strong></p>'
// }]);