<?
	function mjpeg_grab_frame($url) {
		$f = fopen($url, 'r');
		if($f) {
			$r = null;
			while(substr_count($r, "\xFF\xD8") != 2) $r .= fread($f, 512);
			$start = strpos($r, "\xFF\xD8");
			$end = strpos($r, "\xFF\xD9", $start)+2;
			$frame = substr($r, $start, $end-$start);
			fclose($f);
			return $frame;
		}
	}
	header("Content-type: image/jpeg");
	echo mjpeg_grab_frame('http://10.50.24.2:1181/stream.mjpg');