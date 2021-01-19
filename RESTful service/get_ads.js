var url = require('url');
var path = require('path');
var fs = require('fs');
var crypto = require('crypto');
var express = require('express');
//npm install request
var request = require('request');


const app = express();


var defaultOptions = {
    host: 'api.acrcloud.com',
    endpoint: '/v1/audios',
    signature_version: '1',
    secure: true,
    access_key: '#ACCESS_KEY#',
    access_secret: '#ACCESS_SECRET#'
};

function buildStringToSign(method, uri, accessKey, signatureVersion, timestamp) {
    return [method, uri, accessKey, signatureVersion, timestamp].join('\n');
}

function sign(signString, accessSecret) {
    return crypto.createHmac('sha1', accessSecret)
        .update(new Buffer.from(signString, 'utf-8'))
        .digest().toString('base64');
}

function get_audios(bucket, page, cb) {
    var current_data = new Date();
    var timestamp = current_data.getTime() / 1000;

    var endpoint = defaultOptions.endpoint

    var stringToSign = buildStringToSign('GET',
        endpoint,
        defaultOptions.access_key,
        defaultOptions.signature_version,
        timestamp);

    var signature = sign(stringToSign, defaultOptions.access_secret);

    var headers = {
        'access-key': defaultOptions.access_key,
        'signature-version': defaultOptions.signature_version,
        'signature': signature,
        'timestamp': timestamp
    };

    var requrl = "https://" + defaultOptions.host + endpoint + "?bucket_name=" + bucket + "&page=" + page

    request.get({
        url: requrl,
        method: 'GET',
        headers: headers,
    }, cb);

}


app.get('/ads', (req, res) => {


    get_audios("#PROJECT_NAME#", 1, function(err, httpResponse, body) {
        res.send(body);
    });

});


module.exports = app;