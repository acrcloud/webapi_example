<?php
    $your_bucket_name = "your bucket name";
    $request_url = 'https://api.acrcloud.com/v1/buckets/'.$your_bucket_name.'/channels';
    $http_method = 'GET';
    $http_uri = '/v1/buckets/'.$your_bucket_name.'/channels';
    $timestamp = time();
    $signature_version = '1';
    
    $account_access_key = 'xxxxx';
    $account_access_secret = 'xxxxxx';

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
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headerArr);
    $response = curl_exec($ch);
    var_dump($response);
    curl_close($ch);
?>
