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
<title>Splunk reports </title>

</head>
<body>

<?php
 $spl=shell_exec("python splunk.py");
 $abc=json_decode($spl,true);
        foreach ( $abc as $key=>$value )
        {
               <<construct the html table from the json data $abc by appropriate echo statements>>


        }



 ?>

</body>
</html>
