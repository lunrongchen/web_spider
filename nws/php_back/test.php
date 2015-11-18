<?php

header( "Access-Control-Allow-Origin: *");

$startTime = $_GET['startTime'];
$endTime = $_GET['endTime'];

$config_file = fopen("/etc/yuqing", "r") or die("Unable to open file!");
$password=fgets($config_file);
fclose($config_file);

$dbconn = pg_connect("host=localhost dbname=news2 user=bdccl password=$password") or die ( 'Could not connect: ' . pg_last_error());

$query = 'select * from labeled ' . "where pubtime >= '$startTime' and pubtime < date '$endTime' + 1 " . 'order by id desc limit 100';

$result = pg_query($query) or die ('query failed: ' . pg_last_error());

$ans_stack=array();


echo '{"contentType":"news","startTime":"' . $startTime . '","endTime":"' . $endTime . '","data":';

$pre='';
echo "[";
while ( $ro=pg_fetch_object($result) )
{
	echo $pre;
	$pre = ",";
	echo json_encode($ro);
}
echo "]}";


pg_free_result($result);

pg_close($dbconn);


?>

