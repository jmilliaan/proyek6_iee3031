<?php

echo '<A HREF="index.html"><h4>Return to Homepage</h4></A>';
echo "<h2>Robotic Arm, Conveyor Belt, Computer Vision System Log</h2><br>";

$servername = "127.0.0.1";
$username = "jm_03";
$password = "iee3031";
$dbname = "Proyek6_IEE3031";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}

$sql = "SELECT log_id, time, date, event FROM event_logging ORDER BY log_id DESC";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
  echo " Event ID | Event Time | Event Date | Event Details "; 
  echo "<br>";
  while($row = mysqli_fetch_assoc($result)) {
    echo $row["log_id"] . " | " . $row["time"] . " | " . $row["date"] . " | " .  $row["event"] . "<br>";
  }
} else {
  echo "0 results";
}

mysqli_close($conn);
?> 
