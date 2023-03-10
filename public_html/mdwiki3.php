<?php 
require ('header.php');
//---
$save  = isset($_GET['save']) ? 'checked' : '';
$title = isset($_GET['title']) ? $_GET['title'] : '';
//---
?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Med updater</h3>
    </div>
    <div class="card-body">
        <form action='mdwiki3.php' method='GET'>
            <div class='container-fluid'>
                <div class='row'>
                    <div class='col-md-3'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' name='title' value='<?php echo $title ?>' required/>
                        </div>
                    </div>
                    <div class='col-md-2'>
                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='save' name='save' value='1' <?php echo $save ?>>
                            <label class='form-check-label' for='save'>Auto save</label>
                        </div>
                    </div>
                    <div class='col-md-2'>
                        <input class='btn btn-primary' type='submit' value='send' />
                    </div>
                </div>
                <div class='input-group'>
                    
                </div>
            </div>
        </form>
<?php
//---
function strstartswith($text, $start) {
    return strpos($text, $start) === 0;
};
//---
function endsWith($string, $endString) {
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};
//---
function get_results($title) { 
    //---
    global $save;
    //---
    $dir = 'I:/mdwiki/TDpynew';  
    if ( $_SERVER['SERVER_NAME'] == 'mdwiki.toolforge.org' )    $dir = '/data/project/mdwiki/TDpynew'; 
    //---
    $title2 = rawurlencode($title);
    //---
    $sa = ($save != '') ? ' save' : '';
    //---
    $ccc = "python3 $dir/mdd.py $title2 from_toolforge ch $sa"; 
    //---
    if ( $_SERVER['SERVER_NAME'] != 'mdwiki.toolforge.org' or isset($_GET['test']) ) { 
        echo "<span style='font-size: 18px;'>$ccc</span>
        <br>";
    };
    //---
    $resultb = shell_exec($ccc);
    //---
    $resultb = trim($resultb);
    //---
    return $resultb;
}
//---
function worknew($title) {
    //---
    global $save;
    //---
    $new = 'https://mdwiki.org' . '/w/index.php?title=' . $title . '&action=submit';
    //---
    $form = "
    <form id='editform' name='editform' method='POST' action='$new'>
        <input type='hidden' value='' name='wpEdittime'/>
        <input type='hidden' value='' name='wpStarttime'/>
        <input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
        <input type='hidden' value='12' name='parentRevId'/>
        <input type='hidden' value='wikitext' name='model'/>
        <input type='hidden' value='text/x-wiki' name='format'/>
        <input type='hidden' value='1' name='wpUltimateParam'/>
        <input type='hidden' name='wpSummary' value='mdwiki changes.'>
        <input type='hidden' id='wikitext-old' value=''>
    ";
    //---
    $resultb = get_results($title);
    //---
    $edit_line = "<a class='btn btn-primary' href='$new'>Go to edit page.</a>";
    //---
    $t1  = strstartswith( $resultb , '/mdwiki/public_html/updatercash/' );
    $t2 = strstartswith( $resultb , '/mnt/nfs/labstore-secondary-tools-project/mdwiki/public_html/updatercash/' );
    $t3 = endsWith( $resultb , '.txt' );
    //---
    if (isset($_REQUEST['test'])) echo "results:($resultb)<br>";
    //---
    $edit_link = "<a type='button' class='btn btn-primary' href='$new'>Go to edit page.</a>";
    //---
    $edt_link_row = "
    <div class='col-sm'>
        $edit_link
    </div>";
    //---
    if ($resultb == 'no changes') {
        echo "no changes";
        echo $edt_link_row;
    } elseif ($resultb == "notext") {
        echo "text == ''";
        echo $edt_link_row;
    } elseif ($t1 || $t2 || $t3 || isset($_REQUEST['test'])) {
        $newtext = file_get_contents( $resultb );
        $form = $form . "
            <div class='form-group'>
                <label for='find'>new text:</label>
                <textarea class='form-control' rows='10' name='wpTextbox1'>$newtext</textarea>
            </div>
            <div class='editOptions aligncenter'>
                <input id='wpPreview' type='submit' class='btn btn-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
                <input id='wpDiff' type='submit' class='btn btn-primary' tabindex='7' name='wpDiff' value='show changes' accesskey='v' title='show changes.'>
                <div class='editButtons'>
                </div>
            </div>
        </form>";
        //---
        if ($save != "") {
            if ($resultb == "True") {
                echo 'changes has published';
            } else {
                echo 'Changes are not published, try to do it manually.'; 
                echo $form;
            };
        } else {
            echo $form;
        };
        //---
    } else {
        echo $resultb;
        echo $edt_link_row;
    };
    //---
};
//---
if ($title == '') {
    echo "
    ";
} else {
    worknew($title);
};
//---
?>
</div>
<?php require('foter.php'); ?>