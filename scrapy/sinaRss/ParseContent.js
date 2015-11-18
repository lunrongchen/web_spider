var fs = require('fs')
var read = require('node-readability')

var html = fs.readFileSync ( 'tmp.html','utf-8');

read( html, function( err, article, meta ){
	console.log( JSON.stringify({"title":article.title, "content":article.content}));
} )

