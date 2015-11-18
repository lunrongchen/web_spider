<?php
header( "Access-Control-Allow-Origin: *");
echo '{"name":"' . $_GET["name"] . '"}';
?>
