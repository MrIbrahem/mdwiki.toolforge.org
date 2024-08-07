<?php
require('header.php');
//---
?>

<style>
    .filterDiv {
        display: none;
    }

    .show2 {
        display: list-item;
    }

    .container {
        overflow: hidden;
    }

    .btne {
        border: none;
        outline: none;
        padding: 12px 16px;
        background-color: #f1f1f1;
        cursor: pointer;
    }

    .btne:hover {
        background-color: #ddd;
    }

    .btne.active {
        background-color: #5d8aa8;
    }
</style>
<?php
//---
// find:
// (\$[^=\s]+\s*=\s*\$_(?:REQUEST|GET|POST|SESSION)\[["'][^"']+["']\]\s*);
// (\$[^=\s]+\s*=\s*\$_(?:\w+)\[["'][^"']+["']\]\s*);
// (\$[^=\s]+\s*=\s*\$[^\$\s\[\]]+\[["'][^"']+["']\]\s*);  # bad
// replace by:
// $1 ?? "";
//---
$test = $_REQUEST['test'] ?? "";
$id = $_REQUEST['id'] ?? "";
//---
$strs = "Replace log for id:$id";
//---
if ($id == '') $strs = 'Replace log files';
//---
echo "
<div class='card-header aligncenter' style='font-weight:bold;'>
  <h3>$strs</h3>
</div>
<div class='card-body'>
  <div class='container'>

";
//---
function str_end_with($haystack, $needle)
{
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
};
//---
function open_dir()
{
    $files = array();
    if ($handle = opendir("find/log/")) {
        while (false !== ($file = readdir($handle))) {
            if ($file != "." && $file != ".." && !str_end_with($file, '-text.txt') && !str_end_with($file, '.bak')) {
                $files[$file] = filemtime("find/log/$file");
                // $files[filemtime("find/log/$file")] = $file;
            }
        }
        closedir($handle);
    }
    //---
    arsort($files);
    //---
    // len of $files
    $ln = count($files);
    //---
    // divid $ln by 3
    $ln2 = $ln / 3;
    $ln2 = $ln2 + 1;
    //---

    //---
    $fs = "
      <div class='col-md'>
        <ul>";
    //---
    $nd = "
        </ul>
      </div>
    ";
    //---
    echo "
    <div class='row'>
    $fs
    ";
    //---
    $n = 0;
    //---
    foreach ($files as $file_name => $file_time) {
        //---
        $n++;
        //---
        $lastModified = date('d F Y, H:i', $file_time);
        //---
        $file_name = str_replace('.txt', '', $file_name);
        //---
        if ($n >= $ln2) {
            echo "
          $nd
          $fs
          ";
            $n = 0;
        };
        //---
        echo "
        <li>
          <div class='group'>
              <a href='replace-log.php?id=$file_name'><b><span>$file_name</span></b></a>
              $lastModified
          </div>
        </li>
        ";
    }
    //---
    echo "
    $nd
    </div>
    ";
};
//---
if ($id == '') {
    //---
    open_dir();
    //---
} else {
    //---
    echo "
    You can stop this job (if it working now!) by click <a href='qdel.php?job=replace$id'><b><span style='color:red'>here</span></b></a>.";
    //---
    $textx_file = "find/log/$id-text.txt";
    if (is_file($textx_file)) {
        $textlog = file_get_contents($textx_file);
        echo '<pre>' . $textlog . '</pre>';
    };
    //---
    $f1 = "find/" . $id . "_find.txt";
    $f2 = "find/" . $id . "_replace.txt";
    //---
    if (is_file($f1) && is_file($f2)) {
        //---
        $find    = file_get_contents($f1);
        $replace = file_get_contents($f2);
        //---
        $find_row = "
        <div class='form-group'>
            <label for='find'>Find:</label>
            <textarea class='form-control' id='find' name='find' readonly='true'>$find</textarea>
        </div>";
        //---
        $replace_row = "
        <div class='form-group'>
            <label for='replace'>Replace with:</label>
            <textarea class='form-control' id='replace' name='replace' readonly='true'>$replace</textarea>
        </div>";
        //---
        echo "
        <div class='container-fluid'>
            <div class='row'>
                <div class='col-sm'>$find_row</div>
                <div class='col-sm'>$replace_row</div>
            </div>
        </div>";
    };
    //---
    $rows = '';
    //---
    $log = file_get_contents("find/log/$id.txt");
    //---
    $log = '{' . $log .  '"0":0}';
    $table = json_decode($log);
    //---
    $all = 0;
    $no_change = 0;
    $done = 0;
    $nodone = 0;
    //---
    foreach ($table as $title => $diffid) {
        //---
        if ($title != '0') {
            //---
            $all += 1;
            //---
            $url = "https://mdwiki.org/w/index.php?title=" . $title;
            //---
            $type = '';
            $color = '';
            $text = '';
            //---
            $sta = "
            <li class='filterDiv";
            $end = '</li>
            ';
            //---
            if ($diffid == "no changes") {
                //---
                $no_change += 1;
                $type = 'nochange';
                $color = '';
                $text = 'no changes';
                //---
            } elseif ($diffid > 0) {
                $done += 1;
                $type = 'done';
                $color = 'green';
                $text = 'done';
                $url = "https://mdwiki.org/w/index.php?diff=prev&oldid=" . $diffid;
            } else {
                //---
                $nodone += 1;
                $type = 'nodone';
                $color = 'red';
                $text = 'not done';
            };
            //---
            $rows .= "$sta $type'>page: <a href='$url'><b><span style='color:$color'>$title</span></b></a> $text. $end";
            //---
        };
    };
    //---
    // if ($nodone == 0) $rows .= "<li class='filterDiv nodone'>a</li>";
    //---
    if ($test != '') {
        $rows .= "
        <li>$log</li>";
    };
    //---
    echo "
    <div id='myBtnContainer'>
      <button class='btne active' id='all' onclick=filterSelection('all')>All ($all)</button>
      <button class='btne' id='done' onclick=filterSelection('done')>Done ($done)</button>
      <button class='btne' id='nodone' onclick=filterSelection('nodone')>Not Done ($nodone)</button>
      <button class='btne' id='nochange' onclick=filterSelection('nochange')>No Changes ($no_change)</button>
    </div>
    <br>
    <ul class='container-fluid' style='list-style-type: decimal;'>
    $rows
    </ul>
    <br>";
};
//---
// echo'</div>';
//---
?>


<script>
    filterSelection("all")

    function filterSelection(c) {
        $('.btne').removeClass('active');
        $('#' + c).addClass('active');

        var x, i;
        x = document.getElementsByClassName("filterDiv");
        if (c == "all") c = "";
        for (i = 0; i < x.length; i++) {
            w3RemoveClass(x[i], "show2");
            if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show2");
        }
    }

    function w3AddClass(element, name) {
        var i, arr1, arr2;
        arr1 = element.className.split(" ");
        arr2 = name.split(" ");
        for (i = 0; i < arr2.length; i++) {
            if (arr1.indexOf(arr2[i]) == -1) {
                element.className += " " + arr2[i];
            }
        }
    }

    function w3RemoveClass(element, name) {
        var i, arr1, arr2;
        arr1 = element.className.split(" ");
        arr2 = name.split(" ");
        for (i = 0; i < arr2.length; i++) {
            while (arr1.indexOf(arr2[i]) > -1) {
                arr1.splice(arr1.indexOf(arr2[i]), 1);
            }
        }
        element.className = arr1.join(" ");
    }
</script>
<?php
echo '<!-- start foter -->
';
require('footer.php');
//---
?>
