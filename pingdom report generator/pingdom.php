<!DOCTYPE html>
<html>
<head>
<style>

@import http://fonts.googleapis.com/css?family=Raleway;
/*----------------------------------------------
CSS Settings For HTML Div ExactCenter
------------------------------------------------*/
#main {
width:960px;
margin:50px auto;
font-family:raleway
}
span {
color:red
}
hr {
border:0;
border-bottom:1px solid #ccc;
margin:10px -40px;
margin-bottom:30px
}

#rtable {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

#rtable td, #rtable th {
    border: 1px solid #ddd;
    padding: 8px;
}

#rtable tr:nth-child(even){background-color: #f2f2f2;}

#rtable tr:hover {background-color: #ddd;}

#rtable th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}

</style>
<title>Pingdom Report</title>
</head>
<body>
<?php

     
     $newname=shell_exec("python pingdom.py <<search term 1>> <<search term 2>>");
     echo "<h2>Pingdom Post Major code Report</h2>";
     echo "<b>Average Response Time:</b> <p>Last 4 hours response time</p>";
     echo "<b>Base Response Time:</b> <p>Last week same 4 hour duration response time</p>";
     $abc=json_decode($newname,true);
            echo "<table id='rtable'>";
            echo "<th> checkname  </th>";
            echo "<th> average response time (ms) </th>";
            echo "<th> base response time (ms) </th>";
            echo "<th> Delta (ms) </th>";
     foreach ($abc as $key) {

                echo "<tr>";
                echo "<td>" .$key['name']. "</td>";
                echo "<td>" .$key['avgresponse']. "</td>";
                echo "<td>" .$key['baseavgresponse']. "</td>";
                echo "<td>" .$key['delta']. "</td>";
                echo "</tr>";
     }

            echo "</table>";
?>

</body>
</html>
