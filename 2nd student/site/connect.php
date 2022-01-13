
<?

$connect = mysqli_connect("localhost","root");



@mysqli_select_db($connect,"news_data") or ("Database not found");

$querry = "SELECT * FROM `news`" ;




$sql = mysqli_query($connect,$querry);
$data = array();

while ($row_data = mysqli_fetch_assoc($sql))
    $data[] = $row_data;

$rows = 20; // количество строк
$cols = 1; // количество столбцов

echo '<table border="1">';

foreach($data as $data){
    
    
    echo "<tr>";
    echo "<th>";
    echo "link: ".$data['link']."<br />";
    echo "</th>";
    echo "<th>";
    echo "article: ".$data['article']."<br />";
    echo "</th>";
    echo "<th>";
    echo "date: ".$data['date']."<br />";
    echo "</th>";
    echo "<th>";
    echo "text: ".$data['text']."<br />";
    echo "</th>";
    echo "<th>";
    echo "comments: ".$data['comments']."<br />";
    echo     "<br />";
    echo "</th>";
    echo "</tr>";
    
}
mysqli_close($connect);
echo "</table>";

?>
