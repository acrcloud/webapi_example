<?php

function monitor_update($account_access_key, $account_access_secret, $stream_id, $action_type){
    $request_url = 'https://api.acrcloud.com/v1/monitor-streams/' . $stream_id.'/' . $action_type;
    $http_method = 'PUT';
    $http_uri = '/v1/monitor-streams/' . $stream_id . '/' . $action_type;
    $timestamp = time();
    $signature_version = '1';

    $string_to_sign = $http_method . "\n" .
                      $http_uri ."\n" .
                      $account_access_key . "\n" .
                      $signature_version . "\n" .
                      $timestamp;
    $signature = hash_hmac("sha1", $string_to_sign, $account_access_secret, true);
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

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headerArr);
    $response = curl_exec($ch);
    var_dump($response);
    curl_close($ch);
}

$account_access_key = '<account_access_key>';
$account_access_secret = '<account_access_secret>';
$stream_id = '<stream_id>';
$action_type = 'pause'; // pause or restart

monitor_update($account_access_key, $account_access_secret, $stream_id, $action_type);
?>
