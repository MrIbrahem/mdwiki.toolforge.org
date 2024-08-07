<?PHP
namespace LeadHelp;

use function Functions\make_mdwiki_title;
use function Functions\make_target_url;

function make_table_lead($dd, $lang='') {

    global $md_titles_to_section;

    $sato = <<<HTML
        <table class='table table-striped compact soro table-mobile-responsive table-mobile-sided'>
            <thead>
                <tr>
                    <th>#</th>
                    <th>mdtitle</th>
                    <!-- <th>Section</th> -->
                    <th>Words</th>
                    <th>Views</th>
                    <th>Translated</th>
                    <th>Translator</th>
                </tr>
            </thead>
            <tbody>
        HTML;

    // {"mdtitle": "Abscess","target": "","lang": "ar","views": 576128,"words": 730,"translator": "","tr_type": ""}

    $noo = 0;
    foreach ( $dd AS $tat => $tabe ) {

        $noo += 1;

        $mdtitle = $tabe['mdtitle'] ?? "";
        $target  = $tabe['target'] ?? "";
        $views   = number_format($tabe['views']);
        $word    = number_format($tabe['words']);
        $translator = $tabe['translator'] ?? "";
        // $tr_type = $tabe['tr_type'] ?? "";

        $section = $md_titles_to_section[$mdtitle] ?? '';

        $nana = make_mdwiki_title($mdtitle);

        $target_link    = make_target_url($target, $lang);

        $laly = <<<HTML
            <tr class='filterDiv show2'>
                <th data-content="#">$noo</th>
                <td data-content="Title">$nana</td>
                <!-- <td data-content="Section">$section</td> -->
                <td data-content="Words">$word</td>
                <td data-content='Views'>$views</td>
                <td data-content="Translated">$target_link</td>
                <td data-content="Translator">$translator</td>
            </tr>
            HTML;

        $sato .= $laly;

    };

    $sato .= <<<HTML
        </tbody>
    </table>
    HTML;

    return $sato;

};
