<?php
    $project_name = "your_project_name";
    $account_access_key = 'your_console_key';
    $account_access_secret = 'your_console_secret';
    $request_url = 'https://api.acrcloud.com/v1/monitor-streams?project_name='.$project_name;
    $http_method = 'GET';
    $http_uri = "/v1/monitor-streams";
    $timestamp = time();
    $signature_version = '1';
    

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
