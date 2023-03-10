<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Import history from enwiki</h3>
    </div>
    <div class="card-body">
<?php
//---
$from       = $_REQUEST['from'];
$title      = $_REQUEST['title'];
$titlelist  = $_REQUEST['titlelist'];
$code       = $_REQUEST['code'];
//---
$err = '';
//---
if ( $code != 'James#99' && $code != 'james#99' && $code != '') {
    $err = "<span style='font-size:13pt;'>! (" . $code . ")</span><span style='font-size:13pt;color:red'> is wrong code.</span>";
};
//---
if ( ($titlelist == '' && $title == '') or $code == '' or ( $code != 'James#99' && $code != 'james#99' ) ) {
    //---
    $title = $_REQUEST['title']; 
    //---
    echo "
    <form action='import-history.php' method='POST'>
        <div class='container'>
            <div class='container'>
                <div class='row'>
                    <div class='col-lg-12'>
                        <div class='form-group'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Title:</span>
                                </div>
                                <input class='form-control' type='text' name='title' value='$title'/>
                            </div>
                        </div>
                    </div>
                    <div class='col-lg-12'>
                        <h3 class='aligncenter'>or</h3>
                    </div>
                    <div class='col-lg-12'>
                        <div class='form-group'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>List of titles:</span>
                                </div>
                                <textarea class='form-control' cols='20' rows='7' id='titlelist' name='titlelist'>$titlelist</textarea>
                            </div>
                        </div>
                    </div>
                    <div class='col-lg-12'>
                        <div class='form-group'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Code:</span>
                                </div>
                                <input class='form-control' type='text' name='code' value='$code' required/>
                                $err
                            </div>
                        </div>
                    </div>
                    <div class='col-lg-12'>
                        <h4 class='aligncenter'>
                            <input class='btn btn-primary' type='submit' value='send'>
                        </h4>
                    </div>
                </div>
            </div>
        </div>
    </form>
      ";
    //---
//---
} else {
//---
    //---
    $dir = '/mdwiki';  
    //---
    $filee = '/mdwiki/public_html/importlist.txt';
    $jsub = 'python3 ';
    //---
    if ( $_SERVER['SERVER_NAME'] == 'mdwiki.toolforge.org' ) { 
        $dir = '/mnt/nfs/labstore-secondary-tools-project/mdwiki/core'; 
        $jsub = 'jsub -N history python3 ';
        $filee = '/mnt/nfs/labstore-secondary-tools-project/mdwiki/public_html/importlist.txt';
    };
    //---
    $python3 = " $dir/pwb.py $dir/py/imp -page2:" . rawurlencode($title) . ' save' ;
    //---
    //if ( $code == 'James' ) {
    //---
    echo "<span style='font-size:15pt;color:green'>";
    //echo 'Hi, James:<br>';
    echo "";
    echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    if ($title != '') {
        $python3 = " $dir/pwb.py $dir/py/imp -page2:" . rawurlencode($title) . ' -from:' . rawurlencode($from) . ' save' ;
        //---
        if ($from == '') {
            echo 'The Bot will import ' . rawurldecode($title) . ' history in seconds.';
        } else {
            echo 'The Bot will import ' . rawurldecode($title) . ' history from (' . rawurldecode($from) . ') in seconds.';
        };
        //---
    } else {
        //---
        $myfile = fopen( 'importlist.txt' , "w");
        fwrite($myfile , $titlelist);
        fclose($myfile);
        //---
        $python3 = " $dir/pwb.py $dir/py/imp -file:" . $filee . ' save' ;
        //---
        echo 'The Bot will import history for titles in the list in seconds.';
        //---
    };
    echo '</span>';
    //---
    echo "<br>";
    $result = shell_exec($jsub . $python3);
    print $result;
    //---
    }
//---
?>
</div>
<?php require('foter.php'); ?>