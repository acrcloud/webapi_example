var http = require('http');
var crypto = require('crypto');
var fs = require("fs");
var qs = require('querystring');  

function create_sign(data, secret_key) {
    return crypto.createHmac('sha1', secret_key).update(data).digest().toString('base64');
}

function recogize(host, access_key, secret_key, query_data, query_type) {
    var http_method = "POST"
    var http_uri = "/v1/identify"
    var data_type = query_type
    var signature_version = "1" 
    var current_data = new Date();
    var minutes = current_data.getTimezoneOffset();
    var timestamp = parseInt(current_data.getTime()/1000) + minutes*60 + '';
    var sample_bytes = query_data.length + '';

    var options = {
        hostname: host,
        port: 80,
        path: http_uri,
        method: http_method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    };

    var string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+timestamp;
    var sign = create_sign(string_to_sign, secret_key);
    var post_data = {
        'access_key':access_key, 
        'sample_bytes':sample_bytes, 
        'sample':query_data.toString('base64'),
        'timestamp':timestamp, 
        'signature':sign, 
        'data_type':data_type, 
        'signature_version':signature_version
    };

    var content = qs.stringify(post_data); 

    var req = http.request(options, function (res) {
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('BODY: ' + chunk);
        });
    });

    req.on('error', function (e) {
        console.log('problem with request: ' + e.message);
    });

    req.write(content);
    req.end();
}

// Replace "###...###" below with your project's host, access_key, access_scret
var host = "###YOUR_HOST###";
var your_access_key = "###YOUR_ACCESS_KEY###";
var your_access_secret = "###YOUR_ACCESS_SECRET###";

var data_type = 'audio';
var bitmap = fs.readFileSync('sample.wav');
recogize(host, your_access_key, your_access_secret, new Buffer(bitmap), data_type);
