<?php
	include('config.php');
	
	
	switch ($_GET['act']) {
		case 'profile':
			$memberInfo = mysqli_fetch_assoc(mysqli_query($conn, "SELECT * FROM member WHERE member_id = " . $memberId));
			if (empty($memberInfo)) {
				$message = '請先登入會員';
				include('message.php');
				exit;
			}

			$dataArr = array(
				'fullname' => isset($_GET['fullname']) ? trim($_GET['fullname']) : '',
				'email' => isset($_GET['email']) ? trim($_GET['email']) : '',
				'tel' => isset($_GET['tel']) ? trim($_GET['tel']) : ''
			);

			if (
				mysqli_query(
					$conn,
					"UPDATE member " .
					"SET fullname = '" . $dataArr['fullname'] . "', " .
					"email = '" . $dataArr['email'] . "', " .
					"tel = '" . $dataArr['tel'] . "' " .
					"WHERE member_id = " . $memberId
				)
			) {
				header('location: message.php');
			}
		break;

		default:
			break;
	}