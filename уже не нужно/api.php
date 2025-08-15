<?php
header('Content-Type: application/json');

$apiToken = 'D2_FNI5LjIsTXxUhTq1VgpMKURTd99rF';

function query($method, $data)
{
    global $apiToken;

    $data = array_merge($data, ['apiToken' => $apiToken]);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, 'https://api.tehnomir.com.ua/' . $method);
    curl_setopt($curl, CURLOPT_HTTPHEADER, ['Content-Type: application/json', 'accept: application/json']);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
    $result = curl_exec($curl);
    curl_close($curl);

    return json_decode($result, true);
}

$output = [];

// 1. TEST CONNECT
$connectRequest = query('test/connect', ['string' => 'Test connection']);
if ($connectRequest['success'] === false) {
    echo json_encode(['success' => false, 'data' => $connectRequest['data']], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    die();
}
$output['test_connect'] = $connectRequest;


// Итоговый вывод всех ответов одним JSON
echo json_encode($output, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
