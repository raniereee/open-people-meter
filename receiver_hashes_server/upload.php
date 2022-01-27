<?php
	$folder ="/home/guest/processing/hashes_server/hashes/";
		 
	if(!$_FILES)
	{
		echo 'No sent file!';
	}
	else
	{
		$file_name = $_FILES['upfile']['name'];
		$file_type = $_FILES['upfile']['type'];
		$file_size = $_FILES['upfile']['size'];
		$file_tmp_name = $_FILES['upfile']['tmp_name'];
		$error = $_FILES['upfile']['error'];
	}

	switch ($error){

		case 0:
			break;
		case 1:
			echo 'The file size is bigger than permitted in php file settings!';
			break;
		case 2:
			echo 'The file size is bigger than permitted!';
			break;
		case 3:
			echo 'O upload was not concluded!';
			break;
		case 4:
			echo 'O upload was ok!';
			break;
	}

	if($error == 0)
	{
		$serial  = (int) $_SERVER['HTTP_SERIAL'];
		#$event   = (int) $_SERVER['HTTP_EVENT'];
		$minute  =       $_SERVER['HTTP_MINUTE'];
		$length  = (int) $_SERVER['CONTENT_LENGTH'];


		if(is_uploaded_file($file_tmp_name))
		{
			$ret=move_uploaded_file($file_tmp_name, $folder.$minute."/".$file_name);
			if($ret)
			{
				Echo "File uploaded\n";
			} else
			{
				Echo "File not moved to destination folder. Check permissions\n";
			}
		}
		else
		{
			Echo "File is not uploaded.";
		} 
	}
?>
