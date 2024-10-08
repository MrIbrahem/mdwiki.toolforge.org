<?php

namespace Publish\Text;

/*

use function Publish\Text\get_medwiki_text;

*/


include_once __DIR__ . '/include.php';

use function Actions\CurlApi\post_url_params_result;

function get_medwiki_text($target)
{
    $params = [
        'title' => $target,
        'action' => 'raw',
    ];
    $endPoint = "https://medwiki.toolforge.org/ws/index.php?";

    $result = post_url_params_result($endPoint, $params);
    $result = trim($result);
    // if $result start with <pre> and end with </pre> remove them
    if (substr($result, 0, 5) == '<pre>' && substr($result, -6) == '</pre>') {
        $result = substr($result, 5, -6);
    }
    return $result;
}
