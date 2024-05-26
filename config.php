<?php
	$host = 'localhost';
	$dbuser ='acer_group';
	$dbpassword = '123456';
	$dbname = 'acer_group';

	$conn = mysqli_connect($host, $dbuser, $dbpassword,$dbname);

	if($conn){
		session_start();
		$memberId = isset($_SESSION['mid']) ? (int)$_SESSION['mid'] : 0;
	}
	else {
		echo "不正確連接資料庫</br>" . mysqli_connect_error();
	}
