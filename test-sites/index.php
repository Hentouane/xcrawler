<form action="/index.php" method="get">
  User: <input type="text" name="query"><br>
  <input type="submit" value="Submit">
</form>

<?php
$xml = new DOMDocument;
$xml->preserveWhiteSpace = false;

$xml->Load('simple_test.xml');

if (isset($_REQUEST["query"])) {
  $xpath = new DOMXPath($xml);

  $query = $_REQUEST["query"];

  $request = "boolean('/data/users/user/" . $query . "')";

  $result_xpath = $xpath->evaluate($request);
  if ($result_xpath === NULL  || $result_xpath == 0){
    echo "User '" . $query, "' does not exists.", "<br/>";
  }
  else {
    echo "User '" . $query, "' exists.", "<br/>";
  } 
}
?>
