<form action="/index.php" method="get">
  User: <input type="text" name="query"><br>
  <input type="submit" value="Submit">
</form>

<?php
$xml = new DOMDocument;
$xml->preserveWhiteSpace = false;

$xml->load('./tests-xml/user-pass-64.xml');

if (isset($_REQUEST["query"])) {
  $xpath = new DOMXPath($xml);

  $query = trim($_REQUEST["query"]);
  if (!empty($query)) {
    $request = "boolean(//data/users/user[text() = '" . $query . "'])";

    $result_xpath = $xpath->evaluate($request);
    if ($result_xpath === NULL  || $result_xpath == 0){
      echo "User '" . $query, "' does not exists.", "<br/>";
    }
    else {
      echo "User '" . $query, "' exists.", "<br/>";
    } 
  }
}
?>
