<?php

function monitor_update($stream_id, $stream_name, $url, $region, $realtime){
    $request_url = 'https://api.acrcloud.com/v1/monitor-streams/'.$stream_id;
    $http_method = 'PUT';
    $http_uri = '/v1/monitor-streams/'.$stream_id;
    $timestamp = time();
    $signature_version = '1';
    $account_access_key = '########account_access_key#########';
    $account_access_secret = '##########account_access_secret#########';

    $string_to_sign = $http_method . "\n" .
                      $http_uri ."\n" .
                      $account_access_key . "\n" .
                      $signature_version . "\n" .
                      $timestamp;
    $signature = hash_hmac("sha1",$string_to_sign,$account_access_secret,true);
    $signature = base64_encode($signature);

    $headerArray = array();
    $headers = array(
        'access-key' => $account_access_key,
        'timestamp' => $timestamp,
        'signature-version' => '1',
        'signature' => $signature
    );
    foreach( $headers as $n => $v ) {
        $headerArr[] = $n .':' . $v;
    }

    $put_data = array('stream_name'=>$stream_name, 'url'=>$url, "region"=>$region, "realtime"=>$realtime);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($put_data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headerArr);
    $response = curl_exec($ch);
    var_dump($response);
    curl_close($ch);
}

$stream_id = "STREAM_ID";
$stream_name = "stream name";
$url = "the stream url";
$region = "The stream region";
$realtime = 0;
monitor_update($stream_id, $stream_name, $url, $region, $realtime);
?>
